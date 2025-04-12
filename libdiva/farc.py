import io
import struct
import sys

class FARCExtract:
  def __init__(self, filepath):
    self.filepath = filepath
    self.f = None
    self.filenames = []

  def check_header(self):
    with open(self.filepath, 'rb') as f:
      self.f = f
      self.f.seek(0)
      header = self.f.read(4)
      if header !=b'FARC':
        raise ValueError("invalid header. is this a valid farc file?")

  def parse_flist(self):
    with open(self.filepath, 'rb') as f:
      f.seek(0x28)

      while True:
        chunk = f.read(4)
        if chunk == b"xxxx":
          break

        f.seek(-4, io.SEEK_CUR)

        entry = f.read(32) # all filenames seem to be allocated a 32 byte space within the file list
        filename = entry.split(b'\x00')[0].decode('ascii', errors='ignore')
        self.filenames.append(filename)

        f.read(8)

  def print_flist(self):
    for name in self.filenames:
      print(name)

if __name__ == "__main__":
  import sys
  if len(sys.argv) != 2:
    print("Usage: python farc.py <farc_file>")
    sys.exit(1)
  
  farc = FARCExtract(sys.argv[1])
  try:
    farc.check_header()
    print("info: valid header found.")
    farc.parse_flist()
    print(f"info: parsed files: ")
    farc.print_flist()
  except ValueError as e:
    print(f"Error: {e}")
    sys.exit(1)
    