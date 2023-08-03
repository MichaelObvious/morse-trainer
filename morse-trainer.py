#!/bin/python3

import random
from sys import argv, exit
from time import time

MAX_LEN = 5

def slurp_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def split_to_tokens(content: str) -> list[str]:
    blank_chars = "\t\n\r"
    for c in blank_chars:
        content = content.replace(c, ' ')
    return list(filter(lambda x: len(x) > 0, content.split(' ')))

LETTERS_TO_MC = {
    'A': '.-/',
    'B': '-.../',
    'C': '-.-./',
    'D': '-../',
    'E': './',
    'F': '..-./',
    'G': '--./',
    'H': '..../',
    'I': '../',
    'J': '.---/',
    'K': '-.-/',
    'L': '.-../',
    'M': '--/',
    'N': '-./',
    'O': '---/',
    'P': '.--./',
    'Q': '--.-/',
    'R': '.-./',
    'S': '.../',
    'T': '-/',
    'U': '..-/',
    'V': '...-/',
    'W': '.--/',
    'X': '-..-/',
    'Y': '-.--/',
    'Z': '--../',
    '1': '.----/',
    '2': '..---/',
    '3': '...--/',
    '4': '....-/',
    '5': '...../',
    '6': '-..../',
    '7': '--.../',
    '8': '---../',
    '9': '----./',
    '0': '-----/',
    '.': '.-.-.-/',
    ',': '--..--/',
    '?': '..--../',
    '(': '-.--.-/',
    ')': '-.--.-/',
    '-': '-....-/',
    ':': '---.../',
    ' ': '/'
}

MC_TO_LETTERS = dict((v,k) for k,v in LETTERS_TO_MC.items())

def translate(msg: str) -> str:
    out = ""
    for x in msg:
        c = x.upper()
        if c in LETTERS_TO_MC.keys():
            out += LETTERS_TO_MC[c]
    return out + '/'

def untranslate(msg: str) -> str:
    m = msg
    out = ""
    while len(m) > 0:
        for k in MC_TO_LETTERS.keys():
            if m.startswith(k):
                out += MC_TO_LETTERS[k]
                m = m[len(k)-1:]
                break
        m = m[1:]
    
    while out.endswith(' '):
        out = out[:-1]
    
    return out

def main(argv: list[str]) -> int:
    argv = argv[1:]
    if len(argv) < 1:
        print("USAGE: ./morse-trainer.py <sample-file>")
        return -1
    
    filepath = argv[0]

    tokens = split_to_tokens(slurp_file(filepath))
    # return

    i = 1
    correct = 0
    words = 0
    start_time = time()
    while True:
        try:
            n = max(int(MAX_LEN * (random.random() ** (5.0 / float(i)))), 1)
            words += n
            start = random.randint(0, len(tokens)-1-n)
            translation = translate(' '.join(tokens[start:start+n]))
            message = untranslate(translation)
            if random.random() < 0.5:
                q = message
                a = translation
            else:
                q = translation
                a = message
            print(f"Message [{i}]: {q}")
            t = input(f"Translation [{i}]: ").upper()
            # print(f"`{q}` | `{a}` | `{t}`")
            if t == a:
                print("CORRECT!")
                correct += 1
            else:
                print("ERROR!")
            print()
        except:
            break
        i += 1
    
    print("DONE!")
    print("--------")
    if i-1 > 0:
        print(f"Accuracy: {float(correct)*100/float(i-1):.2f}%")
        print(f"Timing: {(time()-start_time)/float(words):.2f} seconds per word")


if __name__ == '__main__':
    exit(main(argv))