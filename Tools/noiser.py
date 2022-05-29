import math
import random
import shutil
from synthesis import Synthesizer, SynthesisStrategy

for file_pair in [
        ("../MLRS/corpus_curated_tokenised.txt", "../MLRS/Synthesized/src.txt"),
        ("../Common Voice/common_voice_tokenised.txt", "../Common Voice/Synthesized/src.txt")
    ]:
    source_filepath, destination_filepath = file_pair

    sentence_list = []
    copy_over = 1

    for _ in range(0, copy_over):
        with open(source_filepath, "r", encoding='utf8') as f:
            sentence_list = sentence_list + f.readlines()


    # Filter to list
    source = list(filter(lambda y: y, map(lambda x: [e.replace('\n', '') for e in x.split(' ')], sentence_list)))

    synthesis_ops = [
        dict(synthesis_strategy=SynthesisStrategy.COMMON_ARTICLE_ERRORS, sentence_seed=0.5, token_seed=0.2)
        , dict(synthesis_strategy=SynthesisStrategy.NO_SILENT_LETTERS, sentence_seed=0.4, token_seed=0.4)
        , dict(synthesis_strategy=SynthesisStrategy.NO_FONTS, sentence_seed=1, token_seed=1)
        , dict(synthesis_strategy=SynthesisStrategy.KEY_PROXIMITY_TYPO, sentence_seed=0.2, token_seed=0.1, character_seed=0.05)
        , dict(synthesis_strategy=SynthesisStrategy.KEY_INSERTION, sentence_seed=0.2, token_seed=0.1, character_seed=0.05)
        , dict(synthesis_strategy=SynthesisStrategy.KEY_DUPLICATE, sentence_seed=0.2, token_seed=0.1, character_seed=0.05)
        , dict(synthesis_strategy=SynthesisStrategy.KEY_SUBSTITUTION, sentence_seed=0.2, token_seed=0.1, character_seed=0.05)
        , dict(synthesis_strategy=SynthesisStrategy.KEY_OMISSION, sentence_seed=0.2, token_seed=0.1, character_seed=0.05)
    ]

    synth = Synthesizer(source)

    for op in synthesis_ops:
        synth.synthesize(**op)

    with open(destination_filepath, "w+", encoding='utf8') as f:
        for ele in synth.data:
            f.write(" ".join(ele) + "\n")

    shutil.copyfile(source_filepath, destination_filepath.replace("src", "trg"))