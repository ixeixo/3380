import json
import sys
import os
import time
import hashlib
import collections
import collections.abc


def is_image(file):
    fileidentifier = file.lower()
    return fileidentifier.endswith(".png") or fileidentifier.endswith(".jpg") or \
        fileidentifier.endswith(".jpeg") or '.jpg' in f \


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
        raise TypeError("The selected file is not an acceptable file type.")

count = 0
hashesdict = collections.defaultdict(dict)
hashesdict[f'Hash {count}']['Hash']
updatedhashdict = {'Hashes': {}}
filename1 = 'hashdictionary.json'
comparison_hash = cryptohashingfunction(file)

if os.path.isfile(filename1):
    with (open(filename1, "r+")) as openfile:
        while True:
            try:
                updatedhashdict.update(json.load(filename1))
            except EOFError:
                break
                
while count < len(hashesdict):
    if hashesdict[f'Hash {count}']['Hash'] == comparison_hash:
        print("Your hashed image has a match in our dictionary. Here is the info on this hash: ")
        if hashesdict.get(f'Hash{count}', {}).get('Info') == 'None':
            while True:
                infoaddition = input("There is no info on this image. Would you like to add additional info?")
                if infoaddition.strip() == 'yes' or 'Yes':
                    info = input("Please provide additional info about the image: ")
                    hashesdict[f'Hash {count}']['Info'] = info
                    print("Hash info successfully added to dictionary.")
                    break
                elif infoaddition.strip() == 'no' or 'No':
                    print("No additional info will be added.")
                    break
                else:
                    print("Error: Response is not valid. The following responses are valid: yes, Yes, no, No")
                    time.sleep(3)
        else:
            print(hashesdict[f'Hash {count}']['Info'])
            break

    else:
        count = count + 1

 if count == len(hashesdict):
    print("There are no matching hashes for your image within the dictionary.")
    print("Adding hash to the dictionary... please wait for 5 seconds.")
    hashesdict[f'Hash {count}']['Hash'] = comparison_hash
    time.sleep(5)
    while True:
        decision = input("Would you like to add info about this image?")
        if decision.strip() == 'yes' or 'Yes':
            info = input("Please provide additional info about the image: ")
            hashesdict[f'Hash {count}']['Info'] = info
            print("Hash and hash info successfully added to dictionary.")
            break
        elif decision.strip() == 'no' or 'No':
            print("No additional info will be provided. Hash successfully added to dictionary.")
            break
        else:
            print("Error: Response is not valid. The following responses are valid: yes, Yes, no, No")
            time.sleep(3)

with open(filename1, 'w') as f:
    json.dump(updatedhashdict, f)
