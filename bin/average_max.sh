#!/bin/bash

CURRENT_LINES=0
CURRENT_CHARS=0
CURRENT_FN=""
MAX_CHAR_FN=""
MAX_LINE_FN=""
MAX_LINES=0
MAX_CHARS=0
TOTAL_LINES=1
TOTAL_CHARS=1
FILECOUNT=0

# set -x

for KK in ../html/*.html
do
    CURRENT_FN=${KK}
    CURRENT_LINES=$( wc -l ${KK} | awk '{print $1}' )
    CURRENT_CHARS=$( wc -c ${KK} | awk '{print $1}'  )    
    if [ ${CURRENT_LINES} -gt ${MAX_LINES} ]
    then
	MAX_LINE_FN=${KK}
	MAX_LINES=${CURRENT_LINES}
    fi
    if [ ${CURRENT_CHARS} -gt ${MAX_CHARS} ]
    then
	MAX_CHAR_FN=${KK}
	MAX_CHARS=${CURRENT_CHARS}
    fi
    TOTAL_LINES=$(( ${TOTAL_LINES} + ${CURRENT_LINES} ))
    TOTAL_CHARS=$(( ${TOTAL_CHARS} + ${CURRENT_CHARS} ))
    FILECOUNT=$(( FILECOUNT + 1 ))
done


echo Number of html files: ${FILECOUNT}
echo Average Chars:$(( ${TOTAL_CHARS} / ${FILECOUNT} ))
echo Average Lines: $(( ${TOTAL_LINES} / ${FILECOUNT} ))
echo Maximum Lines: ${MAX_LINE_FN}   ${MAX_LINES}
echo Maximum Chars: ${MAX_CHAR_FN}   ${MAX_CHARS}


					  
    
