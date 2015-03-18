#!/bin/sh
source /home/arenduc1/MachineTranslation/MacaronicTextGeneration/config.cfg
moses -f $HOME/MachineTranslation/MyExperiments/WMT2013/tuning/moses.tuned.and.filtered.ini.2 -xml-input exclusive -n-best-list $DATA_DIR/$FILE_PREFIX.de.20.substr.trans 100 distinct < $DATA_DIR/$FILE_PREFIX.de.20.txtspan

