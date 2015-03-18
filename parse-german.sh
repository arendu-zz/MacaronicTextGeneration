#PARSER_OPTIONS="-binarize -confidence -kbest 10"
PARSER_OPTIONS="-binarize "
JAVA_OPTIONS="-XX:MaxPermSize=1024m -XX:MaxHeapSize=4048m"
#java  $JAVA_OPTIONS  -jar ~/source-pkgs/berkeleyparser/berkeleyParser.jar $PARSER_OPTIONS  -gr ~/source-pkgs/berkeleyparser/ger_sm5.gr < data/moses-files/train.clean.tok.true.20.de > data/moses-files/train.clean.tok.true.20.de.parse
java  $JAVA_OPTIONS  -jar ~/source-pkgs/berkeleyparser/berkeleyParser.jar -gr ~/source-pkgs/berkeleyparser/ger_sm5.gr < data/moses-files/train.clean.tok.true.20.de > data/moses-files/train.clean.tok.true.20.de.nonbin.parse
python consituents.py > data/moses-files/train.clean.tok.true.20.de.parsespans
