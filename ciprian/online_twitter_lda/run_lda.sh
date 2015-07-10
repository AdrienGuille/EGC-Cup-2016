#!/usr/bin/env bash
#/bin/bash

#parameters
num_topics=10

#globals
dates_EN=`ls input_en/ | cut -f 1-1 -d \. | sort | uniq`
INPUT='input_en'
first=1
LANG=EN
prev=""
for date in $dates_EN
do
    echo "processing datetime = $date (previous datetime = $prev)"
    if [ $first -eq 1 ]
    then
        #run the first one without online
        out_dir=`echo $date | cut -f 2-2 -d-`
        time python lda.py -f $INPUT/$date.text -t $INPUT/$date.time -o output-EN-$out_dir -k $num_topics --language $LANG
        prev=$out_dir
    else
        time python lda.py -f $INPUT/$date.text -t $INPUT/$date.time -m output-EN-$prev/model.dat -o output-EN-$date --language $LANG
        prev=$date
    fi
    
    first=0
done


#globals
dates_FR=`ls input_fr/ | cut -f 1-1 -d \. | sort | uniq`
INPUT='input_fr'
first=1
LANG=FR
prev=""
for date in $dates_FR
do
    echo "processing datetime = $date (previous datetime = $prev)"
    if [ $first -eq 1 ]
    then
        #run the first one without online
        out_dir=`echo $date | cut -f 2-2 -d-`
        time python lda.py -f $INPUT/$date.text -t $INPUT/$date.time -o output-FR-$out_dir -k $num_topics --language $LANG
        prev=$out_dir
    else
        time python lda.py -f $INPUT/$date.text -t $INPUT/$date.time -m output-FR-$prev/model.dat -o output-FR-$date --language $LANG
        prev=$date
    fi

    first=0
done
