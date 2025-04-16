# pylint: disable=E1101
"""libdiva - a library for manitpulating files specific to the Project Diva series"""
import argparse
from .dlt import DLTReader, DLTWriter
from .divafile import encrypt_divafile, decrypt_divafile

def main():
  """main method"""
  parser = argparse.ArgumentParser(
    description="a library with various tools to extract and create files specific to " \
    "the Project Diva series.",
      add_help=False)
  parser.add_argument("filepath", type=str, help="path to your file of choice")
  parser.add_argument("--write", nargs="+", help="write to DLT file")
  parser.add_argument("--read", action="store_true", help="read from DLT file")
  parser.add_argument("--encrypt", action="store_true", help="encrypt a file using DIVAFILE")
  parser.add_argument("--decrypt", action="store_true", help="decrypt a file from DIVAFILE")
  parser.add_argument("--help", action="help", help="show this help message and exit")
  args = parser.parse_args()

  if args.write:
    dlt_writer = DLTWriter(args.filepath)
    for entry in args.write:
      dlt_writer.add_entry(entry)
    dlt_writer.write()
    print(f"Written to {args.filepath}")

  elif args.encrypt:
    output_path = encrypt_divafile(args.filepath)
    print(f"encrypted {output_path}")

  elif args.decrypt:
    output_path = decrypt_divafile(args.filepath)
    print(f"decrypted {args.filepath}")

  elif args.read:
    dlt_reader = DLTReader(args.filepath)
    dlt_reader.read()
    dlt_reader.print_contents()

  elif args.help:
    argparse.print_help()

  else:
    print("use --help to get a list of available commands.")

if __name__ == "__main__":
  main()
