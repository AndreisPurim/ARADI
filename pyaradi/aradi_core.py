"""Core ARADI functions, such as sbox, linear map, keyschedule and basic encryption and decryption blocks"""

from pyaradi import aradi_utils


def sbox(w, x, y, z):
    """ARADI S-box"""
    x ^= w & y
    z ^= x & y
    y ^= w & z
    w ^= x & z
    return w, x, y, z


def sbox_inverse(w, x, y, z):
    """Inverse ARADI S-box"""
    w ^= x & z
    y ^= w & z
    z ^= x & y
    x ^= w & y
    return w, x, y, z


def linear(j, x):
    """ARADI Linear Map"""
    a = [11, 10, 9, 8]
    b = [8, 9, 4, 9]
    c = [14, 11, 14, 7]

    u = (x >> 16) & 0xFFFF  # Upper 16 bits
    l = x & 0xFFFF  # Lower 16 bits

    s0 = aradi_utils.rotate(u, a[j], 16)
    t0 = aradi_utils.rotate(l, a[j], 16)
    s1 = aradi_utils.rotate(u, b[j], 16)
    t1 = aradi_utils.rotate(l, c[j], 16)

    u ^= s0 ^ t1
    l ^= t0 ^ s1

    return ((u << 16) | l) & 0xFFFFFFFF


def m0(x, y):
    """M0 function"""
    return (
        aradi_utils.rotate(x, 1, 32) ^ y,
        aradi_utils.rotate(y, 3, 32) ^ aradi_utils.rotate(x, 1, 32) ^ y,
    )


def m1(x, y):
    """M1 function"""
    return (
        aradi_utils.rotate(x, 9, 32) ^ y,
        aradi_utils.rotate(y, 28, 32) ^ aradi_utils.rotate(x, 9, 32) ^ y,
    )


def keyschedule(key, i):
    """Generate key schedule for rounds i and i+1"""
    t0, t1 = m0(key[0], key[1])
    t2, t3 = m1(key[2], key[3])
    t4, t5 = m0(key[4], key[5])
    t6, t7 = m1(key[6], key[7])

    ki = [t0, t2, t1, t3, t4, t6, t5, t7 ^ i]

    t0, t1 = m0(ki[0], ki[1])
    t2, t3 = m1(ki[2], ki[3])
    t4, t5 = m0(ki[4], ki[5])
    t6, t7 = m1(ki[6], ki[7])

    ki2 = [t0, t4, t2, t6, t1, t5, t3, t7 ^ (i + 1)]

    return ki, ki2


def roundkeys(key):
    """Generate all round keys"""
    keys = [key]

    for i in range(1, 16, 2):
        ki, ki2 = keyschedule(keys[i - 1], i - 1)
        keys.append(ki)
        keys.append(ki2)

    new_keys = [key[:4]]
    for i in range(1, 16, 2):
        new_keys.append(keys[i][4:])
        new_keys.append(keys[i + 1][:4])

    return new_keys


def aradi_encryption_block(state, key):
    """ARADI Encryption block"""
    rk = roundkeys(key)
    w, x, y, z = state

    for i in range(16):
        w ^= rk[i][0]
        x ^= rk[i][1]
        y ^= rk[i][2]
        z ^= rk[i][3]

        w, x, y, z = sbox(w, x, y, z)

        j = i % 4
        w = linear(j, w)
        x = linear(j, x)
        y = linear(j, y)
        z = linear(j, z)

    w ^= rk[16][0]
    x ^= rk[16][1]
    y ^= rk[16][2]
    z ^= rk[16][3]

    return [w, x, y, z]


def aradi_decryption_block(state, key):
    """ARADI Decryption block"""
    rk = roundkeys(key)
    w, x, y, z = state

    w ^= rk[16][0]
    x ^= rk[16][1]
    y ^= rk[16][2]
    z ^= rk[16][3]

    for i in range(15, -1, -1):
        j = i % 4

        w = linear(j, w)
        x = linear(j, x)
        y = linear(j, y)
        z = linear(j, z)

        w, x, y, z = sbox_inverse(w, x, y, z)

        w ^= rk[i][0]
        x ^= rk[i][1]
        y ^= rk[i][2]
        z ^= rk[i][3]

    return [w, x, y, z]


if __name__ == "__main__":
    # Example of inputs in the published NSA paper
    print("Example of inputs in the published NSA paper")

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
    plaintex = [0x00000000, 0x00000000, 0x00000000, 0x00000000]
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

    # Function to print a hexadecimal list
    phex = lambda x: str([hex(i) for i in x])

    print(f"Input: \t{phex(plaintex)}")

    ciphertext = aradi_encryption_block(plaintex, key)
    print(f"Enc.: \t{phex(ciphertext)}")

    deciphered = aradi_decryption_block(ciphertext, key)
    print(f"Dec.: \t{phex(deciphered)}")
