#!/bin/sh
${MOSES_DIR}/scripts/training/train-model.perl -root-dir ${PROJECT_DIR}/data/moses-files -external-bin-dir ~/source-pkgs/giza-pp/external-bin/ --corpus ${PROJECT_DIR}/data/training/train.clean --f en --e de --first-step 1 --last-step 4
