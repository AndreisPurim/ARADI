
def rot_16(val, rot):
    '''Rotate 16 bits'''
    # Remember to put the first bits back in the end, and mask to stop overflows
    return ((val << rot) | (val >> (16 - rot))) & 0xFFFF

def rot_32(val, rot):
    '''Rotate 32 bits'''
    # Remember to put the first bits back in the end, and mask to stop overflows
    return ((val << rot) | (val >> (32 - rot))) & 0xFFFFFFFF

def phex(lst):
    '''Function to print hexadecimal lists'''
    print([hex(x) for x in lst])

def sbox(w, x, y, z):
    '''ARADI S-box'''
    # Sbox, very straightforward function
    x ^= (w & y)
    z ^= (x & y)
    y ^= (w & z)
    w ^= (x & z)
    return w, x, y, z

def linear(j, x):
    '''Aradi Linear Map'''
    # The parameters of ai, bi, and ci
    # In a future version, this does not need to be in the function
    a = [11, 10, 9, 8]
    b = [8, 9, 4, 9]
    c = [14, 11, 14, 7]
    # Get upper 16 bits, remember to do a mask to make sure python is keeping it 16 bits
    u = (x >> 16) & 0xFFFF
    # Get lower 16 bits using a mask
    l = (x & 0xFFFF)
    # Now, does the circular shifts
    s0 = rot_16(u,a[j])
    t0 = rot_16(l,a[j])
    s1 = rot_16(u,b[j])
    t1 = rot_16(l,c[j])
    u ^= s0 ^ t1
    l ^= t0 ^ s1
    # It should be noted that linear(linear(x, i), i) = x should be true
    # Use a mask of 32 bits to make sure it doesn't overflow.
    return ((u << 16) | l) & 0xFFFFFFFF

def m0(x, y):
    # M0 function, as described in the paper
    return rot_32(x, 1) ^ y, rot_32(y, 3) ^ rot_32(x,1) ^ y

def m1(x, y):
    # M1 function, as described in the paper
    return rot_32(x, 9) ^ y, rot_32(y, 28) ^ rot_32(x, 9) ^ y

def keyschedule(key, i):
    # Temporary (middle) values of the first key schedule
    t0, t1 = m0(key[0], key[1])
    t2, t3 = m1(key[2], key[3])
    t4, t5 = m0(key[4], key[5])
    t6, t7 = m1(key[6], key[7])
    ki = [t0, t2, t1, t3, t4, t6, t5, t7 ^ i]
    # Second temporary values of the key schedule
    t0, t1 = m0(ki[0], ki[1])
    t2, t3 = m1(ki[2], ki[3])
    t4, t5 = m0(ki[4], ki[5])
    t6, t7 = m1(ki[6], ki[7])
    ki2 = [t0, t4, t2, t6, t1, t5, t3, t7 ^ (i + 1)]
    # Returns k_{i} and k_{i+1}
    return ki, ki2

def roundkeys(key):
    # ERROR SHOULD BE AROUND HERE
    # Function to generate round_keys
    keys = [key]
    for i in range(1,16, 2):
        # Gets the past key, and then makes the schedule of rows i and i+1
        ki, ki2 = keyschedule(keys[i-1], i-1)
        keys.append(ki)
        keys.append(ki2)
    # Now, remembers to take the 4 blocks of each key
    new_keys = [key[:4]]
    for i in range(1 ,16, 2):
        new_keys.append(keys[i][4:])
        new_keys.append(keys[i+1][:4])
    return new_keys

def encryption_ARADI(state,key):
    # Needs to debug why this is creating subciphers other than expected
    # First subcipher checks out, the remaining don't.
    rk = roundkeys(key)
    w = state[0]
    x = state[1]
    y = state[2]
    z = state[3]
    for i in range(16):
        w = w ^ rk[i][0]
        x = x ^ rk[i][1]
        y = y ^ rk[i][2]
        z = z ^ rk[i][3]
        w,x,y,z = sbox(w,x,y,z)
        j = i% 4
        w = linear(j,w)
        x = linear(j,x)
        y = linear(j,y)
        z = linear(j,z)
    w = w ^ rk[16][0]
    x = x ^ rk[16][1]
    y = y ^ rk[16][2]
    z = z ^ rk[16][3]
    return [w, x, y, z]



def main():
    # Just testing some values for now, this should be cleaner in the next version
    key = [0x03020100,0x07060504,0x0b0a0908,0x0f0e0d0c, 0x13121110,0x17161514,0x1b1a1918,0x1f1e1d1c]
    plaintex = [0x00000000,0x00000000,0x00000000,0x00000000]
    ciphertext = encryption_ARADI(plaintex, key)
    print("Output:", end=" ")
    phex(ciphertext)
    expected_output = [0x3f09abf4, 0x00e3bd74, 0x03260def, 0xb7c53912]
    print("Expected output:", end=" ")
    phex(expected_output)


main()
