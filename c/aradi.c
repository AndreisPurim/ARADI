#include <stdio.h>
#include <stdint.h>
#include "functions.h"

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

