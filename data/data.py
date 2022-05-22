import os
import math
import requests
from datetime import datetime
from zipfile import ZipFile
import tldextract

from dga import corebot, simda, banjori, cryptolocker, dicrypt, kraken, locky, qakbot, ramdo

BENING_ALEXA_URL = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'


def get_bening_domains(number_of_items=1000):
    filename = BENING_ALEXA_URL.split('/')[-1]
    # fetch zip file
    r = requests.get(BENING_ALEXA_URL, stream=True)
    # write zip file
    with open(filename, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=512):
            fd.write(chunk)

    # get data from file
    archive = ZipFile(filename, 'r')
    filename_csv = filename.replace(".zip", "")
    data_raw = archive.read(filename_csv).split()[:number_of_items]

    # extract needed number of domains
    being_domains = []
    for d in data_raw:
        d = str(d).replace("'", "")
        particles = d.split(',')

        domain = particles[1]

        # extract only second level domain
        domain = tldextract.extract(domain)[1]
        being_domains.append(domain)

    # drop zip file
    os.remove(filename)

    bening_labels = ['bening']*number_of_items

    return being_domains, bening_labels


def get_dga_domains():
    DOMAINS_PER_ALGORITHM = 30

    malicious_domains = []
    malicious_labels = []

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


def get_data():
    # get DGA domains
    malicious_domains, malicious_labels = get_dga_domains()

    # get the same number of real domains as DGA domains. Classes must be balanced.
    bening_domains, bening_labels = get_bening_domains(len(malicious_domains))

    all_domains = []
    all_domains += bening_domains
    all_domains += malicious_domains

    all_labels = []
    all_labels += bening_labels
    all_labels += malicious_labels

    print ("all_domains", all_domains)
    print ("all_labels", all_labels)

    return all_domains, all_labels


get_data()
