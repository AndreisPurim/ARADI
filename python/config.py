# Plaintext that you want to encrypt. Each element in the list must be the word size used in ARADI, 32 bits in hexadecimal format.
plaintext = [0x00000000, 0x00000000, 0x00000000, 0x00000000]
# 256-bit key, with each element being 32 bits in hexadecimal format in each item of the list.
key = [
        0x03020100,
        0x07060504,
        0x0B0A0908,
        0x0F0E0D0C,
        0x13121110,
        0x17161514,
        0x1B1A1918,
        0x1F1E1D1C,
    ]