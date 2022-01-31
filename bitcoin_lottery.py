'''
Created on Dec 5, 2020

@author: Edoz
'''

from bit import Key, base58, crypto
from datetime import datetime 
from multiprocessing import Process
from threading import Thread
import os, copy, sys

def load_addresses(filepath='./addresses.txt'):
    print('Loading target addresses')
    with open(filepath) as f:
        return set([x.strip() for x in f.read().splitlines() if not x.startswith('bc')])

def load_addresses_and_decode(filepath='./addresses.txt'):
    set_addresses = load_addresses(filepath)
    return decode_addresses(segregate_addresses(set_addresses))

def segregate_addresses(mixed_set_addresses):
    legacy_set = []
    segwit_set = []
    bech_set = []
    for addr in mixed_set_addresses:
        if addr.startswith('1'):
            legacy_set.append(addr)
        elif addr.startswith('3'):
            segwit_set.append(addr)
        elif addr.startswith('bc'):
            bech_set.append(addr)
    return [set(legacy_set), set(segwit_set), set(bech_set)]

def decode_addresses(segregated_set_addresses):
    legacy_set = []
    segwit_set = []
    #bech_set = []
    for addr in segregated_set_addresses[0]:
        legacy_set.append(decode_legacy_or_segwit_address_nochecksum(addr))
    for addr in segregated_set_addresses[1]:
        segwit_set.append(decode_legacy_or_segwit_address_nochecksum(addr))
    return set(legacy_set).union(set(segwit_set))

def decode_legacy_or_segwit_address_nochecksum(legacy_address):
    no_version = legacy_address[1:]
    decoded = base58.b58decode(no_version)
    shortened = decoded[:-4]
    return shortened

def check_if_found_decoded(key, decoded_set_addresses):
    legacyhash = crypto.ripemd160_sha256(key.public_key)
    return (legacyhash in decoded_set_addresses)

def save_found_key(key):
    pk_wif = key.to_wif()
    print('Collision found: {}'.format(pk_wif))
    fname = './%s.txt' % key.address
    try:
        with open(fname,'w') as f:
            f.write(pk_wif)
        while True:
            pass
    except Exception as e:
        print('Could not write pkey {} to file. Trying again.'.format(pk_wif))
        with open('./found.txt','w'):
            f.write(pk_wif)
        while True:
            pass

def brute_force_withtimer_no_checksum(decoded_set_addresses, check = 10**5):
    #godspeed, brother
    counter = 0
    start_time = datetime.now()
    while 1:
        key = Key()
        if check_if_found_decoded(key, decoded_set_addresses):
            save_found_key(key)
        counter+=1
        if counter > check:
            time_diff = (datetime.now() - start_time).total_seconds()
            start_time = datetime.now()
            print('{} , Hash rate: {:.2f} hk cycles per min'.format(os.getpid(),60/time_diff))
            #reset
            counter = 0

def main_multiprocess_nochecksum(n_processes=2):
    print('Starting brute force multiprocess, #processes: {}'.format(n_processes))
    decoded_set_addresses = load_addresses_and_decode()
    for i in range(0,n_processes):
        p = Process(target=brute_force_withtimer_no_checksum,args=(copy.deepcopy(decoded_set_addresses),))
        p.start()

if __name__ == '__main__':
    print('Welcome to the BTC collision lottery. Good luck.')
    n_processes = 1
    if len(sys.argv) > 1:
        n_processes = int(sys.argv[1])
        print('Now loading with {} processes'.format(n_processes))
    main_multiprocess_nochecksum(n_processes)