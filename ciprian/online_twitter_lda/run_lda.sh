#!/usr/bin/env bash
#/bin/bash

#location of the input folders
dir=$1
#parameters
num_topics=$2

#globals
INPUT=$dir'/EN/input'
OUTPUT=$dir'/EN/output'
first=1
LANG=EN
prev=""
dates_EN=`ls $INPUT | cut -f 1-1 -d \. | sort | uniq`
for date in $dates_EN
do
    echo "processing datetime = $date (previous datetime = $prev)"
    if [ $first -eq 1 ]
    then
        #run the first one without online
        out_dir=`echo $date | cut -f 2-2 -d-`
        time python lda.py -f $INPUT/$date.text -t $INPUT/$date.time -o $OUTPUT$out_dir -k $num_topics --language $LANG
        prev=$out_dir
    else
        time python lda.py -f $INPUT/$date.text -t $INPUT/$date.time -m $OUTPUT$prev/model.dat -o $OUTPUT$date --language $LANG
        prev=$date
    fi
    first=0
done


#globals
INPUT=$dir'/FR/input'
OUTPUT=$dir'/FR/output'
first=1
LANG=FR
prev=""
dates_FR=`ls $INPUT | cut -f 1-1 -d \. | sort | uniq`
for date in $dates_FR
do
    echo "processing datetime = $date (previous datetime = $prev)"
    if [ $first -eq 1 ]
    then
        #run the first one without online
        out_dir=`echo $date | cut -f 2-2 -d-`
        time python lda.py -f $INPUT/$date.text -t $INPUT/$date.time -o $OUTPUT$out_dir -k $num_topics --language $LANG
        prev=$out_dir
    else
        time python lda.py -f $INPUT/$date.text -t $INPUT/$date.time -m $OUTPUT$prev/model.dat -o $OUTPUT$date --language $LANG
        prev=$date
    fi
    first=0
done
