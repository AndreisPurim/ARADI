
# ARADI and LLAMA Encryption Implementations

## Overview

This repository includes many implementations of the the ARADI and LLAMA cryptographic algorithms as described in the NSA publication [ARADI and LLAMA](https://eprint.iacr.org/2024/1240). This library is designed for encrypting and decrypting messages and files securely using ARADI. The following lines will present each implementation:

**License:** This project is licensed under the MIT License.

**Contributions:** All suggestions and corrections are welcome. Please feel free to submit issues or pull requests.

**To-do:**
-   Implement LLAMA
-   Optimize the Python and C code
-   Create unit tests to verify integrity
-   Benchmark performance across different systems
- Implement in an eletronic hardware system

**Acknowledgements:** Thanks to the authors of the original ARADI and LLAMA paper for their contributions to cryptography; to Bill Buchanan and Odzhan for their C implementations (for benchmark comparisons, check the C implementation); and to Professor Julio César López Hernández (IC-UNICAMP) for introducing us to this algorithm.

# Python Library: pyaradi

```pyaradi``` is the implementation of these functions in Python, which include the following features (so far):

- ARADI encryption in CTR mode
- Encrypt and decrypt strings and files
- Automatic nonce generation
- Padding support with PKCS7
- Easy-to-use API

To install the `pyaradi` library, use pip:

```bash
pip install pyaradi
```

## Use

### Encryption

You can encrypt a message using the ```encrypt``` function. Here's an example:

```python
from pyaradi import aradi_utils, aradi_core, encrypt

# Define your key (list of 8 32-bit words)
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

message = "Hello, World!"
encrypted_message = encrypt(message, key)
print("Encrypted message (hex):", encrypted_message.hex())
```

### Decrypting a Message

To decrypt a message, use the `decrypt` function:

```python
from pyaradi import decrypt

# Assuming you have the encrypted message and the key
reconstructed_message = decrypt(encrypted_message, key)
print("Reconstructed message:", reconstructed_message)
```
### Encrypting and Decrypting Files

You can also process files with the `aradi_process_file` function:

```python
from pyaradi import aradi_process_file

input_file = 'input.txt'
output_file = 'output.txt'
nonce = aradi_utils.generate_nonce(size=8)

aradi_process_file(input_file, output_file, key, nonce)
print(f"File '{input_file}' has been encrypted to '{output_file}'.")
```

### Testing the Implementation

You can run a test to verify the encryption and decryption:

```python
from pyaradi import aradi_test

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

message = "Test message for encryption."
encrypted_hex, reconstructed_message = aradi_test(message, key)

print("Encrypted message (hex):", encrypted_hex)
print("Reconstructed message:", reconstructed_message)
```

### Contributing and Formatting

Feel free to make contributions. In order to automate the boring parts, the file ```pybash.sh``` should have all necessary functions to format, create the releases and upload the code to pip (although I'd prefer you left that to the admins). The functions are:

```chmod +x pybash.sh``` to make it executable.

```./pybash format``` to format using black and flake8.

```./pybash create_dist``` to create the dist packages.

```./pybash test_upload``` to test the upload to test.pypi.org

For the test uploads, create/configure the ```$HOME/.pypirc```  as:

```
[distutils]
index-servers=
pypi
testpypi
[pypi]
repository = https://upload.pypi.org/legacy/
username = <username>
password = <api-key starting with pypi-...>

[testpypi]
repository = https://test.pypi.org/legacy/
username = <username>
password = <api-key starting with pypi-...>
```
Be aware that your test.pypi and pypi are different "organizations" with different usernames and api-keys. You need to create an account on both.



