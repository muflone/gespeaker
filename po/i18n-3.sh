#!/bin/bash
for file in *.po
do
  msgmerge -U $file new/$file
done

for file in $(cat availables);
do (
  if [ -d $file ];
    then rm -r $file
  fi
  mkdir -p $file/LC_MESSAGES
  msgfmt --output-file=$file/LC_MESSAGES/gespeaker.mo $file.po
)
done
read
