import json
import sys
import os
import time
import hashlib
from collections import defaultdict


def is_image(file):
    fileidentifier = file.lower()
    return fileidentifier.endswith(".png") or fileidentifier.endswith(".jpg") or \
        fileidentifier.endswith(".jpeg") or '.jpg' in fileidentifier \


def cryptohashingfunction(file):
    sha256 = hashlib.sha256()
    hashverification = is_image(file)
    if hashverification:
        with open(file, 'rb') as fi:
            while True:
                data = fi.read()
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    else:
        raise TypeError("The selected file is not an acceptable file type. Only .png, .jpg, and .jpeg are allowed.")
        

comparison_hash = cryptohashingfunction(file)
filename1 = 'hashdictionary.json'
hashesdict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))


if os.path.isfile(filename1):
    with (open(filename1)) as openfile:
        while True:
            try:
                hashesdict.update(json.load(openfile))
                break
            except EOFError:
                break


def match(comparison_hash):
    matching_hash = comparison_hash
    try:
        match_decision = find_matching_hash(hashesdict, matching_hash)
    except ValueError:
        return None
    return match_decision


def find_matching_hash(hashesdict, matching_hash):
    count1 = 0
    for j in range(len(hashesdict["Hashmap"]['Hashes']['Hash'])):
        if matching_hash == hashesdict["Hashmap"]['Hashes']['Hash'][j]:
            return True
        else:
            count1 = count1 + 1
    if count1 == len(hashesdict["Hashmap"]['Hashes']['Hash']):
        return False


matcher = match(comparison_hash)


def items_in(d):
    items = []
    if isinstance(d, list):
        items.extend(d)
    elif isinstance(d, dict):
        for k, v in d.items():
            res.extend([k] * len(items_in(v)))
    else:
        raise ValueError('Unknown data')
    return items

def sendhashinfo(hashesdict):
    if matcher is False:
        print("The image hash cannot be found in the dictionary.")
        print("Adding hash to dictionary...please wait for 5 seconds")
        hashesdict['Hashmap']['Hashes']['Hash'].append(comparison_hash)
        time.sleep(5)
        while True:
            decision2 = input("Would you like to add info about this image?")
            if decision2.strip().lower() == "yes":
                info2 = input("Please provide additional info about the image: ")
                print("Adding info to dictionary...")
                hashesdict['Hashmap']['Hashes']['Info'].append(info2)
                time.sleep(3)
                return hashesdict['Hashmap']['Hashes']['Info'].append(info2)

            elif decision2.strip().lower() == "no":
                hashesdict['Hashmap']['Hashes']['Info'].append("None")
                return "No additional info will be added. Hash successfully added to dictionary."

    else:
        proof = items_in(hashesdict['Hashmap']['Hashes']['Hash'])
        length = len(proof)
        for i in range(length):
            if comparison_hash != proof[i]:
                continue
            else:
                print("The requested hash has been found in the dictionary.")
                print("Sending info about the image correlated to the hash...")
                if hashesdict['Hashmap']['Hashes']['Info'][i] == "None":
                    print("There seems to be no information about this hash.")
                    decision = input("Would you like to give information about this hash?")
                    if decision.strip().lower() == "yes":
                        info = input("Please provide additional info about the image: ")
                        hashesdict['Hashmap']['Hashes']['Info'][i] = info
                        return hashesdict['Hashmap']['Hashes']['Info'][i]

                    else:
                        return "No additional info will be added."
                else:
                    return hashesdict['Hashmap']['Hashes']['Info'][i]


with open(filename1, 'w') as f:
    json.dump(updatedhashdict, f)
