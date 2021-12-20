def h():
    print('BINARY POLYNOMIAL ARITHMETIC')
    print('On binary polys (GF(2^n))')
    print('0b100111 -> x5 + x2 + x + 1')
    print('use [polystr(n)] for clarity')
    print('also see [to_bits(n)])')
    print('example below:')
    print('1+x+x2+x4+x6 % 1+x+x4+x5 = x')
    print('0b01010111   % 0b110011  = 1')

def p_mul(a, b):
    """ Binary polynomial multiplication (peasant). """
    result = 0
    while a and b:
        if a & 1: result ^= b
        a >>= 1; b <<= 1
    return result

def p_mod(a, b):
    """ Binary polynomial remainder / modulus.
        Divides a by b and returns resulting remainder polynomial.
        Precondition: b != 0 """
    bl = b.bit_length()
    while True:
        shift = a.bit_length() - bl
        if shift < 0: return a
        a ^= b << shift

def p_exp(a, exponent):
    """ Binary polynomial exponentiation by squaring (iterative).
        Returns polynomial `a` multiplied by itself `exponent` times.
        Precondition: exponent >= 0
        Precondition: not (x == 0 and exponent == 0) """
    factor = a; result = 1
    while exponent:
        if exponent & 1: result = p_mul(result, factor)
        factor = p_mul(factor, factor)
        exponent >>= 1
    return result

def p_gcd(a, b):
    """ Binary polynomial euclidean algorithm (iterative).
        Returns the Greatest Common Divisor of polynomials a and b. """
    while b: a, b = b, p_mod(a, b)
    return a

def p_egcd(a, b):
    """ Binary polynomial Extended Euclidean algorithm (iterative).
        Returns (d, x, y) where d is the Greatest Common Divisor of polynomials a and b.
        x, y are polynomials that satisfy: p_mul(a,x) ^ p_mul(b,y) = d
        Precondition: b != 0
        Postcondition: x <= p_div(b,d) and y <= p_div(a,d) """
    a = (a, 1, 0)
    b = (b, 0, 1)
    while True:
        q, r = p_divmod(a[0], b[0])
        if not r: return b
        a, b = b, (r, a[1] ^ p_mul(q, b[1]), a[2] ^ p_mul(q, b[2]))

def p_divmod(a, b):
    """ Binary polynomial division.
        Divides a by b and returns resulting (quotient, remainder) polynomials.
        Precondition: b != 0 """
    q = 0; bl = b.bit_length()
    while True:
        shift = a.bit_length() - bl
        if shift < 0: return (q, a)
        q ^= 1 << shift; a ^= b << shift

def p_mult_inv(a, modulus):
    """ Binary polynomial modular multiplicative inverse.
        Returns b so that: p_mod(p_mul(a, b), modulus) == 1
        Precondition: modulus != 0 and p_coprime(a, modulus)
        Postcondition: b < modulus """
    d, x, y = p_egcd(a, modulus)
    assert d == 1 # inverse exists
    return x

p_degree = lambda a: a.bit_length() - 1
p_congruent = lambda a, b, modulus: p_mod(a^b, modulus) == 0
p_coprime = lambda a, b: p_gcd(a, b) == 1

def to_bits(n):
    bits = set(); bit = 0
    while n:
        if n & 1: bits.add(bit)
        bit += 1; n >>= 1
    return bits

def from_bits(bits):
    n = 0
    for bit in bits: n |= 1 << bit
    return n

def polystr(n, variable="x", unicode=False, separator=" + ", constant="1"):
    sup = lambda s: "".join("⁰¹²³⁴⁵⁶⁷⁸⁹"[ord(c) & 0xF] for c in s)
    power = lambda s: variable + sup(s) if unicode else variable + "^" + s
    term = lambda bit: constant if bit == 0 else ( \
        variable if bit == 1 else power(str(bit)) )
    return separator.join(map(term, sorted(to_bits(n), reverse=True)))

bits = lambda *bits: from_bits(bits)
bit_str = lambda n, width=0: "{:b}".format(abs(n)).rjust(width, "0")