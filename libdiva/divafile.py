"""DIVAFILE encryption and decryption module"""
from Crypto.Cipher import AES

DIVA_MAGIC = b"DIVAFILE"
DIVA_KEY = b"file access deny"
HEADER_SIZE = 16 # 8 bytes for magic, 4 bytes for LEN_PAYLOAD and 4 bytes for LEN_PLAINTEXT

def pad_data(data: bytes):
  """pads data to be a multiple of 16 bytes"""
  block_size = 16
  pad_len = block_size - (len(data) % block_size)
  padded_data = data + (b"\x00" * pad_len)
  return padded_data, len(padded_data)

def encrypt_divafile(filepath):
  """encrypt a file using DIVAFILE""" 
  with open(filepath, 'rb') as f:
    input_data = f.read()

  cipher = AES.new(DIVA_KEY, AES.MODE_ECB)

  padded_data, len_payload = pad_data(input_data)
  len_plaintext = len(input_data)

  print(f"info: input data length: {len(input_data)}")
  print(f"info: padded data length: {len(padded_data)}")

  encrypted_data = cipher.encrypt(padded_data)
  print(f"info: encrypted data length: {len(encrypted_data)}")

  output_path = filepath + ".txt"

  header = (
    DIVA_MAGIC +
    len_payload.to_bytes(4, 'little') +
    len_plaintext.to_bytes(4, 'little')
  )

  with open(output_path, "wb") as f:
    f.write(header + encrypted_data)

  return output_path

def decrypt_divafile(filepath):
  """decrypt a file from DIVAFILE"""
  with open(filepath, "rb") as f:
    encrypted_data = f.read()

  if encrypted_data[:8] != DIVA_MAGIC:
    raise ValueError("Not a valid DIVAFILE")

  len_payload = int.from_bytes(encrypted_data[8:12], 'little')
  len_plaintext = int.from_bytes(encrypted_data[12:16], 'little')

  print("info: contents of len_payload: ", len_payload)
  print("info: contents of len_plaintext: ", len_plaintext)

  cipher = AES.new(DIVA_KEY, AES.MODE_ECB)

  encrypted_payload = encrypted_data[HEADER_SIZE:HEADER_SIZE + len_payload]
  decrypted_payload = cipher.decrypt(encrypted_payload)

  # to be honest, this implementation is stupid, but hey it works!
  if filepath.endswith('.txt'):
    output_path = filepath[:-4] + '_decrypted.txt'
  else:
    output_path = filepath[:-4] + '_decrypted.txt'

  with open(output_path, "wb") as f:
    f.write(decrypted_payload[:len_plaintext])

  return output_path
