from pyaradi import aradi_core
from pyaradi import aradi_utils
import struct


def aradi_ctr_mode(message, key, nonce, initial_counter=0):
    """
    Perform ARADI encryption/decryption in CTR mode.

    This function processes the input message in 128-bit (16-byte)
    blocks, generating a keystream from the encrypted counter block,
    and XORs it with the message to produce the encrypted output.

    :param message: The plaintext or ciphertext to process (bytes).
    :param key: The ARADI encryption key (list of 8 32-bit words).
    :param nonce: A unique nonce (8 bytes) used to initialize the counter.
    :param initial_counter: The initial value for the counter (default is 0).
    :return: The encrypted or decrypted message (bytes).
    """
    block_size = 16
    encrypted_message = bytearray()
    message_len = len(message)

    for block_index in range(0, message_len, block_size):
        counter = initial_counter + (block_index // block_size)
        counter_block = nonce + aradi_utils.int_to_bytes(counter, 8)
        counter_state = struct.unpack(">4I", counter_block)
        keystream_block = struct.pack(
            ">4I", *aradi_core.aradi_encryption_block(list(counter_state), key)
        )
        message_block = message[block_index : block_index + block_size]
        encrypted_block = aradi_utils.xor_bytes(
            message_block, keystream_block[: len(message_block)]
        )
        encrypted_message.extend(encrypted_block)

    return bytes(encrypted_message)


def encrypt(message, key, mode="CTR", nonce=None, block_size=16):
    """
    Encrypt the given message using ARADI in the specified mode.

    This function handles padding and nonce generation automatically.
    By default, it uses CTR mode for encryption.

    :param message: The plaintext message to encrypt (str or bytes).
    :param key: The ARADI encryption key (list of 8 32-bit words).
    :param mode: The encryption mode to use (default is 'CTR').
    :param nonce: An optional nonce (8 bytes); if not provided, one will be generated.
    :param block_size: The size of blocks to pad the message to (default is 16 bytes).
    :return: The concatenated nonce and encrypted message (bytes).
    """
    if isinstance(message, str):
        message = message.encode("utf-8")

    padded_message = aradi_utils.pkcs7_pad(message, block_size)
    nonce = nonce or aradi_utils.generate_nonce(size=8)

    if mode == "CTR":
        encrypted_message = aradi_ctr_mode(padded_message, key, nonce)
    else:
        raise ValueError(f"Unsupported encryption mode: {mode}")

    return nonce + encrypted_message


def decrypt(ciphertext, key, mode="CTR", block_size=16):
    """
    Decrypt the given ciphertext using ARADI in the specified mode.

    This function separates the nonce from the ciphertext,
    decrypts the message using CTR mode, and removes any padding
    before returning the original plaintext.

    :param ciphertext: The encrypted message (bytes) that includes the nonce.
    :param key: The ARADI encryption key (list of 8 32-bit words).
    :param mode: The decryption mode to use (default is 'CTR').
    :param block_size: The size of blocks to unpad the message to (default is 16 bytes).
    :return: The decrypted original message (str).
    """
    if mode == "CTR":
        nonce = ciphertext[:8]
        encrypted_message = ciphertext[8:]
        decrypted_padded_message = aradi_ctr_mode(encrypted_message, key, nonce)
        return aradi_utils.pkcs7_unpad(decrypted_padded_message, block_size).decode(
            "utf-8"
        )
    else:
        raise ValueError(f"Unsupported decryption mode: {mode}")


def aradi_process_file(input_path, output_path, key, nonce):
    """
    Encrypt or decrypt a file using ARADI in CTR mode.

    This function reads the input file in 16-byte chunks, encrypts
    each chunk using the provided key and nonce, and writes the
    encrypted output to the specified output file.

    :param input_path: Path to the input file to be processed (str).
    :param output_path: Path to save the encrypted output file (str).
    :param key: The ARADI encryption key (list of 8 32-bit words).
    :param nonce: A unique nonce (8 bytes) used for encryption.
    """
    with open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
        while True:
            chunk = f_in.read(16)
            if not chunk:
                break
            encrypted_chunk = aradi_ctr_mode(chunk, key, nonce)
            f_out.write(encrypted_chunk)


def aradi_test(message, key, nonce=None):
    """
    Test the ARADI encryption and decryption process.

    This function encrypts the provided message and then decrypts
    it to verify that the original message can be successfully
    reconstructed.

    :param message: The plaintext message to encrypt and decrypt (str).
    :param key: The ARADI encryption key (list of 8 32-bit words).
    :param nonce: An optional nonce (8 bytes) for encryption; if not provided, one will be generated.
    :return: A tuple containing the encrypted message in hex and the reconstructed message (str).
    """
    encrypted_message = encrypt(message, key, nonce=nonce)
    reconstructed_message = decrypt(encrypted_message, key)
    return encrypted_message.hex(), reconstructed_message


def aradi_test_default():
    # Test functions
    key = [
        0x01234567,
        0x89ABCDEF,
        0xFEDCBA98,
        0x76543210,
        0x00112233,
        0x44556677,
        0x8899AABB,
        0xCCDDEEFF,
    ]
    nonce = b"\x12\x34\x56\x78\x90\xab\xcd\xef"

    original_message = "Example message to encrypt in CTR mode with ARADI"
    encrypted_hex, reconstructed_message = aradi_test(original_message, key, nonce)

    print("Original message:\n\t", original_message)
    print("Encrypted message (hex):\n\t", encrypted_hex)
    print("Reconstructed message after decryption:\n\t", reconstructed_message)

    # Example file processing
    # process_file('input.txt', 'output.txt', key, nonce)


if __name__ == "__main__":
    aradi_test_default()
