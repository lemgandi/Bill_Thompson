#!/bin/bash

for kk in ../html/*.html
do
    FN=$(basename $kk)
    ./table_list.py -i $kk -o ./edited/$FN 2> /dev/null
    if [ $? -gt 0 ]
    then
	echo $FN
    fi
    
done
