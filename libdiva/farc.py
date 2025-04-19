"""FARC file handling"""
from Crypto.Cipher import AES
import struct
import gzip
import os

FARC_KEY = b"project_diva.bin"

class ExtractFARC:
  def __init__(self, filepath):
    self.filepath = filepath
    self.entries = []
    self._parse_header(filepath)
    self.xsize = None
    self.parse_entries()

  def _parse_header(self, filepath):
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
    self.header = b"FARC"
    self.is_compressed = True
    self.is_encrypted = True
    self.dummy = struct.unpack(">I", f.read(4))[0]
    self.xsize = struct.unpack(">I", f.read(4))[0]
    f.read(8)
  
  def _FArC(self):
    # hacky way of checking FArCs
    # uncompressed FArCs exist and all files inside are 0 bytes when "decompressed"
    self.header = b"FArC"
    self.is_compressed = True
    self.is_encrypted = False

  def _FArc(self):
    self.header = b"FArc"
    self.is_compressed = False
    self.is_encrypted = False

  def parse_entries(self):
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
    if not self.entries:
      self.parse_entries()

    os.makedirs(output_dir, exist_ok=True)

    with open(self.filepath, 'rb') as f:
      for entry in self.entries:
        output_path = os.path.join(output_dir, entry['name'])

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        f.seek(entry['offset'])

        if self.header == b"FArc" or (entry['zsize'] is not None and entry['size'] == entry['zsize']):
          data = f.read(entry['size'])

        else:
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

          print(f"{entry['name']}: offset={entry['offset']}, size={entry['size']}, zsize={entry['size']}, compressed data length={len(compressed_data)}")
          print(compressed_data)

          try:
            data = gzip.decompress(compressed_data)
            if len(data) != entry['size']:
              print("warning: decompressed data length is longer than original")

          except Exception as e:
            print(f"error: failed to decompress {entry['name']}: {e}")
            continue
          
          if len(data) > entry['size']:
            data = data[:entry['size']]

        with open(output_path, 'wb') as f:
          f.write(data)

        print(f"extracted {entry['name']}")