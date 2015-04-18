#!/bin/sh
source ./config.cfg
OUTPUT_DIR=$PROJECT_DIR/outputs
OPTIONS="--lm $LM_FILE --st $DATA_DIR/substring-translations.20.tuned.en.3 -p 2"
#python bottom-up-tree.py $OPTIONS --sim m > $OUTPUT_DIR/meteor.10.log
#python bottom-up-tree.py $OPTIONS --sim m -o  > $OUTPUT_DIR/meteor.10.outside.log
python bottom-up-tree.py $OPTIONS --sim m --cs $DATA_DIR/$FILE_PREFIX.20.de.parsespans > $OUTPUT_DIR/meteor.10.parse.log
#python bottom-up-tree.py $OPTIONS --sim e > $OUTPUT_DIR/editd.10.log
#python bottom-up-tree.py $OPTIONS --sim e -o  > $OUTPUT_DIR/editd.10.outside.log
#python bottom-up-tree.py $OPTIONS --sim e --cs $DATA_DIR/$FILE_PREFIX.20.de.parsespans > $OUTPUT_DIR/editd.10.parse.log

