# pylint: disable=E1101
"""libdiva - a Project Diva format library and command-line tool"""
import argparse
import sys
from .dlt import DLTReader, DLTWriter
from .divafile import encrypt_divafile, decrypt_divafile
from .farc import ExtractFARC

def main():
  """main method"""
  parser = argparse.ArgumentParser(
    description="a Project Diva format library and command-line tool",
      add_help=False)
  subparsers = parser.add_subparsers(dest="command", required=True)
  parser.add_argument("--help", action="help", help="show this help message and exit")
  parser.add_argument("--version", action="version", version="libdiva v0.1.2 (the filler update)")
  dlt_parser = subparsers.add_parser("dlt", help="read or write DLT files")
  dlt_parser.add_argument("filepath", nargs="?", type=str, help="path to your file of choice")
  dlt_parser.add_argument("--write", help="write to DLT file")
  dlt_parser.add_argument("--entries", nargs="+", help="entries to be written to a DLT file. used exclusively with write")
  dlt_parser.add_argument("--read", action="store_true", help="read from DLT file")
  divafile_parser = subparsers.add_parser("divafile", help="encrypt or decrypt DIVAFILEs")
  divafile_parser.add_argument("filepath", nargs="?", type=str, help="path to your file of choice")
  divafile_parser.add_argument("--encrypt", action="store_true", help="encrypt a file using DIVAFILE")
  divafile_parser.add_argument("--decrypt", action="store_true", help="decrypt a file from DIVAFILE")
  extract_parser = subparsers.add_parser("extract", help="extract an archive")
  extract_parser.add_argument("filepath", type=str, help="path to your file of choice")
  extract_parser.add_argument("output_dir", type=str, nargs="?", help="the output directory for archive files")
  
  args = parser.parse_args()

  if args.command == "dlt":  
    if args.write:
      if not args.entries:
        print("error: --write requires you to provide at least 1 entry.")
        sys.exit(1)
      dlt_writer = DLTWriter(args.write)
      for entry in args.entries:
       dlt_writer.add_entry(entry)
      dlt_writer.write()
      print(f"Written to {args.write}")
    
    elif args.read:
      dlt_reader = DLTReader(args.filepath)
      dlt_reader.read()
      dlt_reader.print_contents()  
  
  elif args.command == "divafile":  
    if args.encrypt:
      output_path = encrypt_divafile(args.filepath)
      print(f"encrypted {output_path}")

    elif args.decrypt:
      output_path = decrypt_divafile(args.filepath)
      print(f"decrypted {args.filepath}")
  
  elif args.command == "extract":
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
