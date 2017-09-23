import sys
import random
import re

if sys.version_info < (3, 6, 0):
    raise Exception('Use python 3!')

delete_synonyms = ['delete', 'remove', 'del', 'rm']

define_synonyms = ['def', 'define']

restore_synonyms = ['restore']

save_synonyms = ['back', 'backup', 'save']

actions = ['add', 'all', 'given', 'trans', 'intrans', 'check'] + define_synonyms + delete_synonyms + restore_synonyms + save_synonyms

consonants = ['', 'r', 't', 'y', 'p', 's', 'd', 'g', 'h', 'j', 'k', 'l',
'z', 'b', 'n', 'm', 'ch', 'sh']

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

def check(word):
    # numbers are note ids
    return word and (word.isdigit() or word[-1] in vowels and all(i in consonants for i in re.split('[' + vowels + ']', word)))

def check_all():
    for i in read_words():
        if not check(i):
            print(i + ' is a weird word!!!!')

def translate(word, contains=False):
    words = read_words()
    for i in words:
        if word in [i, words[i], None] or (contains and (word in i or word in words[i])):
            print(i + ' means ' + words[i])

def delete(word):
    words = read_words()
    with open('words.txt', 'w') as f:
        for i in words:
            if word not in [i, words[i]] or \
            not yes_or_no('delete ' + i + ' (' + words[i] + ')? '):
                f.write(words[i] + ': ' + i + '\n')

def save():
    with open('words.txt') as f:
        s = f.read()
    with open('words_backup.txt', 'w') as f:
        f.write(s)

def restore():
    if not yes_or_no('Are you sure you want to restore? '):
        return
    with open('words_backup.txt') as f:
        s = f.read()
    with open('words.txt', 'w') as f:
        f.write(s)

def define(word, definition):
    words = read_words()
    with open('words.txt', 'w') as f:
        for i in words:
            question = 'replace current definition for ' + i + ' (' + words[i] + ') with new definition ' \
                + definition + '? '
            if word not in [i, words[i]] or not yes_or_no(question):
                f.write(words[i] + ': ' + i + '\n')
            else:
                f.write(definition + ': ' + i + '\n')

def main(action, word=None, syllables=None):
    if action not in actions:
        raise ValueError('invalid action!')
    if (action not in ['add', 'define', 'given']) != (syllables is None):
        raise ValueError('syllables issue')
    if (action in ['all', 'check'] or action in restore_synonyms + save_synonyms) != (word is None):
        raise ValueError('word issue')
    if action == 'add':
       add(word, syllables=int(syllables))
    if action == 'check':
        check_all()
    if action == 'given':
        # hack
        new_word = syllables
        add(word, translation=new_word)
    elif action in delete_synonyms:
        delete(word)
    elif action in define_synonyms:
        # hack
        definition = syllables
        define(word, definition)
    elif action in save_synonyms:
        save()
    elif action in restore_synonyms:
        restore()
    elif action == 'trans':
        translate(word)
    elif action == 'intrans':
        translate(word, contains=True)
    elif action == 'all':
        translate(None)

if __name__ == '__main__':
    main(*sys.argv[1:])
