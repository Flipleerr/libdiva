import os
import sys

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

class DLTWriter:
  def __init__(self, filepath):
    self.filepath = filepath
    self.entries = []

  def add_entry(self, entry):
    self.entries.append(entry)

  def write(self):
    with open(self.filepath, "w", encoding="utf-8") as file:
      file.write("\n".join(self.entries) + "\n")