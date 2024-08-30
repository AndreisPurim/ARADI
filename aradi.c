#include <stdio.h>
#include <stdint.h>

// Utility Functions

uint16_t rotate16(uint16_t val, int rot) {
    return ((val << rot) | (val >> (16 - rot))) & 0xFFFF;
}

uint32_t rotate32(uint32_t val, int rot) {
    return ((val << rot) | (val >> (32 - rot))) & 0xFFFFFFFF;
}

void print_hex(uint32_t* arr, int len) {
    for (int i = 0; i < len; i++) {
        printf("0x%x ", arr[i]);
    }
    printf("\n");
}

// S-box Functions

void sbox(uint32_t* w, uint32_t* x, uint32_t* y, uint32_t* z) {
    *x ^= (*w & *y);
    *z ^= (*x & *y);
    *y ^= (*w & *z);
    *w ^= (*x & *z);
}

void sbox_inverse(uint32_t* w, uint32_t* x, uint32_t* y, uint32_t* z) {
    *w ^= (*x & *z);
    *y ^= (*w & *z);
    *z ^= (*x & *y);
    *x ^= (*w & *y);
}

// Linear Map Functions

uint32_t linear(int j, uint32_t x) {
    int a[4] = {11, 10, 9, 8};
    int b[4] = {8, 9, 4, 9};
    int c[4] = {14, 11, 14, 7};
    
    uint16_t u = (x >> 16) & 0xFFFF;
    uint16_t l = x & 0xFFFF;
    
    uint16_t s0 = rotate16(u, a[j]);
    uint16_t t0 = rotate16(l, a[j]);
    uint16_t s1 = rotate16(u, b[j]);
    uint16_t t1 = rotate16(l, c[j]);
    
    u ^= s0 ^ t1;
    l ^= t0 ^ s1;
    
    return ((u << 16) | l) & 0xFFFFFFFF;
}

// M0 and M1 Functions

void m0(uint32_t x, uint32_t y, uint32_t* out1, uint32_t* out2) {
    *out1 = rotate32(x, 1) ^ y;
    *out2 = rotate32(y, 3) ^ rotate32(x, 1) ^ y;
}

void m1(uint32_t x, uint32_t y, uint32_t* out1, uint32_t* out2) {
    *out1 = rotate32(x, 9) ^ y;
    *out2 = rotate32(y, 28) ^ rotate32(x, 9) ^ y;
}

// Key Schedule Functions

void keyschedule(uint32_t* key, int i, uint32_t* ki, uint32_t* ki2) {
    uint32_t t0, t1, t2, t3, t4, t5, t6, t7;
    
    m0(key[0], key[1], &t0, &t1);
    m1(key[2], key[3], &t2, &t3);
    m0(key[4], key[5], &t4, &t5);
    m1(key[6], key[7], &t6, &t7);
    
    ki[0] = t0; ki[1] = t2; ki[2] = t1; ki[3] = t3;
    ki[4] = t4; ki[5] = t6; ki[6] = t5; ki[7] = t7 ^ i;
    
    m0(ki[0], ki[1], &t0, &t1);
    m1(ki[2], ki[3], &t2, &t3);
    m0(ki[4], ki[5], &t4, &t5);
    m1(ki[6], ki[7], &t6, &t7);
    
    ki2[0] = t0; ki2[1] = t4; ki2[2] = t2; ki2[3] = t6;
    ki2[4] = t1; ki2[5] = t5; ki2[6] = t3; ki2[7] = t7 ^ (i + 1);
}

void roundkeys(uint32_t* key, uint32_t round_keys[17][4]) {
    uint32_t keys[17][8];
    
    // Initial key
    for (int i = 0; i < 8; i++) {
        keys[0][i] = key[i];
    }
    
    // Generate round keys
    for (int i = 1; i < 16; i += 2) {
        keyschedule(keys[i - 1], i - 1, keys[i], keys[i + 1]);
    }
    
    // Extract 4 blocks for each round key
    for (int i = 0; i < 17; i++) {
        for (int j = 0; j < 4; j++) {
            round_keys[i][j] = (i == 0) ? key[j] : keys[i][j + (i % 2 == 0 ? 0 : 4)];
        }
    }
}

// Encryption and Decryption Functions

void encryption_ARADI(uint32_t* state, uint32_t* key, uint32_t* out) {
    uint32_t round_keys[17][4];
    roundkeys(key, round_keys);
    
    uint32_t w = state[0];
    uint32_t x = state[1];
    uint32_t y = state[2];
    uint32_t z = state[3];
    
    for (int i = 0; i < 16; i++) {
        w ^= round_keys[i][0];
        x ^= round_keys[i][1];
        y ^= round_keys[i][2];
        z ^= round_keys[i][3];
        
        sbox(&w, &x, &y, &z);
        
        int j = i % 4;
        w = linear(j, w);
        x = linear(j, x);
        y = linear(j, y);
        z = linear(j, z);
    }
    
    w ^= round_keys[16][0];
    x ^= round_keys[16][1];
    y ^= round_keys[16][2];
    z ^= round_keys[16][3];
    
    out[0] = w;
    out[1] = x;
    out[2] = y;
    out[3] = z;
}

void decryption_ARADI(uint32_t* state, uint32_t* key, uint32_t* out) {
    uint32_t round_keys[17][4];
    roundkeys(key, round_keys);
    
    uint32_t w = state[0];
    uint32_t x = state[1];
    uint32_t y = state[2];
    uint32_t z = state[3];
    
    w ^= round_keys[16][0];
    x ^= round_keys[16][1];
    y ^= round_keys[16][2];
    z ^= round_keys[16][3];
    
    for (int i = 15; i >= 0; i--) {
        int j = i % 4;
        
        w = linear(j, w);
        x = linear(j, x);
        y = linear(j, y);
        z = linear(j, z);
        
        sbox_inverse(&w, &x, &y, &z);
        
        w ^= round_keys[i][0];
        x ^= round_keys[i][1];
        y ^= round_keys[i][2];
        z ^= round_keys[i][3];
    }
    
    out[0] = w;
    out[1] = x;
    out[2] = y;
    out[3] = z;
}

// Main Function

int main() {
    uint32_t key[8] = {0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c, 
                       0x13121110, 0x17161514, 0x1b1a1918, 0x1f1e1d1c};
    uint32_t plaintext[4] = {0x00000000, 0x00000000, 0x00000000, 0x00000000};
    uint32_t ciphertext[4], deciphered[4];
    
    printf("Input:\t");
    print_hex(plaintext, 4);
    
    encryption_ARADI(plaintext, key, ciphertext);
    printf("Output:\t");
    print_hex(ciphertext, 4);
    
    decryption_ARADI(ciphertext, key, deciphered);
    printf("Dec.:\t");
    print_hex(deciphered, 4);
    
    return 0;
}

