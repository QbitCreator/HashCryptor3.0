import hashlib
import random
from alive_progress import alive_bar

__hash_length = int(512/8)  # must match type of hashfunction, given in bytes
__hash_function = hashlib.blake2b
__salt_length = 32  # at least 32
__rounds = 3  # must at least be 2 rounds, more is more secure, but takes longer
__prerounds = 500000 #more takes longer, but is more secure


def bxor(ba1, ba2):
    # XOR function for bytes
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def hashchainotp(in_data, password):
    with alive_bar(__prerounds+(((len(in_data)//__hash_length)+1)*__rounds)) as bar:
        # splitting the data into chunks
        datachunks = [in_data[i:i + __hash_length]
                      for i in range(0, len(in_data), __hash_length)]

        #hashing prerounds as a "blankfiring" hashchain
        current_hash = __hash_function(password).digest()
        for i in range(__prerounds):
            current_hash = __hash_function(current_hash).digest()
            bar()
        print("Prerounds finished, working on the data now...")
        # applying the hashchain as otp to the data with multiple rounds
        for i in range(((len(in_data)//__hash_length)+1)*__rounds):
            datachunks[i % len(datachunks)] = bxor(
                current_hash, datachunks[i % len(datachunks)])
            current_hash = __hash_function(current_hash).digest()
            bar()

    # flattening the datachunks list to get the data
    out_data = b''.join(datachunks)

    return out_data


def encrypt(data, password):
    password = password.encode("utf-16")
    salt = random.randbytes(__salt_length)

    # hashchain generator
    cipherdata = salt + hashchainotp(data+salt, password+salt)

    return cipherdata


def decrypt(cipherdata, password):
    password = password.encode("utf-16")
    salt = cipherdata[:__salt_length]
    cipherdata = cipherdata[__salt_length-len(cipherdata):]

    data = hashchainotp(cipherdata, password+salt)

    salt_in_data = data[-__salt_length:]
    data = data[:len(data)-__salt_length]

    if salt == salt_in_data:
        return data
    else:
        return -1
