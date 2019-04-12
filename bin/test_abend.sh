#!/bin/bash

for kk in ../html/*.html
do
    FN=$(basename $kk)
    if ! ./urlshifter.py -i $kk -o ./edited/$FN 2> /dev/null
    then
	echo $FN : $?
    fi
    
done
