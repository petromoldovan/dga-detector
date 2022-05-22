# src: https://github.com/baderj/domain_generation_algorithms/blob/master/ramdo/dga.py

def dga(seed, nr, no_tld):
    s = (2 * seed * (nr + 1))
    r = s ^ (26 * seed * nr)
    domain = ""
    for i in range(16):
        r = r & 0xFFFFFFFF
        domain += chr(r % 26 + ord('a'))
        r += (r ^ (s * i ** 2 * 26))

    if not no_tld:
        domain += ".org"

    return domain


def generate_domains(number_of_items, no_tld=True):
    res = []
    for nr in range(number_of_items):
        res.append(dga(0xD5FFF, nr, no_tld))

    return res
