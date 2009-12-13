#!/bin/bash
if [ -f ../data/ui/*.glade.h ]
then
  rm ../data/ui/*.glade.h
fi
intltool-extract --type=gettext/glade ../data/ui/gespeaker.glade
intltool-extract --type=gettext/glade ../data/ui/preferences.glade

if ! [ -f gespeaker.pot ]
then
  touch gespeaker.pot
fi
xgettext --language=Python --keyword=_ --keyword=N_ --output gespeaker.pot --join-existing ../data/ui/*.glade.h ../src/*.py
rm ../data/ui/*.glade.h
read
