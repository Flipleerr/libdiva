import argparse
from .dlt import DLTReader

def main():
    parser = argparse.ArgumentParser(description="Read and print DLT files.")
    parser.add_argument("filepath", type=str, help="Path to the DLT file")
    args = parser.parse_args()

    dlt_reader = DLTReader(args.filepath)
    dlt_reader.read()
    dlt_reader.print_contents()

if __name__ == "__main__":
    main()