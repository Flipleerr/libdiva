# pylint: disable=C0103,C0301,C0303,W0201,W0718,R0902
"""FARC file handling"""
import struct
import gzip
import os
from Crypto.Cipher import AES

FARC_KEY = b"project_diva.bin"

class ExtractFARC:
  """
  class for extracting FARC archives.
  this class requires a filepath argument.
  """
  def __init__(self, filepath):
    self.filepath = filepath
    self.entries = []
    self._parse_header(filepath)
    self.xsize = None
    self.parse_entries()

  def _parse_header(self, filepath):
    """checks the file's header and sets variables accordingly"""
    with open(filepath, 'rb') as f:
      header = f.read(4)
      if header == b'FARC':
        self.limit = struct.unpack(">I", f.read(4))[0]
        self._FARC(f)
      elif header == b'FArC':
        self.limit = struct.unpack(">I", f.read(4))[0]
        dummy = struct.unpack(">I", f.read(4))[0]
        self._FArC()
      elif header == b'FArc':
        self.limit = struct.unpack(">I", f.read(4))[0]
        dummy = struct.unpack(">I", f.read(4))[0]
        self._FArc()
      else:
        raise ValueError("not a farc file. check the header.")

  def _FARC(self, f):
    """defines variables for FARC extraction"""
    self.header = b"FARC"
    self.is_compressed = True
    self.is_encrypted = True
    self.dummy = struct.unpack(">I", f.read(4))[0]
    self.xsize = struct.unpack(">I", f.read(4))[0]
    f.read(8)
  
  def _FArC(self):
    """defines variables for FArC extraction"""
    self.header = b"FArC"
    self.is_compressed = True
    self.is_encrypted = False

  def _FArc(self):
    """defines variables for FArc extraction"""
    self.header = b"FArc"
    self.is_compressed = False
    self.is_encrypted = False

  def parse_entries(self):
    """
    parses the filelist inside a FARC. 
    you do not need to call this method from your scipts as it's called from the extract() method.
    """
    with open(self.filepath, 'rb') as f:
      if self.header == b'FARC':
        f.seek(15)
      else:
        f.seek(12)

      curr_pos = f.tell()

      while curr_pos < self.limit:
        name = b''
        while True:
          char = f.read(1)
          if char == b'\x00':
            break
          name += char
        name = name.decode('utf-8')

        offset = struct.unpack(">I", f.read(4))[0]

        if self.header != b'FArc':
          zsize = struct.unpack(">I", f.read(4))[0]
        else:
          zsize = None
          
        size = struct.unpack(">I", f.read(4))[0]

        self.entries.append({
          'name': name,
          'offset': offset,
          'zsize': zsize,
          'size': size
        })

        self.entries = [entry for entry in self.entries if entry['name'] and (entry['size'] > 0 or entry['zsize'] > 0)]

        curr_pos = f.tell()
        print(self.entries)
        
  def extract(self, output_dir=None):
    """
    extracts files from a FARC archive.
    this method requires an output directory variable.
    """
    if not self.entries:
      self.parse_entries()

    os.makedirs(output_dir, exist_ok=True)

    with open(self.filepath, 'rb') as f:
      for entry in self.entries:
        output_path = os.path.join(output_dir, entry['name'])

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        f.seek(entry['offset'])

        if entry['zsize'] is not None and entry['size'] == entry['zsize']:
          self.is_compressed = False
          data = f.read(entry['size'])

        if self.is_compressed:
          # align zsize to a 16 byte boundary because AES
          aligned_zsize = entry['zsize']
          if aligned_zsize % 16 != 0:
            aligned_zsize += 16 - (aligned_zsize % 16)

          f.seek(entry['offset'])
          compressed_data = f.read(aligned_zsize)
          
          if self.is_encrypted:
            cipher = AES.new(FARC_KEY, AES.MODE_ECB)
            compressed_data = cipher.decrypt(compressed_data)
            compressed_data = compressed_data[:entry['zsize']]

          print(f"extracting {entry['name']}: size={entry['size']}, zsize={entry['size']}, compressed data length={len(compressed_data)}")

          try:
            data = gzip.decompress(compressed_data)
            if len(data) != entry['size']:
              print("warning: decompressed data length is longer than original")

          # pylint complains about this block; but the sheer amount of gzip errors is absurd so off it goes
          except Exception as e:
            print(f"error: failed to decompress {entry['name']}: {e}")
            continue
          
          if len(data) > entry['size']:
            data = data[:entry['size']]

        with open(output_path, 'wb') as out_f:
          out_f.write(data)

        print(f"extracted {entry['name']}")
