# from simalign import SentenceAligner

# # making an instance of our model.
# # You can specify the embedding model and all alignment settings in the constructor.
# aligner = SentenceAligner(model="bert"
#   , token_type="bpe", matching_methods="i")

# zipped_corpus = list(zip(input_tokens, valid_tokens))
# mwmf = []
# inter = []
# itermax = []

# max = len(zipped_corpus)

# for sentence_pair in zipped_corpus:
#   alignments = aligner.get_word_aligns(*sentence_pair)

#   if "mwmf" in aligner.matching_methods:
#     mwmf.append(" ".join(map(lambda x: "{0}-{1}".format(x[0], x[1]), alignments["mwmf"])))
#     if len(mwmf) % 50 == 0: print("Processed {0}/{1}".format(len(mwmf), max))
#   if "inter" in aligner.matching_methods:
#     inter.append(" ".join(map(lambda x: "{0}-{1}".format(x[0], x[1]), alignments["inter"])))
#     if len(inter) % 50 == 0: print("Processed {0}/{1}".format(len(inter), max))
#   if "itermax" in aligner.matching_methods:
#     itermax.append(" ".join(map(lambda x: "{0}-{1}".format(x[0], x[1]), alignments["itermax"])))
#     if len(itermax) % 50 == 0: print("Processed {0}/{1}".format(len(itermax), max))

# if "mwmf" in aligner.matching_methods:
#   with open("/content/GIT/MTData/Alignment/mwmf_align.src-trg", "w+") as f:
#     f.writelines(list(map(lambda x: x + "\n", itermax)))

# if "inter" in aligner.matching_methods:
#   with open("/content/GIT/MTData/Alignment/inter_align.src-trg", "w+") as f:
#     f.writelines(list(map(lambda x: x + "\n", itermax)))

# if "itermax" in aligner.matching_methods:
#   with open("/content/GIT/MTData/Alignment/itermax_align.src-trg", "w+") as f:
#     f.writelines(list(map(lambda x: x + "\n", itermax)))