#! /bin/bash

filelist=(`ls $1|grep -v diff|tail -2`)
echo ${#filelist[@]}
if [[ ${#filelist[@]} -ge 2 ]]
then
sdiff -l $1/${filelist[1]} $1/${filelist[0]} > $1/${filelist[1]}\_${filelist[0]}.diff.txt
else
exit
fi

