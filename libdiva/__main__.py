# pylint: disable=E1101
"""libdiva - a library for manitpulating files specific to the Project Diva series"""
import argparse
import sys
from .dlt import DLTReader, DLTWriter
from .divafile import encrypt_divafile, decrypt_divafile
from .farc import ExtractFARC

def main():
  """main method"""
  parser = argparse.ArgumentParser(
    description="a library with various tools to extract and create files specific to " \
    "the Project Diva series.",
      add_help=False)
  parser.add_argument("filepath", type=str, help="path to your file of choice")
  parser.add_argument("output_dir", type=str, nargs="?", help="the output directory for FARC files")
  parser.add_argument("--write", nargs="+", help="write to DLT file")
  parser.add_argument("--read", action="store_true", help="read from DLT file")
  parser.add_argument("--encrypt", action="store_true", help="encrypt a file using DIVAFILE")
  parser.add_argument("--decrypt", action="store_true", help="decrypt a file from DIVAFILE")
  parser.add_argument("--extract", action="store_true", help="extract a FARC")
  parser.add_argument("--help", action="help", help="show this help message and exit")
  parser.add_argument("--version", action="version", version="libdiva v0.1.2 (the filler update)")
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

  elif args.extract:
    if not args.output_dir:
      print("error: --extract requires you to provide an output directory.")
      sys.exit(1)
    extract = ExtractFARC(args.filepath)
    extract.extract(args.output_dir)

  elif args.help:
    argparse.print_help()

  else:
    print("use --help to get a list of available commands.")

if __name__ == "__main__":
  main()
