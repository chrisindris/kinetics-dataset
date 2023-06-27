#!/bin/bash

count=0

split=$([[ $1 =~ (train|val|test) ]] && echo ${BASH_REMATCH[1]})

while read one;
do

	if [ $count -gt $(($2 - 1)) ] && [ $count -lt $(($3 + 1)) ]
	then

		archivename=$(basename -- "${one##*/}")
		archivename="${archivename%%.*}" # part_x, where x in {0, ..., n}; this is the .tar.gz archive


		echo "unzipping $archivename"	
		#tar zxf ${one##*/}

		DIRECTORY="/data/i5O/kinetics400/$split/${archivename}_resized"
		if [ -d "$DIRECTORY" ]; 
		then
			echo "$DIRECTORY exists."
		else
			echo "making directory $DIRECTORY"
			#mkdir $DIRECTORY
		fi



		for f in ./*.mp4
		do 
			echo "$f"
			#ffmpeg -loglevel quiet -y -i "$f" -vf "scale='if(gt(ih,iw),320,trunc(oh*a/2)*2):if(gt(ih,iw),trunc(ow/a/2)*2,320)'" "$DIRECTORY/$f" < /dev/null
		done


		echo "removing un-resized files"
		#rm ./*.mp4 
	fi	

count=$(( $count + 1 ))

done < $1
