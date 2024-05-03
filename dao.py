import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from twofish import Twofish


def aes_encrypt_decrypt(file_contents, key):

    # Encrypt the plaintext
    start_time = time.time()
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(file_contents, AES.block_size))
    encrypt_time = time.time() - start_time

    # Decrypt the ciphertext
    start_time = time.time()
    decipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = unpad(decipher.decrypt(ciphertext), AES.block_size)
    decrypt_time = time.time() - start_time

    return encrypt_time, decrypt_time


def twofish_encrypt_decrypt(file_contents, key):
    
    bs = 16 #block size 16 bytes or 128 bits 
    plaintext=file_contents

    start_time = time.time()

    try:
        if len(plaintext) % bs:  # add padding
            padding = b'%' * (bs - len(plaintext) % bs)  # Ensure padding is represented as bytes
            padded_plaintext = plaintext + padding
        else:
            padded_plaintext = plaintext.encode('utf-8')  
    except:
        padded_plaintext=plaintext        

    T = Twofish(str.encode(key))
    ciphertext=b''

    for x in range(int(len(padded_plaintext)/bs)):
	    ciphertext += T.encrypt(padded_plaintext[x*bs:(x+1)*bs])
    
    encrypt_time = time.time() - start_time

    start_time = time.time()

    plaintext=b''

    for x in range(int(len(ciphertext)/bs)):
        plaintext += T.decrypt(ciphertext[x*bs:(x+1)*bs])

    decrypt_time = time.time() - start_time

    return encrypt_time, decrypt_time


def mars_encrypt_decrypt(data, key):
  """
  Encrypts and decrypts data using the MARS algorithm with a given key,
  returning encryption and decryption times.

  Args:
      data: The data to encrypt (byte array).
      key: The MARS key (list of integers representing rotation values for each byte).

  Returns:
      A tuple containing encryption time and decryption time (floats in seconds).
  """
  # Encryption
  start_time = time.time()
  blocks = [data[i:i+16] for i in range(0, len(data), 16)]
  encrypted_blocks = []
  for block in blocks:
    block += bytearray([0] * (16 - len(block)))
    encrypted_block = bytearray(block)
    for i in range(16):
      encrypted_block[i] = (encrypted_block[i] + key[i]) % 256
    encrypted_blocks.append(encrypted_block)
  ciphertext = b''.join(encrypted_blocks)
  encrypt_time = time.time() - start_time

  # Decryption
  start_time = time.time()
  blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
  decrypted_blocks = []
  for block in blocks:
    decrypted_block = bytearray(block)
    for i in range(16):
      decrypted_block[i] = (decrypted_block[i] - key[i]) % 256
    decrypted_blocks.append(decrypted_block)
  decrypted_data = b''.join(decrypted_blocks)
  decrypted_data = decrypted_data[:-decrypted_data.count(0)]
  decrypt_time = time.time() - start_time

  return encrypt_time, decrypt_time