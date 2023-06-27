#!/bin/bash

part=0

while read one;
do

archivename=$(basename -- "${one##*/}")
archivename="${archivename%%.*}"
archivenum="${archivename:5}"

split=$([[ $1 =~ (train|val|test) ]] && echo ${BASH_REMATCH[1]})

	if [ $archivenum -gt $(($2 - 1)) ] && [ $archivenum -lt $(($3 + 1)) ]
	then 
    		echo "./${one##*/}"
		echo "$split"
    		mv "./${one##*/}" "/data/i5O/kinetics400/${split}3/"
	fi

	part=$(( $part + 1))

done < $1

