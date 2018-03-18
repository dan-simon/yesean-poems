import re
import sys

if sys.version_info < (1 | 2,  1 | 2 | 4, 0):
    raise Exception('Use most recent python!')

chars = 'いろはにほへとちりぬるをわかよたれそつねならむうのおくやまけふこえてあさきゆめみしひもせす' + \
'アイウエオカキクケコサシスセソタチツテト'

# consonants = ['', 'r', 't', 'y', 'p', 's', 'd', 'g', 'h', 'j', 'k', 'l',
# 'z', 'b', 'n', 'm', 'ch', 'sh']

consonants = ['', 'r', 't', 'y', 'p', 's', 'h', 'k', 'l', 'n', 'm', 'ch', 'sh']

vowels = 'aeiou'

voiced = {'t': 'd', 'p': 'b', 's': 'z', 'k': 'g', 'ch': 'j'}

def reverse_map(d):
    return {d[i]: i for i in d}

def get_all_map():
    all_map = {consonants[i // len(vowels)] + vowels[i % len(vowels)]: chars[i]
        for i in range(len(chars))}
    for i in list(all_map):
        if i[:-1] in voiced:
            all_map[voiced[i[:-1]] + i[-1]] = all_map[i] + '\u0304'
    return all_map

all_map = get_all_map()

reversed_all_map = reverse_map(all_map)

def convert_word(word, forward=True):
    if forward:
        parts = [i for i in re.split('(?<=[' + vowels + '])', word) if i]
        return ''.join(all_map[i] for i in parts)
    else:
        return re.sub('[' + chars + ']\u0304?',
        lambda x: reversed_all_map[x.group(0)], word)

def convert(text, forward=True):
    if forward:
        return re.sub('[abcdefghijklmnopqrstuvwxyz]+',
            lambda x: convert_word(x.group(0), forward), text)
    else:
        return re.sub('[' + chars + '\u0304]+',
            lambda x: convert_word(x.group(0), forward), text)

print(convert(sys.argv[1], any(i.isalpha() for i in sys.argv[1])))
