#!/bin/sh
/usr/local/Cellar/moses/HEAD/scripts/training/train-model2.perl -root-dir ~/PycharmProjects/MacaronicTextGeneration/data/moses-files -external-bin-dir ~/source-pkgs/giza-pp/external-bin/ --corpus /Users/arenduchintala/PycharmProjects/MacaronicTextGeneration/data/training/train.10 --f en --e de --first-step 1 --last-step 4
