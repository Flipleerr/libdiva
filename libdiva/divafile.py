from Crypto.Cipher import AES

DIVA_MAGIC = b"DIVAFILE"
DIVA_KEY = b"file access deny"
HEADER_SIZE = 16 # 8 bytes for magic, 4 bytes for LEN_PAYLOAD and 4 bytes for LEN_PLAINTEXT

def pad_data(data: bytes):
    block_size = 16
    pad_len = block_size - (len(data) % block_size)
    padded_data = data + (b"\x00" * pad_len)  # Use simple null padding
    return padded_data, len(padded_data)

def encrypt_divafile(input_data, filepath):
    cipher = AES.new(DIVA_KEY, AES.MODE_ECB)

    padded_data, len_payload = pad_data(input_data)
    len_plaintext = len(input_data)

    print(f"Info: Input data length: {len(input_data)}")
    print(f"Info: Padded data length: {len(padded_data)}")

    encrypted_data = cipher.encrypt(padded_data)
    print(f"Info: Encrypted data length: {len(encrypted_data)}")

    output_path = filepath + ".txt"

    header = (
        DIVA_MAGIC +
        len_payload.to_bytes(4, 'little') +
        len_plaintext.to_bytes(4, 'little')
    )

    with open(output_path, "wb") as f:
        f.write(header + encrypted_data)

    return output_path

def decrypt_divafile(encrypted_data):
  cipher = AES.new(DIVA_KEY, AES.MODE_ECB)

  if encrypted_data[:8] != DIVA_MAGIC:
    raise ValueError("Invalid DIVA file magic number")

  len_payload = int.from_bytes(encrypted_data[8:12], 'little')
  len_plaintext = int.from_bytes(encrypted_data[12:16], 'little')

  encrypted_payload = encrypted_data[HEADER_SIZE:HEADER_SIZE + len_payload]
  decrypted_payload = cipher.decrypt(encrypted_payload)

  return decrypted_payload[:len_plaintext]

