import time

# rotate right input x, by n bits
def ROR(x, n, bits=32):
    mask = (2**n) - 1
    mask_bits = x & mask
    return (x >> n) | (mask_bits << (bits - n))

# rotate left input x, by n bits
def ROL(x, n, bits=32):
    return ROR(x, bits - n, bits)

# convert input sentence into blocks of binary
# creates 4 blocks of binary each of 32 bits.
def blockConverter(data):
    blocks = []
    for i in range(0, len(data), 4):
        block = data[i:i+4]
        block_int = 0
        for byte in block:
            block_int = (block_int << 8) | byte
        blocks.append(block_int)
    return blocks


# converts 4 blocks array of long int into string
def deBlocker(blocks):
    result = []
    for block in blocks:
        for i in range(4):
            result.append(block & 0xFF)
            block >>= 8
    return result

# generate key s[0... 2r+3] from given input string userkey
def generateKey(userkey):
    r = 12
    w = 32
    key_size = 128  # Key size in bits
    key_words = key_size // w  # Number of words in the key

    modulo = 2 ** w
    s = (2 * r + 4) * [0]
    s[0] = 0xB7E15163

    userkey_bytes = userkey.encode()  # Convert the user key to bytes
    # Pad or truncate the key to match the required size
    userkey_bytes = userkey_bytes[:key_words * 4] if len(userkey_bytes) > key_words * 4 else userkey_bytes.ljust(key_words * 4, b'\x00')

    # Convert the key bytes to integers
    key_words = [int.from_bytes(userkey_bytes[i:i+4], byteorder='big') for i in range(0, len(userkey_bytes), 4)]

    for i in range(1, 2 * r + 5):
        s[i] = (s[i - 1] + 0x9E3779B9) % modulo

    encoded = blockConverter(key_words)
    enlength = len(encoded)
    l = enlength * [0]
    for i in range(1, enlength + 1):
        l[enlength - i] = int(encoded[i - 1], 2)

    v = 3 * max(enlength, 2 * r + 4)
    A = B = i = j = 0

    for index in range(0, v):
        A = s[i] = ROL((s[i] + A + B) % modulo, 3, w)
        B = l[j] = ROL((l[j] + A + B) % modulo, (A + B) % w, w)
        i = (i + 1) % (2 * r + 4)
        j = (j + 1) % enlength
    return s



def rc6_encrypt_decrypt(data, s):
    start_time = time.time()

    file_data = [byte for byte in data]

    encoded = blockConverter(file_data)

    enlength = len(encoded)
    A = encoded[0]
    B = encoded[1]
    C = encoded[2]
    D = encoded[3]
    r = 12
    w = 32
    modulo = 2 ** 32
    lgw = 5
    B = (B + s[0]) % modulo
    D = (D + s[1]) % modulo
    for i in range(1, r):  # Modified loop condition
        t_temp = (B * (2 * B + 1)) % modulo
        t = ROL(t_temp, lgw, 32)
        u_temp = (D * (2 * D + 1)) % modulo
        u = ROL(u_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        A = (ROL(A ^ t, umod, 32) + s[i]) % modulo
        C = (ROL(C ^ u, tmod, 32) + s[i + 1]) % modulo
        (A, B, C, D) = (B, C, D, A)
    A = (A + s[r + 2]) % modulo
    C = (C + s[r + 3]) % modulo
    cipher = [A, B, C, D]

    encrypt_time = time.time() - start_time

    start_time = time.time()

    encoded = blockConverter(deBlocker(cipher))
    enlength = len(encoded)
    A = encoded[0]
    B = encoded[1]
    C = encoded[2]
    D = encoded[3]
    cipher = [A, B, C, D]
    r = 12
    w = 32
    modulo = 2 ** 32
    lgw = 5
    C = (C - s[r + 3]) % modulo
    A = (A - s[r + 2]) % modulo
    for j in range(1, r + 1):
        i = r + 1 - j
        (A, B, C, D) = (D, A, B, C)
        u_temp = (D * (2 * D + 1)) % modulo
        u = ROL(u_temp, lgw, 32)
        t_temp = (B * (2 * B + 1)) % modulo
        t = ROL(t_temp, lgw, 32)
        tmod = t % 32
        umod = u % 32
        C = (ROR((C - s[i + 1]) % modulo, tmod, 32) ^ u)
        A = (ROR((A - s[i]) % modulo, umod, 32) ^ t)
    D = (D - s[1]) % modulo
    B = (B - s[0]) % modulo
    orgi = [A, B, C, D]

    decrypt_time = time.time() - start_time

    return encrypt_time, decrypt_time