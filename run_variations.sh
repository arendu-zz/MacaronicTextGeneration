python bottom-up-tree.py --st data/moses-files/substring-translations.20.tuned.en --sim m -p 10 > outputs/output.meteor.10.log
python bottom-up-tree.py --st data/moses-files/substring-translations.20.tuned.en --sim e -p 10 > outputs/output.editd.10.log
python bottom-up-tree.py --st data/moses-files/substring-translations.20.tuned.en --sim m -o -p 10 > outputs/output.meteor.10.outside.log
python bottom-up-tree.py --st data/moses-files/substring-translations.20.tuned.en --sim e -o -p 10 > outputs/output.editd.10.outside.log
python bottom-up-tree.py  --st data/moses-files/substring-translations.20.tuned.en --sim m -p 10 --cs data/moses-files/train.clean.tok.true.20.de.parsespans > outputs/output.constituent.meteor.10.log
python bottom-up-tree.py --st data/moses-files/substring-translations.20.tuned.en --sim e -p 10 --cs data/moses-files/train.clean.tok.true.20.de.parsespans > outputs/output.constituent.editd.10.log
python bottom-up-tree.py --st data/moses-files/substring-translations.20.tuned.en --sim m -o -p 10 --cs data/moses-files/train.clean.tok.true.20.de.parsespans > outputs/output.constituent.meteor.10.outside.log
python bottom-up-tree.py --st data/moses-files/substring-translations.20.tuned.en --sim e -o -p 10 --cs data/moses-files/train.clean.tok.true.20.de.parsespans > outputs/output.constituent.editd.10.outside.log

