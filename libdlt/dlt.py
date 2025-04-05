class DLTReader:
  def __init__(self, filepath):
    self.filepath = filepath
    self.contents = []

  def read(self):
      with open(self.filepath, "r", encoding="utf-8") as file:
        self.contents = file.read()

  def print_contents(self):
    if self.contents is not None:
      print(self.contents)
    else:
      print("No contents to display. Call read() first.")