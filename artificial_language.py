#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import sys
import itertools

voiceless = ['p', 't', 'k']
voiceless_wb = ['p', 't', 'k','']
voiced = ['b', 'd', 'g']
aspirated = ['P','T','K','']
aspirated_mono = ['P','T','K']
vowels = ['a', 'e', 'i', 'o', 'u']
nasals = ['m','n','N','']
sibilant = ['s','']
liquids = ['r','']

MAX_WORD_LENGTH = 3

#lang1
#words = [''.join(t) for t in itertools.product(voiceless_wb,vowels,voiceless,vowels,voiceless,vowels)] + [''.join(t) for t in itertools.product(voiceless_wb,vowels,voiceless,vowels)] + [''.join(t) for t in itertools.product(voiceless_wb,vowels,voiceless_wb)]

#lang2
#words = [''.join(t) for t in itertools.product(voiceless_wb,vowels,voiced,vowels,voiced,vowels)] + [''.join(t) for t in itertools.product(voiceless_wb,vowels,voiced,vowels)] + [''.join(t) for t in itertools.product(voiceless_wb,vowels,voiceless_wb)]

#lang3
#words = [''.join(t) for t in itertools.product(aspirated_mono,vowels,voiced,vowels,voiced,vowels,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,voiced,vowels,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,voiceless_wb)]

#lang4
#words = [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,vowels,nasals,voiced,vowels,nasals,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,vowels,nasals,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiceless_wb)]

#lang5 same as lang4 but nasals are optional
#words = [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,vowels,nasals,voiced,vowels,nasals,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,vowels,nasals,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiceless_wb)]

#lang6 same as lang5 with ban on non-homo-organic nasal obstruent clusters
#words = [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,vowels,nasals,voiced,vowels,nasals,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,vowels,nasals,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiceless_wb)]

#lang7 same as lang6 with lateral after voiced obstruents
#words = [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,liquids,vowels,nasals,voiced,liquids,vowels,nasals,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,liquids,vowels,nasals,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiceless_wb)]

#lang8 same as lang7 with sibilant voiceless obstruent cluster 
#words = [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,liquids,vowels,nasals,voiced,liquids,vowels,nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,liquids,vowels,nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,sibilant,voiceless_wb)]

#lang9 same as lang8 with ban on non-homo-organic nasal sibilant clusters in monosyllabic
#words = [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,liquids,vowels,nasals,voiced,liquids,vowels,nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,voiced,liquids,vowels,nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,vowels,nasals,sibilant,voiceless_wb)]

#lang10 same as lang9 with restrictions on initial vowel- only high vowel in first syllable
#words = [''.join(t) for t in itertools.product(aspirated_mono,['i','u'],nasals,voiced,liquids,vowels,nasals,voiced,liquids,vowels,nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['i','u'],nasals,voiced,liquids,vowels,nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['i','u'],nasals,sibilant,voiceless_wb)]

#lang11 same as lang10 with vowel harmony
#words = [''.join(t) for t in itertools.product(aspirated_mono,['i'],nasals,voiced,liquids,['i','e'],nasals,voiced,liquids,['i','e'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['i'],nasals,voiced,liquids,['i','e'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['i'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['u'],nasals,voiced,liquids,['u','o'],nasals,voiced,liquids,['u','o'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['u'],nasals,voiced,liquids,['u','o'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['u'],nasals,sibilant,voiceless_wb)]

#lang12 same as lang11 with vowel harmony and one transparent vowel
#words = [''.join(t) for t in itertools.product(aspirated_mono,['i'],nasals,voiced,liquids,['i','e','a'],nasals,voiced,liquids,['i','e','a'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['i'],nasals,voiced,liquids,['i','e','a'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['i'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['u'],nasals,voiced,liquids,['u','o','a'],nasals,voiced,liquids,['u','o','a'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['u'],nasals,voiced,liquids,['u','o','a'],nasals,sibilant,voiceless_wb)] + [''.join(t) for t in itertools.product(aspirated_mono,['u'],nasals,sibilant,voiceless_wb)]

with open(sys.argv[1], 'w') as f:
    for w in filter(None,words):
        if len(w) >= 3:
            if not any(clust in w for clust in ['md','mt','mg','mk','nb','np','ng','nk','Nb','Np','Nt','Nd','ms','Ns','nsp','nsk']):
                f.write('%s\n'%(' '.join(list(w)).lstrip().rstrip()))

