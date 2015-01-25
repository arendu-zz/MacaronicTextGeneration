#!/bin/sh
#moses -f ${PROJECT_DIR}/${CORPUS_FOLDER}/model/moses.ini -t -xml-input exclusive  -n-best-list en-n-best-from-de.txt 100 distinct < ${CORPUS_FOLDER}/${CORPUS_PREFIX}.clean.tok.true.20.de
#moses -f ${PROJECT_DIR}/${CORPUS_FOLDER}/model/moses.ini -t -xml-input exclusive  -n-best-list en-n-best-from-de.txt 3 distinct < ${CORPUS_FOLDER}/${CORPUS_PREFIX}.small.test
moses -f ${PROJECT_DIR}/${CORPUS_FOLDER}/model/moses.ini  -xml-input exclusive  -n-best-list en-n-best-from-de-unk0.txt 3 distinct < ${CORPUS_FOLDER}/${CORPUS_PREFIX}.small.test
#moses -f ${PROJECT_DIR}/${CORPUS_FOLDER}/model/moses.ini -t  -n-best-list en-n-best-from-es.txt 100 distinct < ${CORPUS_FOLDER}/train.full.clean.20.es
