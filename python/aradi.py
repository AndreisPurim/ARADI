import config
import functions

def main():
    print("Input:", end="\t")
    functions.phex(config.plaintext)

    print("Key:", end="\t")
    functions.phex(config.key)

    ciphertext = functions.encryption_ARADI(config.plaintext, config.key)
    print("Output:", end="\t")
    functions.phex(ciphertext)

    deciphered = functions.decryption_ARADI(ciphertext, config.key)
    print("Dec.:", end="\t")
    functions.phex(deciphered)

if __name__ == "__main__":
    main()
