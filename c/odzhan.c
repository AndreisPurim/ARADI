/**
    Implementation by odzhan (https://github.com/odzhan) and published in his gist github
    https://gist.github.com/odzhan/a70544ad79c32c8e7d6c954de5546746

    This code belongs to odzhan, and is being used here for benchmarking comparisons.
    Check his other (very good) works on security on his github.

    -----

    ARADI and LLAMA: Low-Latency Cryptography for Memory Encryption
   
    Published in August 2024
    Only tested on little-endian CPU.
   
    For more details, see https://eprint.iacr.org/2024/1240
*/

#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

// circular shift right
#define ROR32(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define ROR16(x, n) (((x) >> (n)) | ((x) << (16 - (n))))

// swap
#define SWP(x, y) (t) = (x); (x) = (y); (y) = (t);  
        
void setkey(void *sk, void *subkeys) {
    uint32_t *ks = (uint32_t*)subkeys;
    uint32_t *K = (uint32_t*)sk;
    uint32_t t;
    
    for (int i = 0;;i++) {
        int j = (i & 1) << 2;
        
        *ks++ = K[j + 0];
        *ks++ = K[j + 1];
        *ks++ = K[j + 2];
        *ks++ = K[j + 3];

        if (i == 16) break;
        
        // linear layer
        for (int k = 0; k < 4; k++) {
            int x = (k + k);
            
            int r1 = k & 1 ? 23 : 31;
            int r2 = k & 1 ? 4 : 29;

            t = K[x + 1];

            K[x + 1] = ROR32(K[x], r1) ^ ROR32(K[x + 1], r2) ^ K[x + 1];
            K[x] = ROR32(K[x], r1) ^ t;
        }

        // add counter
        K[7] ^= i;

        // permutation
        j >>= 1;
        
        SWP(K[1], K[2 + j]);
        SWP(K[5 - j], K[6]);
    }
}

void encrypt(void *data, void *subkeys) {
    uint32_t *x = (uint32_t*)data;
    uint32_t *ks = (uint32_t*)subkeys;

    uint8_t a[4] = {5, 6,  7, 8};
    uint8_t b[4] = {8, 7, 12, 7};
    uint8_t c[4] = {2, 5,  2, 9};
    
    // for each subkey
    for (int i=0;;i++) {
        // add subkey
        for (int j=0; j<4; j++) {
            x[j] ^= *ks++;
        }

        if (i == 16) break;
        
        // non-linear layer
        x[1] ^= (x[0] & x[2]); 
        x[3] ^= (x[1] & x[2]);
        x[2] ^= (x[0] & x[3]);
        x[0] ^= (x[1] & x[3]);

        // linear layer
        for (int j=0; j<4; j++) {
            uint16_t u = x[j] >> 16;
            uint16_t l = x[j] & 0xFFFF;
            
            uint16_t t = (u ^ ROR16(u, a[i&3]) ^ ROR16(l, c[i&3]));
            l = (l ^ ROR16(l, a[i&3]) ^ ROR16(u, b[i&3]));
            
            x[j] = (t << 16) | l;
        }
    }
}

#if defined(TEST)
void bin2hex(const char *str, const void *inbuf, size_t inlen) {
    uint8_t *in = (uint8_t*)inbuf;
    
    printf("\n %-10s : ", str);
    
    for (size_t i = 0; i < inlen; i++) {
        printf(" 0x%02x", in[i]);
        if (i && !(i & 15)) putchar('\n');
    }
}

int main() {
    puts("\nARADI Block Cipher by NSA. 128-bit block, 256-bit Key\n");
    
    uint8_t pt[16]={0};
    uint8_t sk[32]={0};
    uint32_t ks[17][4]={0};
    uint32_t ct[4]={0x3f09abf4, 0x00e3bd74, 0x03260def, 0xb7c53912};
    
    // initialise secret key
    for (int i=0; i<32; i++) sk[i] = i;
    
    // create subkeys
    setkey(sk, ks);
    
    for (int i=0; i<17; i++) {
        printf("key[%2i] : %08lx %08lx %08lx %08lx\n", i, ks[i][0], ks[i][1], ks[i][2], ks[i][3]);
    }
    
    encrypt(pt, ks);
    
    bin2hex("ciphertext", pt, sizeof(pt));
    bin2hex("expected", ct, sizeof(ct));
    
    int ok = memcmp(ct, pt, sizeof(ct)) == 0;
    printf("\n\n Test %s\n", ok ? "OK" : "FAILED");
    return 0;
}

#endif
