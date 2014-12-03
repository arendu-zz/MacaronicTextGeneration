#!/bin/sh
${MOSES_DIR}/scripts/training/train-model.perl -root-dir ${PROJECT_DIR}/${CORPUS_FOLDER} -external-bin-dir ${EXTERNAL_BIN_DIR} --corpus ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.clean.tok.true --f de --e en --first-step 6 --lm 0:5:${PROJECT_DIR}/${CORPUS_FOLDER}/en.binary --lm 0:5:${PROJECT_DIR}/${CORPUS_FOLDER}/de.binary
