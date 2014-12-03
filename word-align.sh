#!/bin/sh
#do tokenizing
${MOSES_DIR}/scripts/tokenizer/tokenizer.perl -l en < ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.en > ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.tok.en
${MOSES_DIR}/scripts/tokenizer/tokenizer.perl -l de < ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.de > ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.tok.de

#learn truecase model
${MOSES_DIR}/scripts/recaser/train-truecaser.perl --model ${PROJECT_DIR}/${CORPUS_FOLDER}/truecase-model.en --corpus  ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.tok.en
${MOSES_DIR}/scripts/recaser/train-truecaser.perl --model ${PROJECT_DIR}/${CORPUS_FOLDER}/truecase-model.de --corpus  ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.tok.de

#do truecasing
${MOSES_DIR}/scripts/recaser/truecase.perl --model ${PROJECT_DIR}/${CORPUS_FOLDER}/truecase-model.en < ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.tok.en > ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.tok.true.en
${MOSES_DIR}/scripts/recaser/truecase.perl --model ${PROJECT_DIR}/${CORPUS_FOLDER}/truecase-model.de < ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.tok.de > ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.tok.true.de

#do cleaning
${MOSES_DIR}/scripts/training/clean-corpus-n.perl ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.tok.true de en ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.clean.tok.true 1 80

#do word align and phrase table
${MOSES_DIR}/scripts/training/train-model.perl -root-dir ${PROJECT_DIR}/${CORPUS_FOLDER} -external-bin-dir ${EXTERNAL_BIN_DIR} --corpus ${PROJECT_DIR}/${CORPUS_FOLDER}/${CORPUS_PREFIX}.clean.tok.true --f de --e en --first-step 1 --last-step 6 --parallel 
