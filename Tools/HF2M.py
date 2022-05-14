import yaml
import argparse
import numpy as np

from transformers import BertModel


def _transpose_order(mat):
    matT = np.transpose(mat)  # just a view with changed row order
    return matT.flatten(order="C").reshape(matT.shape)  # force row order change and reshape


class ModelConverter(object):

    def __init__(self):
        self.config = None
        self.huggingface = None
        self.marian_model = None

    def load_model(self, bert_model_name):
        """
        Load model from HuggingFace.
        """

        self.huggingface = BertModel.from_pretrained(bert_model_name)
        self.huggingface.eval()

        print(self.huggingface.config)
        self._configure()

    def feed_model(self, bert_model):
        """
        Feed model from existing object.
        """

        self.huggingface = bert_model
        self.huggingface.eval()

        print(self.huggingface.config)
        self._configure()

    def _configure(self):

        self.config = {"type": "bert-classifier", "input-types": ["sequence"], "tied-embeddings-all": True,
                       "tied-embeddings-src": False, "transformer-ffn-depth": 2,
                       "transformer-train-position-embeddings": True, "transformer-preprocess": "",
                       "transformer-postprocess": "dan", "transformer-postprocess-emb": "nd",
                       "bert-train-type-embeddings": False, "version": "huggingface2marian.py conversion",
                       "enc-depth": 0, "transformer-dim-ffn": self.huggingface.config.intermediate_size,
                       "transformer-heads": self.huggingface.config.num_attention_heads,
                       "transformer-ffn-activation": self.huggingface.config.hidden_act,
                       "bert-sep-symbol": "</s>",
                       "bert-class-symbol": "</s>"}

    def translate_model(self, output_path):

        self.marian_model = dict()
        self._recurse(self.huggingface)

        for m in self.marian_model:
            print(m, self.marian_model[m].shape)

        config_yaml_str = yaml.dump(self.config, default_flow_style=False)
        desc = list(config_yaml_str)
        np_desc = np.chararray((len(desc),))
        np_desc[:] = desc
        np_desc.dtype = np.int8
        self.marian_model["special:model.yml"] = np_desc

        print("\nMarian config:")
        print(config_yaml_str)
        print("Saving Marian model to %s" % output_path)
        np.savez(output_path, **self.marian_model)

    def _convert(self, pd, srcs, trg, transpose=True, bias=False):
        if len(srcs) == 1:
            for src in srcs:
                num = pd[src].detach().numpy()
                if bias:
                    self.marian_model[trg] = np.atleast_2d(num)
                else:
                    if transpose:
                        self.marian_model[trg] = _transpose_order(num)  # transpose with row order change
                    else:
                        self.marian_model[trg] = num
        else:  # path that joins matrices together for fused self-attention
            nums = [pd[src].detach().numpy() for src in srcs]
            if bias:
                nums = [np.transpose(np.atleast_2d(num)) for num in nums]

            self.marian_model[trg] = np.stack(nums, axis=0)

    def _extract(self, layer, nth, level):
        name = type(layer).__name__
        print("  " * level, nth, name)

        if name == "BertLayer":

            pd = dict(layer.named_parameters())
            for n in pd:
                print("  " * (level + 1), n, pd[n].shape)

            self._convert(pd, ["attention.self.query.weight"], f"encoder_l{nth + 1}_self_Wq", transpose=True)
            self._convert(pd, ["attention.self.key.weight"], f"encoder_l{nth + 1}_self_Wk")
            self._convert(pd, ["attention.self.value.weight"], f"encoder_l{nth + 1}_self_Wv")

            self._convert(pd, ["attention.self.query.bias"], f"encoder_l{nth + 1}_self_bq", bias=True)
            self._convert(pd, ["attention.self.key.bias"], f"encoder_l{nth + 1}_self_bk", bias=True)
            self._convert(pd, ["attention.self.value.bias"], f"encoder_l{nth + 1}_self_bv", bias=True)

            self._convert(pd, ["attention.output.dense.weight"], f"encoder_l{nth + 1}_self_Wo")
            self._convert(pd, ["attention.output.dense.bias"], f"encoder_l{nth + 1}_self_bo", bias=True)

            self._convert(pd, ["attention.output.LayerNorm.weight"], f"encoder_l{nth + 1}_self_Wo_ln_scale", bias=True)
            self._convert(pd, ["attention.output.LayerNorm.bias"], f"encoder_l{nth + 1}_self_Wo_ln_bias", bias=True)

            self._convert(pd, ["intermediate.dense.weight"], f"encoder_l{nth + 1}_ffn_W1")
            self._convert(pd, ["intermediate.dense.bias"], f"encoder_l{nth + 1}_ffn_b1", bias=True)
            self._convert(pd, ["output.dense.weight"], f"encoder_l{nth + 1}_ffn_W2")
            self._convert(pd, ["output.dense.bias"], f"encoder_l{nth + 1}_ffn_b2", bias=True)

            self._convert(pd, ["output.LayerNorm.weight"], f"encoder_l{nth + 1}_ffn_ffn_ln_scale", bias=True)
            self._convert(pd, ["output.LayerNorm.bias"], f"encoder_l{nth + 1}_ffn_ffn_ln_bias", bias=True)

            self.config["enc-depth"] += 1

        elif name == "BertEmbeddings":

            for n, p in layer.named_parameters():
                print("  " * (level + 1), n, p.shape)
            pd = dict(layer.named_parameters())
            self._convert(pd, ["word_embeddings.weight"], f"Wemb", transpose=False)
            self._convert(pd, ["position_embeddings.weight"], f"Wpos", transpose=False)

            self.config["bert-type-vocab-size"] = 0
            if hasattr(layer, "token_type_embeddings"):
                self._convert(pd, ["token_type_embeddings.weight"], f"Wtype", transpose=False)
                self.config["bert-type-vocab-size"] = pd["token_type_embeddings.weight"].shape[0]
                self.config["bert-train-type-embeddings"] = True

            self._convert(pd, ["LayerNorm.weight"], f"encoder_emb_ln_scale_pre", bias=True)
            self._convert(pd, ["LayerNorm.bias"], f"encoder_emb_ln_bias_pre", bias=True)

            self.config["dim-emb"] = pd["word_embeddings.weight"].shape[1]
            self.config["dim-vocabs"] = [pd["word_embeddings.weight"].shape[0]]
            self.config["max-length"] = pd["position_embeddings.weight"].shape[0]

        elif name == "BertPooler":

            for n, p in layer.named_parameters():
                print("  " * (level + 1), n, p.shape)

            pd = dict(layer.named_parameters())
            self._convert(pd, ["dense.weight"], "classifier_ff_logit_l1_W")
            self._convert(pd, ["dense.bias"], "classifier_ff_logit_l1_b", bias=True)

        else:

            self._recurse(layer, level + 1)

    def _recurse(self, parent, level=0):
        for i, child in enumerate(parent.children()):
            self._extract(child, i, level)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert Huggingface Bert model to Marian weight file.')
    parser.add_argument('--bert', help='Path to Huggingface Bert PyTorch model', required=True)
    parser.add_argument('--marian', help='Output path for Marian weight file', required=True)
    args = parser.parse_args()

    MC = ModelConverter()
    MC.load_model(args.bert)
    MC.translate_model(args.marian)
