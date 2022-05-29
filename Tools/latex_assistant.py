from log_parser import parse_valid_file
import pyperclip

# ce-mean-words
# cross-entropy
# perplexity

title_map = {
    "baseline": "Baseline Architectures",
    "dropout": "Source Word Dropout",
    "adaptation": "Error + Domain Adaptation",
    "large_vocab": "Adaptation Large Vocab",
    "tied": "Tied Embeddings",
    "BERTu": "Pretrained Embeddings - BERTu",
    "mBERTu": "Pretrained Embeddings - mBERTu"
}

legend_map = {
    "baseline": "AMUN, Transformer, Seq2Seq",
    "dropout": "BLEU, BLEU-Best",
    "large_vocab": "BLEU, BLEU-Best",
    "adaptation": "BLEU, BLEU-Best",
    "tied": "BLEU, BLEU-Best",
    "BERTu": "BLEU, BLEU-Best",
    "mBERTu": "BLEU, BLEU-Best",
}

score_map = {
    "bleu": "BLEU",
    "cross-entropy": "Cross Entropy",
    "ce-mean-words": "Cross Entropy Mean Words",
    "perplexity": "Perplexity"
}

y_max_dict = {
    'bleu': 100,
    'cross-entropy': 200,
    'perplexity': 75
}

y_tick_dict = {
    'bleu': "0,20,40,60,80,100",
    'cross-entropy': "0,40,80,120,160,200",
    'perplexity': "0,25,50,75"
}

score = 'bleu'
experiment = 'mBERTu'

dict_params = dict(
    title='{0} ({1})'.format(title_map[experiment], score_map[score])
    , x_label="Updates"
    , y_label=score_map[score]
    , x_min=0
    , x_max=20000 if experiment == 'baseline' else 25000
    , y_min=0
    , y_max=y_max_dict[score]
    , x_tick_list="0,5000,10000,15000,20000" if experiment == 'baseline' else "0,5000,10000,15000,20000,25000"
    , y_tick_list=y_tick_dict[score]
    , legend_pos="outer north east"
    , legend=legend_map[experiment])

if experiment == 'baseline':
    for model in (['amun', 'transformer', 's2s']):

        lines = parse_valid_file('../Logs/{0}.log'.format(model))

        if score != 'all':
            lines = list(filter(lambda x: x[2] == score, lines))

        best = True
        print("\n\n*** COORDS - {0} - {1} ***".format(model, score))
        coords = list(map(lambda x: (x[1], x[5] if best else x[3]), filter(lambda y: y[1] % 1000 == 0, lines)))
        dict_params["coord_" + model] = "\n\t\t\t".join(map(lambda x: str(x), coords))

        for coord in coords:
            print(coord)
else:
    model = experiment

    lines = parse_valid_file('../Logs/{0}.log'.format(model))

    if score != 'all':
        lines = list(filter(lambda x: x[2] == score, lines))

    for best in [False, True]:
        print("\n\n*** COORDS - {0} - {1} ***".format(model, score))
        coords = list(map(lambda x: (x[1], x[5] if best else x[3]), filter(lambda y: y[1] % 1000 == 0, lines)))
        dict_params["coord_" + str(best)] = "\n\t\t\t".join(map(lambda x: str(x), coords))

        for coord in coords:
            print(coord)

print("\n\n*** TEMPLATE ***\n\n")
with open("../Template/latex_baseline.txt" if experiment == 'baseline' else "../Template/latex.txt", 'r',
          encoding='utf-8') as f:
    pyperclip.copy(f.read().format(**dict_params))
    print("COPIED TO CLIPBOARD!")
