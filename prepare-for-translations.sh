#!/bin/sh
#source /Users/arenduchintala/PycharmProjects/MacaronicTextGeneration/config.cfg
source /home/arenduc1/MachineTranslation/MacaronicTextGeneration/config.cfg
python make_substrings.py --ce $DATA_DIR/$FILE_PREFIX.en.20 --cd $DATA_DIR/$FILE_PREFIX.de.20
#PARSER_OPTIONS="-binarize -confidence -kbest 10"
PARSER_OPTIONS="-binarize "
export JAVA_OPTIONS="-XX:MaxPermSize=1024m -XX:MaxHeapSize=4048m"
java  $JAVA_OPTIONS  -jar $HOME/source-pkgs/berkeleyparser/berkeleyParser.jar $PARSER_OPTIONS -gr $HOME/source-pkgs/berkeleyparser/ger_sm5.gr < $DATA_DIR/$FILE_PREFIX.de.20 > $DATA_DIR/$FILE_PREFIX.de.20.parse
#java  $JAVA_OPTIONS  -jar ~/source-pkgs/berkeleyparser/berkeleyParser.jar -gr ~/source-pkgs/berkeleyparser/ger_sm5.gr < $DATA_DIR/$FILE_PREFIX.de.20 > $DATA_DIR/$FILE_PREFIX.de.20.nonbin.parse
python constituents.py -p $DATA_DIR/$FILE_PREFIX.de.20.parse
python make_substrings.py --ce $DATA_DIR/$FILE_PREFIX.en.20 --cd $DATA_DIR/$FILE_PREFIX.de.20 #will write out .span and .txtspan
