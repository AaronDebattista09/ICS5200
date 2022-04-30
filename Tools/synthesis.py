import enum
import math
import random
from functools import reduce
from random import randint

# Assume Maltese-48 keyboard
KEYBOARD_MAP = {
    'Q': [x for x in "WAS"], 'q': [x for x in "was"],
    'W': [x for x in "QSDE"], 'w': [x for x in "qsde"],
    'E': [x for x in "WSDR"], 'e': [x for x in "wsdr"],
    'R': [x for x in "EDFT"], 'r': [x for x in "edft"],
    'T': [x for x in "RFGY"], 't': [x for x in "rfgy"],
    'Y': [x for x in "TGHU"], 'y': [x for x in "tghu"],
    'U': [x for x in "YHJI"], 'u': [x for x in "yhji"],
    'I': [x for x in "UJKO"], 'i': [x for x in "ujko"],
    'O': [x for x in "IKLP"], 'o': [x for x in "iklp"],
    'P': [x for x in "OL:Ġ"], 'p': [x for x in "ol;ġ"],
    'Ġ': [x for x in "P:@Ħ"], 'ġ': [x for x in "p;'ħ"],
    'Ħ': [x for x in "@Ġ~+"], 'ħ': [x for x in "'ġ#="],
    'A': [x for x in "QWSZŻ"], 'a': [x for x in "qwszż"],
    'S': [x for x in "AWZX"], 's': [x for x in "awzx"],
    'D': [x for x in "SEXC"], 'd': [x for x in "sexc"],
    'F': [x for x in "DRCV"], 'f': [x for x in "drcv"],
    'G': [x for x in "FTVB"], 'g': [x for x in "ftvb"],
    'H': [x for x in "GYBN"], 'h': [x for x in "gybn"],
    'J': [x for x in "HUNM"], 'j': [x for x in "hunm"],
    'K': [x for x in "JIML"], 'k': [x for x in "jiml"],
    'L': [x for x in "O<>"], 'l': [x for x in "o,."],
    'Ż': [x for x in "AZ"], 'ż': [x for x in "az"],
    'Z': [x for x in "SXŻ"], 'z': [x for x in "sxż"],
    'X': [x for x in "CDSZ"], 'x': [x for x in "cdsz"],
    'C': [x for x in "VFDX"], 'c': [x for x in "vfdx"],
    'V': [x for x in "BGDC"], 'v': [x for x in "bgdc"],
    'B': [x for x in "NHGV"], 'b': [x for x in "nhgv"],
    'N': [x for x in "MJHB"], 'n': [x for x in "mjhb"],
    'M': [x for x in "KJN<"], 'm': [x for x in "kjn,"],
    'Ċ': [x for x in "!Q"], 'ċ': [x for x in "1q"],
}

KEYBOARD_MAP_ALPHA_ONLY = {
    'Q': [x for x in "WAS"], 'q': [x for x in "was"],
    'W': [x for x in "QSDE"], 'w': [x for x in "qsde"],
    'E': [x for x in "WSDR"], 'e': [x for x in "wsdr"],
    'R': [x for x in "EDFT"], 'r': [x for x in "edft"],
    'T': [x for x in "RFGY"], 't': [x for x in "rfgy"],
    'Y': [x for x in "TGHU"], 'y': [x for x in "tghu"],
    'U': [x for x in "YHJI"], 'u': [x for x in "yhji"],
    'I': [x for x in "UJKO"], 'i': [x for x in "ujko"],
    'O': [x for x in "IKLP"], 'o': [x for x in "iklp"],
    'P': [x for x in "OLĠ"], 'p': [x for x in "olġ"],
    'Ġ': [x for x in "PĦ"], 'ġ': [x for x in "pħ"],
    'Ħ': [x for x in "Ġ"], 'ħ': [x for x in "ġ"],
    'A': [x for x in "QWSZŻ"], 'a': [x for x in "qwszż"],
    'S': [x for x in "AWZX"], 's': [x for x in "awzx"],
    'D': [x for x in "SEXC"], 'd': [x for x in "sexc"],
    'F': [x for x in "DRCV"], 'f': [x for x in "drcv"],
    'G': [x for x in "FTVB"], 'g': [x for x in "ftvb"],
    'H': [x for x in "GYBN"], 'h': [x for x in "gybn"],
    'J': [x for x in "HUNM"], 'j': [x for x in "hunm"],
    'K': [x for x in "JIML"], 'k': [x for x in "jiml"],
    'L': [x for x in "O"], 'l': [x for x in "o"],
    'Ż': [x for x in "AZ"], 'ż': [x for x in "az"],
    'Z': [x for x in "SXŻ"], 'z': [x for x in "sxż"],
    'X': [x for x in "CDSZ"], 'x': [x for x in "cdsz"],
    'C': [x for x in "VFDX"], 'c': [x for x in "vfdx"],
    'V': [x for x in "BGDC"], 'v': [x for x in "bgdc"],
    'B': [x for x in "NHGV"], 'b': [x for x in "nhgv"],
    'N': [x for x in "MJHB"], 'n': [x for x in "mjhb"],
    'M': [x for x in "KJN"], 'm': [x for x in "kjn"],
    'Ċ': [x for x in "!Q"], 'ċ': [x for x in "1q"],
}


class Synthesizer(object):

    def __init__(self, tokenized_source):
        """

        :param tokenized_source: Tokenised data (list of lists)
        """

        self.tokenized_source = tokenized_source

    def synthesize(self, synthesis_strategy, rounding=math.ceil, key_map=KEYBOARD_MAP_ALPHA_ONLY,
                   sentence_seed=0, token_seed=0,  # All strategies
                   character_seed=0  # Key Proximity
                   ):
        """

        :param synthesis_strategy: Synthesis strategy.
        :param rounding: Rounding function.
        :param key_map: Overwrite the key proximity map.
        :param sentence_seed: Percentage of sentences on which to apply synthesis
        :param token_seed: Percentage of tokens to be synthesized
        :param character_seed: Percentage chance for a character to be synthesized
        :return:
        """

        sentences = self.tokenized_source
        # TODO: remove replacements from the below method
        rows_to_synthesize_idx = _index_slicer(sentences, rounding(len(self.tokenized_source) * sentence_seed))

        for row_idx in rows_to_synthesize_idx:
            row = sentences[row_idx]
            tokens_to_synthesize_idx = _index_slicer(row, rounding(len(row) * token_seed))

            for token_idx in tokens_to_synthesize_idx:

                token = row[token_idx]

                if synthesis_strategy == SynthesisStrategy.KEY_PROXIMITY_TYPO:
                    characters_to_synthesize_idx = _index_slicer(token, rounding(len(token) * character_seed))

                    for character_idx in characters_to_synthesize_idx:

                        character = token[character_idx]

                        if character in "qwertyuiopasdfghjklzxcvbnmċżġħQWERTYUIOPASDFGHJKLZXCVBNMĊŻĠĦ":
                            new_char = random.choice(key_map[character])
                            token = _replace(token, new_char, character_idx)

                            row[token_idx] = token

                elif synthesis_strategy == SynthesisStrategy.KEY_SUBSTITUTION:

                    if len(token) > 1:
                        # Indexing starts from 0 and there is no character that follows the last character THEREFORE: -2
                        random_pair_idx = randint(0, len(token) - 2)
                        left_char = token[random_pair_idx]
                        right_char = token[random_pair_idx + 1]

                        token = _replace(token, right_char, random_pair_idx)
                        token = _replace(token, left_char, random_pair_idx + 1)

                        row[token_idx] = token

                elif synthesis_strategy == SynthesisStrategy.KEY_OMISSION:

                    if len(token) > 1:
                        random_char_idx = randint(0, len(token) - 1)
                        token = token[:random_char_idx] + token[random_char_idx + 1:]

                        row[token_idx] = token

                elif synthesis_strategy == SynthesisStrategy.KEY_DUPLICATE:

                    if len(token) > 1:
                        random_char_idx = randint(0, len(token) - 1)
                        token = token[:random_char_idx] + token[random_char_idx - 1:]

                        row[token_idx] = token

                elif synthesis_strategy == SynthesisStrategy.KEY_INSERTION:

                    if len(token) > 1:

                        random_char_idx = randint(0, len(token) - 1)

                        if random_char_idx == 0 or random_char_idx == len(token) - 1:
                            character = token[random_char_idx]
                        else:
                            # Get left or right character instead
                            character = token[random_char_idx-1] if randint(0, 1) else token[random_char_idx+1]

                        if character in "qwertyuiopasdfghjklzxcvbnmċżġħQWERTYUIOPASDFGHJKLZXCVBNMĊŻĠĦ":
                            new_char = random.choice(key_map[character]+[character])
                            token = token[:random_char_idx] + new_char + token[random_char_idx:]

                            row[token_idx] = token

                elif synthesis_strategy == SynthesisStrategy.NO_FONTS:

                    token = token.replace('ċ', 'c').replace('ż', 'z').replace('ħ', 'h').replace('ġ', 'g').\
                        replace('Ċ', 'C').replace('Ż', 'Z').replace('Ħ', 'H').replace('Ġ', 'G')

                    row[token_idx] = token

                elif synthesis_strategy == SynthesisStrategy.NO_SILENT_LETTERS:

                    token = token.replace('Gh', '').replace('Għ', '').replace('gh', '').replace('għ', '').replace('h', '').replace('H', '')

                    row[token_idx] = token

                elif synthesis_strategy == SynthesisStrategy.DROPOUT:

                    del row[token_idx]

            sentences[row_idx] = row

        return sentences


class SynthesisStrategy(enum.Enum):
    KEY_PROXIMITY_TYPO = 1
    KEY_SUBSTITUTION = 2
    KEY_OMISSION = 3
    KEY_DUPLICATE = 4
    KEY_INSERTION = 5
    NO_FONTS = 6
    NO_SILENT_LETTERS = 7
    DROPOUT = 8


def _index_slicer(element_list, k_val):
    max_len = len(element_list)

    if max_len == k_val:
        return range(0, max_len-1)
    else:
        return list(random.sample(range(0, max_len-1), k=k_val))


def _replace(source_str, replacement_str, index, no_fail=False):
    # Raise an error if index is outside of string bounds
    if not no_fail and index not in range(len(source_str)):
        raise ValueError("index outside given string")

    # if not error, but the index is still not in the correct range
    if index < 0:  # add it to the beginning
        return replacement_str + source_str
    if index > len(source_str):  # add it to the end
        return source_str + replacement_str

    # insert the new string between "slices" of the original
    return source_str[:index] + replacement_str + source_str[index + 1:]
