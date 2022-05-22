# source: https://github.com/baderj/domain_generation_algorithms/blob/master/banjori/dga.py
def map_to_lowercase_letter(s):
    return ord('a') + ((s - ord('a')) % 26)


def next_domain(domain):
    dl = [ord(x) for x in list(domain)]
    dl[0] = map_to_lowercase_letter(dl[0] + dl[3])
    dl[1] = map_to_lowercase_letter(dl[0] + 2*dl[1])
    dl[2] = map_to_lowercase_letter(dl[0] + dl[2] - 1)
    dl[3] = map_to_lowercase_letter(dl[1] + dl[2] + dl[3])
    return ''.join([chr(x) for x in dl])


def generate_domains(number_of_items, seed='htereisaniceseed.com'):
    res = []

    for i in range(number_of_items):
        seed = next_domain(seed)
        res.append(seed)

    return res
