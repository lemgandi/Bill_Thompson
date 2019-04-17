#!/bin/bash

OUTFILE=./test_abend_out.txt

if [ -f ${OUTFILE} ]
then
    rm ${OUTFILE}
fi

for kk in ../html/*.html
do
    FN=$(basename $kk)
    ./urlshifter.py -i $kk -o ./edited/$FN >> ${OUTFILE}
    ERRORVAL=$?
    if [ ${ERRORVAL} -gt 0 ]
    then
	echo $FN : ${ERRORVAL}
    fi
    
done
