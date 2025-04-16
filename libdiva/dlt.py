"""DLT file reader and writer"""
class DLTReader:
  """read DLT files and print in terminal"""
  def __init__(self, filepath):
    """init filepaths and contents"""
    self.filepath = filepath
    self.contents = []

  def read(self):
    """read the DLT and store contents"""
    with open(self.filepath, "r", encoding="utf-8") as f:
      self.contents = f.read()

  def print_contents(self):
    """print in terminal"""
    if self.contents is not None:
      print(self.contents)

class DLTWriter:
  """write fresh DLT files with user data"""
  def __init__(self, filepath):
    """init filepaths and user entries"""
    self.filepath = filepath
    self.entries = []

  def add_entry(self, entry):
    """add entries to list"""
    self.entries.append(entry)

  def write(self):
    """write contents to a file"""
    with open(self.filepath, "w", encoding="utf-8") as f:
      f.write("\n".join(self.entries) + "\n")
