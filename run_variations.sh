#!/bin/sh
source config.cfg
python bottom-up-tree.py --st $DATA_DIR/substring-translations.20.tuned.en --sim m -p 10 > $OUTPUT_DIR/meteor.10.log
python bottom-up-tree.py --st $DATA_DIR/substring-translations.20.tuned.en --sim m -o -p 10 > $OUTPUT_DIR/meteor.10.outside.log
python bottom-up-tree.py --st $DATA_DIR/substring-translations.20.tuned.en --sim m --cs $DATA_DIR/$FILE_PREFIX.20.de.parsespans -p 10 > $OUTPUT_DIR/meteor.10.parse.log
python bottom-up-tree.py --st $DATA_DIR/substring-translations.20.tuned.en --sim e -p 10 > $OUTPUT_DIR/editd.10.log
python bottom-up-tree.py --st $DATA_DIR/substring-translations.20.tuned.en --sim e --cs $DATA_DIR/$FILE_PREFIX.20.de.parsespans -p 10 > $OUTPUT_DIR/meteor.10.parse.log
python bottom-up-tree.py --st $DATA_DIR/substring-translations.20.tuned.en --sim e -o -p 10 > $OUTPUT_DIR/editd.10.outside.log
