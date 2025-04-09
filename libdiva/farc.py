import io
import struct

print("Debug: program worky!!")

class FARCExtract:
  def __init__(self, filepath):
    self.filepath = filepath
    self.f = None

  def open(self):
    self.f = open(self.filepath, "rb")

  def close(self):
    if self.f:
      self.f.close()
      self.f = None

  def check_header(self):
    try:
      self.open()
      header = self.f.read(4)
      print(f"Header: {header}")
      if header != b'FARC':
        raise ValueError("invalid FARC header. check for corruption or wrong file type")
      return True
    finally:
      self.close()

if __name__ == "__main__":
  import sys
  if len(sys.argv) != 2:
    print("Usage: python farc.py <farc_file>")
    sys.exit(1)
  
  farc = FARCExtract(sys.argv[1])
  try:
    farc.check_header()
    print("checked header")
  except ValueError as e:
    print(f"Error: {e}")
    sys.exit(1)
    
    