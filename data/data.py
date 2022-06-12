import os
from os import walk
import math
import requests
from datetime import datetime
from zipfile import ZipFile
import tldextract
import csv

from dga import corebot, simda, banjori, cryptolocker, dicrypt, kraken, locky, qakbot, ramdo

BENIGN_ALEXA_URL = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

# items from DGArchive
MAX_ITEMS_DGARCHIVE = 10 # TODO: make more

# dictionary of all used DGA domains to avoid repetitions
ALL_MALICIOUS_DOMAINS = {}


def get_benign_domains(number_of_items=False):
    filename = BENIGN_ALEXA_URL.split('/')[-1]
    # fetch zip file
    r = requests.get(BENIGN_ALEXA_URL, stream=True)
    # write zip file
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=512):
            fd.write(chunk)

    # get data from file
    archive = ZipFile(filename, 'r')
    filename_csv = filename.replace(".zip", "")

    data_raw = archive.read(filename_csv).split()

    # extract needed number of domains
    being_domains = []
    for d in data_raw:
        # exit condition
        if number_of_items:
            if len(being_domains) == number_of_items:
                break

        d = str(d).replace("'", "")
        particles = d.split(',')

        domain = particles[1]

        # extract only second level domain
        domain = tldextract.extract(domain)[1]

        if not domain or domain == "":
            continue

        being_domains.append(domain)

    # drop zip file
    os.remove(filename)

    benign_labels = ['benign']*len(being_domains)

    return being_domains, benign_labels


def get_dga_domains_self_generated():
    malicious_domains = []
    malicious_labels = []

    # items per self generated algorith
    DOMAINS_PER_ALGORITHM = 30  # TODO: make more

    # banjori
    malicious_domains += banjori.generate_domains(DOMAINS_PER_ALGORITHM)
    malicious_labels += ['banjori']*DOMAINS_PER_ALGORITHM

    # cryptolocker
    malicious_domains += cryptolocker.generate_domains(DOMAINS_PER_ALGORITHM)
    malicious_labels += ['cryptolocker']*DOMAINS_PER_ALGORITHM

    # corebot
    malicious_domains += corebot.generate_domains(DOMAINS_PER_ALGORITHM)
    malicious_labels += ['corebot']*DOMAINS_PER_ALGORITHM

    # dicrypt
    malicious_domains += dicrypt.generate_domains(DOMAINS_PER_ALGORITHM)
    malicious_labels += ['dicrypt']*DOMAINS_PER_ALGORITHM

    # kraken
    kraken_number = int(DOMAINS_PER_ALGORITHM / 2)
    kraken_domains_1 = kraken.generate_domains(kraken_number, datetime(2022, 7, 18), 'a')
    kraken_domains_2 = kraken.generate_domains(kraken_number, datetime(2022, 7, 18), 'b')
    malicious_domains += kraken_domains_1
    malicious_domains += kraken_domains_2
    malicious_labels += ['kraken']*len(kraken_domains_1)
    malicious_labels += ['kraken']*len(kraken_domains_2)

    # locky
    malicious_domains += locky.generate_domains(DOMAINS_PER_ALGORITHM, datetime(2022, 7, 18))
    malicious_labels += ['locky']*DOMAINS_PER_ALGORITHM

    # qakbot
    malicious_domains += qakbot.generate_domains(DOMAINS_PER_ALGORITHM, date=datetime(2022, 7, 18), tlds=None)
    malicious_labels += ['qakbot']*DOMAINS_PER_ALGORITHM

    # simda
    simda_domain_lengths = range(8, 25)
    simda_particle_size = int(math.ceil(max(1, DOMAINS_PER_ALGORITHM / len(simda_domain_lengths))))
    for domain_length in simda_domain_lengths:
        simda_domains = simda.generate_domains(
            simda_particle_size,
            length=domain_length,
            tld=None,
        )
        malicious_domains += simda_domains
        malicious_labels += ['simda'] * len(simda_domains)

    # ramdo
    malicious_domains += ramdo.generate_domains(DOMAINS_PER_ALGORITHM)
    malicious_labels += ['ramdo']*DOMAINS_PER_ALGORITHM

    # TODO: add more DGAs

    return malicious_domains, malicious_labels


def get_dga_domains_dgarchive():
    malicious_domains = []
    malicious_labels = []

    # get all file names
    f_names = []
    for (dirpath, dirnames, filenames) in walk('data/d_archive/'):
        f_names.extend(filenames)
        break

    for file_name in f_names:
        family_name = file_name.split('_')[0]
        d_domains = extract_dgarchive_domains(file_name)
        malicious_domains += d_domains
        malicious_labels += [family_name] * len(d_domains)

    return malicious_domains, malicious_labels


def extract_dgarchive_domains(file_name):
    malicious_domains = []
    with open('data/d_archive/' + file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(malicious_domains) >= MAX_ITEMS_DGARCHIVE:
                break

            domain = row[0]
            # drop top level domain
            domain = tldextract.extract(domain)[1]

            if not domain or domain == "":
                continue

            # check that there are no domain repetitions
            if domain in ALL_MALICIOUS_DOMAINS:
                continue
            else:
                ALL_MALICIOUS_DOMAINS[domain] = 1

            malicious_domains.append(domain)

    return malicious_domains


def get_dga_domains():
    malicious_domains = []
    malicious_labels = []

    # NOTE: not used now as the main data input is the DArchive
    # Self generated
    # s_domains, s_labels = get_dga_domains_self_generated()
    # malicious_domains += s_domains
    # malicious_labels += s_labels

    # DGArchive
    d_domains, d_labels = get_dga_domains_dgarchive()
    malicious_domains += d_domains
    malicious_labels += d_labels

    return malicious_domains, malicious_labels


def get_data():
    # get DGA domains
    malicious_domains, malicious_labels = get_dga_domains()

    # get the same number of real domains as DGA domains. Classes must be balanced.
    benign_domains, benign_labels = get_benign_domains(len(malicious_domains))

    print('---------------------')
    print('sample size')
    print('malicios', len(malicious_domains), len(malicious_labels))
    print('benign', len(benign_domains), len(benign_labels))

    if len(malicious_domains) > len(benign_domains):
        raise ValueError('Too many DGAs generated')

    all_domains = []
    all_domains += benign_domains
    all_domains += malicious_domains

    all_labels = []
    all_labels += benign_labels
    all_labels += malicious_labels

    return all_domains, all_labels


if __name__ == '__main__':
    get_data()
