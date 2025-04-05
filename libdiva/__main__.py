import argparse
from .dlt import DLTReader,DLTWriter

def main():
    parser = argparse.ArgumentParser(description="Read and write DLT files.")
    parser.add_argument("filepath", type=str, help="Path to the DLT file")
    parser.add_argument("--write", nargs="+", help="Write to DLT file")
    args = parser.parse_args()

    if args.write:
        dlt_writer = DLTWriter(args.filepath)
        for entry in args.write:
            dlt_writer.add_entry(entry)
        dlt_writer.write()
        print(f"Written to {args.filepath}")
    else:
        dlt_reader = DLTReader(args.filepath)
        dlt_reader.read()
        dlt_reader.print_contents()


if __name__ == "__main__":
    main()