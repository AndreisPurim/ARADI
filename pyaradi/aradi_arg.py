"""Simple functions to encrypt and decrypt from the command line"""

import argparse
from pyaradi import aradi_core


def _parse_args():
    """
    Parse command-line arguments for the ARADI encryption/decryption script.
    """
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt a message using ARADI cipher."
    )

    parser.add_argument(
        "operation",
        choices=["encrypt", "decrypt"],
        help="Operation: encrypt or decrypt the message.",
    )
    parser.add_argument("message", help="The message to encrypt or decrypt.")
    parser.add_argument(
        "--key",
        required=True,
        help="Encryption key as a comma-separated list of 8 integers.",
    )
    parser.add_argument(
        "--mode",
        default="CTR",
        choices=["CTR"],
        help="Encryption mode (currently only CTR is supported).",
    )
    parser.add_argument(
        "--nonce", help="Optional nonce (hex) to use for encryption or decryption."
    )
    parser.add_argument(
        "--block-size",
        type=int,
        default=16,
        help="Block size for encryption (default is 16).",
    )

    return parser.parse_args()


def main():
    # Parse command-line arguments
    args = _parse_args()

    # Convert the key from a comma-separated list of integers
    key = [int(k, 16) if "0x" in k else int(k) for k in args.key.split(",")]

    # Handle the message
    message = args.message

    # Handle nonce if provided, convert hex to bytes
    nonce = bytes.fromhex(args.nonce) if args.nonce else None

    if args.operation == "encrypt":
        ciphertext = aradi_core.encrypt(
            message, key, mode=args.mode, nonce=nonce, block_size=args.block_size
        )
        print(f"Encrypted Message (hex): {ciphertext.hex()}")

    elif args.operation == "decrypt":
        ciphertext = bytes.fromhex(message)
        decrypted_message = aradi_core.decrypt(
            ciphertext, key, mode=args.mode, block_size=args.block_size
        )
        print(f"Decrypted Message: {decrypted_message}")


if __name__ == "__main__":
    main()
