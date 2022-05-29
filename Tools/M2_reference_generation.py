class TaggedReference(object):

    _TAG_ARCHETYPE = "A {0} {1}|||R:OTHER|||{2}|||REQUIRED|||-NONE-|||0"

    def __init__(self, sequence_tokens):
        self.S = sequence_tokens
        self.str_S = " ".join(['S'] + sequence_tokens)
        self.str_A = " "
        self._generate_tags()
        self.tagged_sequence = self.str_S + "\n" + self.str_A

    def _generate_tags(self):

        arr_A = []
        i = 0

        for A in self.S:
            arr_A.append(self._TAG_ARCHETYPE.format(i, i+1, A))
            i += 1

        self.str_A = "\n".join(arr_A)


class TaggedReferenceFile(object):

    def __init__(self, sequence_file):

        self.tagged_seqeunces = []

        for sequence_tokens in sequence_file:
            self.tagged_seqeunces.append(TaggedReference(sequence_tokens).tagged_sequence)

    def write_to_file(self, output_path):

        with open(output_path, "w", encoding="utf-8") as f:
            f.writelines("\n\n".join(self.tagged_seqeunces))


def generate_m2_reference(tokenised_reference_file, output_path):

    with open(tokenised_reference_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

        token_list = map(lambda x: x.replace('\n', '').split(' '), lines)
        token_list = list(token_list)

        ref_file = TaggedReferenceFile(token_list)
        ref_file.write_to_file("test.txt")
