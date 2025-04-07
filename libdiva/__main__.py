import argparse
from .dlt import DLTReader, DLTWriter
from .divafile import encrypt_divafile, decrypt_divafile

def main():
    parser = argparse.ArgumentParser(description="Read and write various Project Diva files.")
    parser.add_argument("filepath", type=str, help="Path to the DLT file")
    parser.add_argument("--write", nargs="+", help="Write to DLT file")
    parser.add_argument("--encrypt", action="store_true", help="Encrypt a file using DIVAFILE")
    parser.add_argument("--decrypt", action="store_true", help="Decrypt a file using DIVAFILE")
    args = parser.parse_args()

    if args.write:
        dlt_writer = DLTWriter(args.filepath)
        for entry in args.write:
            dlt_writer.add_entry(entry)
        dlt_writer.write()
        print(f"Written to {args.filepath}")
    
    elif args.encrypt:
        with open(args.filepath, "rb") as file:
            input_data = file.read()
        output_path = encrypt_divafile(input_data, args.filepath)
        print(f"Encrypted: {output_path}")

    elif args.decrypt:
        output_path = decrypt_divafile(args.filepath)
        print(f"Decrypted {args.filepath}")

    else:
        dlt_reader = DLTReader(args.filepath)
        dlt_reader.read()
        dlt_reader.print_contents()

if __name__ == "__main__":
    main()