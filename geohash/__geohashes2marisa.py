import marisa_trie
import sys
import psutil
import json
import os


def main(args=None):
    directory = args[1] if len(args) > 1 else "."
    values = list()
    for file in os.listdir(directory):
        if file.endswith(".json"):
            label = os.path.basename(file).split('.')[0].encode('utf-8').strip()
            with open(os.path.join(directory, file)) as data_file:
                print("Importing - {0: <255s}".format(
                    file,
                ), end="\r", flush=True)
                hashcodes = json.load(data_file)
            values.extend([(hashcode, label) for hashcode in hashcodes])

    print("Building trie...{0: <255s}".format(""), flush=True)
    trie = marisa_trie.BytesTrie(values)

    directory_name = os.path.basename(os.path.abspath(directory))
    trie.save(args[2] if len(args) > 2 else "{0:s}.marisa".format(directory_name))
    print("done.")
    return trie


if __name__ == "__main__":
    trie = main(sys.argv)
