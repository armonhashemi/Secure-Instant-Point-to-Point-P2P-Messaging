import pyDH
import hashlib


def generate_key_pair():
    return pyDH.DiffieHellman()


def derive_shared_key(dh_key_pair, other_pubkey):
    shared_key = dh_key_pair.gen_shared_key(other_pubkey)
    hashed_shared_key = hashlib.sha256(shared_key.encode('utf-8')).digest()[:32]
    return hashed_shared_key
