#!/bin/bash

for kk in *.html
do
    if ! grep -i "viewport" $kk > /dev/null
    then
	echo $kk
    fi
done
