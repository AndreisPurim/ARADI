"""Simple auxiliary and bit manipulation functions for aradi encryption"""

from Crypto import Random


def rotate(val, rot, bits):
    """Generic rotate function for n-bits"""
    return ((val << rot) | (val >> (bits - rot))) & ((1 << bits) - 1)


def xor_bytes(data1, data2):
    """XOR two byte arrays."""
    return bytes([b1 ^ b2 for b1, b2 in zip(data1, data2)])


def int_to_bytes(value, length):
    """Convert an integer to a byte array of specified length."""
    return value.to_bytes(length, byteorder="big")


def generate_nonce(size=8):
    """Generates a nonce (number used once)"""
    return Random.get_random_bytes(
        size
    )  # Use pycryptodome's get_random_bytes for cryptographic safety


def pkcs7_pad(data, block_size=16):
    """
    Add PKCS#7 padding to the data to make its length a multiple of the block_size.
    """
    pad_len = block_size - (len(data) % block_size)
    padding = bytes([pad_len] * pad_len)
    return data + padding


def pkcs7_unpad(padded_data, block_size=16):
    """
    Remove PKCS#7 padding from the data.
    """
    pad_len = padded_data[-1]  # The value of the last byte gives the padding length
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("Invalid padding length")

    # Check if all padding bytes are the same
    if padded_data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid padding")

    return padded_data[:-pad_len]
