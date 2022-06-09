import os

import pyperclip

from log_parser import parse_valid_file

experiments = [
    dict(source_file="01_bench_amun.log"
         , title="Benchmark (AMUN)"
         , xlabel="Updates"
         , xmin=0
         , xmax=20000
         , xtick="0,5000,10000,15000,20000"
         , legend_pos="north east"
         , color=""
         , run_mark="halfcircle*"
         , best_mark="*"
         , legend="Running Score, Best Score"
         )

    , dict(source_file="02_bench_s2s.log"
           , title="Benchmark (Seq2Seq)"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="03_bench_transformer.log"
           , title="Benchmark (Vaswani Transformer)"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="04_bench_source_corruption.log"
           , title="Source Word Corruption"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="05_bench_tied_embed.log"
           , title="Benchmark + Tied Embeddings"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="06_bench_BERTu.log"
           , title="Benchmark + Pretrained (BERTu)"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="07_bench_mBERTu.log"
           , title="Benchmark + Pretrained (mBERTu)"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="08_adaptation_domain_error.log"
           , title="Domain \& Error Adapted"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="09_adaptation_large_vocab.log"
           , title="Domain \& Error Adapted + Large Vocabularies"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="10_adaptation_tied_embed.log"
           , title="Domain \& Error Adapted + Tied Embeddings"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="11_adaptation_BERTu.log"
           , title="Domain \& Error Adapted + Pretrained (BERTu)"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="12_adaptation_mBERTu.log"
           , title="Domain \& Error Adapted + Pretrained (mBERTu)"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )

    , dict(source_file="13_final.log"
           , title="Final Model"
           , xlabel="Updates"
           , xmin=0
           , xmax=20000
           , xtick="0,5000,10000,15000,20000"
           , legend_pos="north east"
           , run_mark="halfcircle*"
           , best_mark="*"
           , legend="Running Score, Best Score"
           )
]

metrics = {"bleu": dict(ylabel="BLEU", ymin=0, ymax=100, ytick="0,20,40,60,80,100", color="blue")
    , "cross-entropy": dict(ylabel="Cross Entropy", ymin=0, ymax=200, ytick="0,40,80,120,160,200", color="brown")
    , "ce-mean-words": dict(ylabel="CE Mean Words", ymin=0, ymax=10, ytick="0,2,4,6,8,10", color="orange")
    , "perplexity": dict(ylabel="Perplexity", ymin=0, ymax=50, ytick="0,10,20,30,40,50", color="red")}

print([0])
LOG_PATH = "../Logs/"

coord_map = {}

for log_file in os.listdir('../Logs'):

    experiment_key = log_file.replace(".log", "")
    filepath = LOG_PATH + log_file
    lst_logs = parse_valid_file(filepath)

    coord_run = {}
    coord_best = {}

    for key in metrics.keys():
        coord_run[key] = []
        coord_best[key] = []

    for log in lst_logs:
        if log[2] not in ['translation', 'bleu-detok']:
            update_number = int(int(log[1]) / 100) * 100
            coord_run[log[2]].append((update_number, log[3]))
            coord_best[log[2]].append((update_number, log[5]))

    coord_map[experiment_key] = {
        "run": coord_run,
        "best": coord_best
    }

latex_plots = []

for coord_key, coord_obj in coord_map.items():

    context_dict = filter(lambda x: x["source_file"] == coord_key + ".log", experiments).__next__()

    for metric_key, metric_obj in metrics.items():
        context_dict = {**context_dict
            , **metric_obj
            , "coord_run": "\n\t\t\t".join(map(lambda x: str(x), filter(lambda x: x[0] % 1000 == 0 and x[0] <= 20000,
                                                                        coord_obj["run"][metric_key])))
            , "coord_best": "\n\t\t\t".join(map(lambda x: str(x), filter(lambda x: x[0] % 1000 == 0 and x[0] <= 20000,
                                                                         coord_obj["best"][metric_key])))
                        }

        latex_plots.append(context_dict)

out_text = ""
get_me = "tables"

if get_me == "plots":
    with open("../Template/latex_plot.txt", 'r', encoding='utf-8') as ltx_plot, \
            open("../Template/latex_tkz.txt", 'r', encoding='utf-8') as ltx_tkz:
        ltx_plot_template = ltx_plot.read()
        ltx_tkz_template = ltx_tkz.read()
        ltx_text = ""

        for experiment_obj in experiments:

            tkz_text = ""

            for plot in filter(lambda l: l['source_file'] == experiment_obj['source_file'], latex_plots):
                plot["title"] = plot["title"] + " - (" + plot["ylabel"] + ")"
                tkz_text += ltx_tkz_template.format(**plot) + "\n"

            ltx_text += ltx_plot_template.format(**{"tkz": tkz_text
                , "caption": experiment_obj["title"]
                , "label": "fig:" + experiment_obj["title"].replace(" ", "").replace("\&", "") + "AllScores"})
        out_text += ltx_text

elif get_me == "tables":
    with open("../Template/latex_table.txt", 'r', encoding='utf-8') as ltx_tb, \
            open("../Template/latex_row.txt", 'r', encoding='utf-8') as ltx_row:
        ltx_tb_template = ltx_tb.read()
        ltx_row_template = ltx_row.read()
        ltx_text = ""

        for experiment_obj in experiments:

            scores = coord_map[experiment_obj['source_file'].replace('.log', '')]
            iter_range = len(scores['run']['bleu'])

            runs = scores['run']
            best = scores['best']

            data = ""

            for iter in range(0, iter_range):

                updates = int(runs['bleu'][iter][0]/100)*100

                if updates % 1000 == 0 and updates <= 20000:
                    row_val = dict(
                        updates=updates,
                        bleu_running=runs['bleu'][iter][1],
                        bleu_best=best['bleu'][iter][1],
                        cross_entropy_running=runs['cross-entropy'][iter][1],
                        cross_entropy_best=best['cross-entropy'][iter][1],
                        mean_words_running=runs['ce-mean-words'][iter][1],
                        mean_words_best=best['ce-mean-words'][iter][1],
                        perplexity_running=runs['perplexity'][iter][1],
                        perplexity_best=best['perplexity'][iter][1])

                    data += ltx_row_template.format(**row_val) + '\n'

            out_text += ltx_tb_template.format(**{
                'data': data,
                'title': experiment_obj['title'] + " - Training Scores",
                'label': "fig:" + experiment_obj['title'].replace(" ", "").replace("\&", "") + "TrainingScores"
            })


pyperclip.copy(out_text)
print("COPIED TO CLIPBOARD!")
