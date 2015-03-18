#!/bin/sh
moses -f /home/arenduc1/MachineTranslation/MyExperiments/WMT2013/tuning/moses.tuned.and.filtered.ini.2 -xml-input exclusive -n-best-list ${CORPUS_FOLDER}/substring-translations.20.tuned.and.filtered.en 100 distinct < ${CORPUS_FOLDER}/${CORPUS_PREFIX}.clean.tok.true.20.de.txtspan

