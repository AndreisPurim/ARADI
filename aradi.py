
def sbox(w, x, y, z):
    '''ARADI S-box'''
    x ^= (w & y)
    z ^= (x & y)
    y ^= (w & z)
    w ^= (x & z)
    return w, x, y, z

def linear(x, i):
    '''Aradi Linear Map'''
    # The parameters of ai, bi, and ci
    a = [11, 10, 9, 8]
    b = [8, 9, 4, 9]
    c = [14, 11, 14, 7]
    j = i % 4
    # Get upper 16 bits
    u = x >> 16
    # Get lower 16 bits
    l = (x & 0xFFFF)
    # Now, does the circular shifts
    u = u ^ (u << a[j]) ^ (l << c[j])
    l = l ^ (l << a[j]) ^ (u << b[j])
    # It should be noted that linear(linear(x, i), i) = x should be true
    return u | l 

def key_schedule():
    #TO DO
    pass

def main():
    #TO DO
    pass
    

    
