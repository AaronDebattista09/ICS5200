# ICS5200
This is the repository for the Msc dissertation, "Grammatical Error Correction for Maltese: A Deep Learning Solution for a Low Resource Scenario" by Aaron Debattista in partial fulfilment of the requirements for the degree of Master of Science in Artificial Intelligence (Universtity of Malta).

# Contents

## Common Voice

Folder containing PRE-TOKENISED and PRE-SYNTHESISED data files from Common Voice.

## Evaluation Vocabs

Folder containing vocabularies for evaluating baseline models (baseline) and adapted models (22K).

## Logs

Logs files from the training processes of the top performing projects during the study. These are mainly there to satisfy curiousity but are otherwise not important for assessment.

## MLRS

Folder containing PRE-TOKENISED and PRE-SYNTHESISED data files from MLRS.

## Overwrite

A folder containing files that need to overwrite existing files in third-party repositories for reasons of compatibility.

## QariTalProvi_Batch_1

Contains the original files as well as the PRE-TOKENISED and CURATED datasets for Qari Tal-Provi (Batch 1).

## QariTalProvi_Batch_2

Contains the original files as well as the PRE-TOKENISED and CURATED datasets for Qari Tal-Provi (Batch 2).

## Template

Contains template files for plots/tables on Latex. It is not important for assessment.

## Tools

Contains a number of tools used in support of the project.

* **alignment.py** - Generates alignment files.
* **data_parser_QTP_Batch1.py** - Was used to parse documents from QariTalProvi_Batch_1
* **data_parser_QTP_Batch2.py** - Was used to parse documents from QariTalProvi_Batch_2
* **HF2M.py** - Converts BERT model files into Marian-readable model files.
* **M2_reference_generator.py** - Used to generate reference M2 files for target files used in the final model (QariTalProvi_Batch_2)
* **noiser.py** - Calls methods from 'synthesis.py' in order to apply noise to the files from Common Voice and MLRS.
* **synthesis.py** - A library of synthesis methods.
* **tokenisation.py** - Contains Maltese tokeniser.
