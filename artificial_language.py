#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import sys
import itertools

voiceless = ['p', 't', 'k']
voiced = ['b', 'd', 'g']
aspirated = ['P','T','K']
vowels = ['a', 'e', 'i', 'o', 'u']
nasals = ['m','n','N','']
sibilant = ['s','']
liquids = ['r','']

MAX_WORD_LENGTH = 3

#lang1
#words = [''.join(t) for t in itertools.product(voiceless,vowels,voiceless,vowels,voiceless,vowels)] + [''.join(t) for t in itertools.product(voiceless,vowels,voiceless,vowels)] + [''.join(t) for t in itertools.product(voiceless,vowels)]

#lang2
#words = [''.join(t) for t in itertools.product(voiceless,vowels,voiced,vowels,voiced,vowels)] + [''.join(t) for t in itertools.product(voiceless,vowels,voiced,vowels)] + [''.join(t) for t in itertools.product(voiceless,vowels)]

#lang3
#words = [''.join(t) for t in itertools.product(aspirated,vowels,voiced,vowels,voiced,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,voiced,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,voiceless)]

#lang4
#words = [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,vowels,nasals,voiced,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiceless)]

#lang5 same as lang4 but nasals are optional
#words = [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,vowels,nasals,voiced,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiceless)]

#lang6 same as lang5 with ban on non-homo-organic nasal obstruent clusters
#words = [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,vowels,nasals,voiced,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiceless)]

#lang7 same as lang6 with lateral after voiced obstruents
#words = [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,liquids,vowels,nasals,voiced,liquids,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,liquids,vowels,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiceless)]

#lang8 same as lang7 with sibilant voiceless obstruent cluster 
#words = [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,liquids,vowels,nasals,voiced,liquids,vowels,sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,liquids,vowels,sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,sibilant,voiceless)]

#lang9 same as lang8 with ban on non-homo-organic nasal sibilant clusters in monosyllabic
#words = [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,liquids,vowels,nasals,voiced,liquids,vowels,sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,voiced,liquids,vowels,sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,vowels,nasals,sibilant,voiceless)]

#lang10 same as lang9 with restrictions on initial vowel- only high vowel in first syllable
#words = [''.join(t) for t in itertools.product(aspirated,['i','u'],nasals,voiced,liquids,vowels,nasals,voiced,liquids,vowels,sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['i','u'],nasals,voiced,liquids,vowels,sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['i','u'],nasals,sibilant,voiceless)]

#lang11 same as lang10 with vowel harmony
#words = [''.join(t) for t in itertools.product(aspirated,['i'],nasals,voiced,liquids,['i','e'],nasals,voiced,liquids,['i','e'],sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['i'],nasals,voiced,liquids,['i','e'],sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['i'],nasals,sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['u'],nasals,voiced,liquids,['u','o'],nasals,voiced,liquids,['u','o'],sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['u'],nasals,voiced,liquids,['u','o'],sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['u'],nasals,sibilant,voiceless)]

#lang11 same as lang11 with vowel harmony and one transparent vowel
#words = [''.join(t) for t in itertools.product(aspirated,['i'],nasals,voiced,liquids,['i','e','a'],nasals,voiced,liquids,['i','e','a'],sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['i'],nasals,voiced,liquids,['i','e','a'],sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['i'],nasals,sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['u'],nasals,voiced,liquids,['u','o','a'],nasals,voiced,liquids,['u','o','a'],sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['u'],nasals,voiced,liquids,['u','o','a'],sibilant,voiceless)] + [''.join(t) for t in itertools.product(aspirated,['u'],nasals,sibilant,voiceless)]

with open(sys.argv[1], 'w') as f:
    for w in filter(None,words):
        if not any(clust in w for clust in ['md','mt','mg','mk','nb','np','ng','nk','Nb','Np','Nt','Nd','ms','Ns','nsk','nsp']):
            f.write('%s\n'%(' '.join(list(w)).lstrip().rstrip()))

