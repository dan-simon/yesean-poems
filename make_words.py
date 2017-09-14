import sys
import random

if sys.version_info < (3, 6, 0):
    raise Exception('Use python 3!')

actions = ['add', 'all', 'delete', 'given', 'trans']

consonants = ['', 'r', 't', 'y', 'p', 's', 'd', 'g', 'h', 'j', 'k', 'l',
'z', 'b', 'n', 'm', 'ch']

vowels = 'aeiou'

def generate_syllable():
    return random.choice(consonants) + random.choice(vowels)

def generate_word(n):
    return ''.join(generate_syllable() for _ in range(n))

def read_words():
    with open('words.txt') as f:
        return {j[1]: j[0] for i in f.readlines()
                for j in [[k.strip() for k in i.split(':')]]}

def write_word(english, other):
    with open('words.txt', 'a') as f:
        f.write(english + ': ' + other + '\n')

yes_or_no_dict = {'yes': True, 'no': False}

def yes_or_no(p):
    while True:
        x = input(p)
        if x in yes_or_no_dict:
            return yes_or_no_dict[x]
        else:
            print('not understood')

def add(word, syllables=None, translation=None):
    words = read_words()
    if word in words.values():
        print(word + ' is already defined')
        return None
    if translation is not None and translation in words:
        print(translation + ' already means something')
        return None
    if translation is None:
        while True:
            translation = generate_word(syllables)
            if translation not in words:
                break
    write_word(word, translation)
    print('Generated word ' + translation + ' to mean ' + word)

def translate(word):
    words = read_words()
    for i in words:
        if word in [i, words[i], None]:
            print(i + ' means ' + words[i])

def delete(word):
    words = read_words()
    with open('words.txt', 'w') as f:
        for i in words:
            if word not in [i, words[i]] or \
            not yes_or_no('delete ' + i + ' (' + words[i] + ')? '):
                f.write(words[i] + ': ' + i + '\n')

def main(action, word=None, syllables=None):
    if action not in actions:
        raise ValueError('invalid action!')
    if (action not in ['add', 'given']) != (syllables is None):
        raise ValueError('syllables issue')
    if (action == 'all') != (word is None):
        raise ValueError('word issue')
    if action == 'add':
       add(word, syllables=int(syllables))
    if action == 'given':
        # hack
        new_word = syllables
        add(word, translation=new_word)
    elif action == 'delete':
       delete(word)
    elif action == 'trans':
       translate(word)
    elif action == 'all':
        translate(None)

if __name__ == '__main__':
    main(*sys.argv[1:])
