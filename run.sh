#!/usr/bin/env bash

echo -e "====  INTERPR  ============="

php7.3 parse.php <$1 | python3 interpret.py --input="./empty" 
ACT_RET=$?

echo -e "\n====  IC18INT  ============="

python3 change_head.py <$1 >tmp.IFJcode18
./ic18int tmp.IFJcode18 <./empty
REF_RET=$?
rm ./tmp.IFJcode18

echo -e "\n====  END  ================="
echo "act ret: $ACT_RET ref ret: $REF_RET"