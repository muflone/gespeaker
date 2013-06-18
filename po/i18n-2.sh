#!/bin/bash
INITOPTS="--input=new/gespeaker.pot --no-translator"
msginit $INITOPTS --output-file=new/en_US.po --locale=en_US
msginit $INITOPTS --output-file=new/it.po --locale=it_IT
msginit $INITOPTS --output-file=new/fr.po --locale=fr_FR
msginit $INITOPTS --output-file=new/es.po --locale=es_ES
msginit $INITOPTS --output-file=new/ru.po --locale=ru_RU
msginit $INITOPTS --output-file=new/eu.po --locale=eu
msginit $INITOPTS --output-file=new/ar.po --locale=ar
msginit $INITOPTS --output-file=new/bg.po --locale=bg
msginit $INITOPTS --output-file=new/cs.po --locale=cs
msginit $INITOPTS --output-file=new/da.po --locale=da
msginit $INITOPTS --output-file=new/de.po --locale=de_DE
msginit $INITOPTS --output-file=new/he.po --locale=he
msginit $INITOPTS --output-file=new/hu.po --locale=hu
msginit $INITOPTS --output-file=new/ja.po --locale=ja
msginit $INITOPTS --output-file=new/nl.po --locale=nl_NL
msginit $INITOPTS --output-file=new/pl.po --locale=pl
msginit $INITOPTS --output-file=new/pt.po --locale=pt_PT
msginit $INITOPTS --output-file=new/sk.po --locale=sk
msginit $INITOPTS --output-file=new/tr.po --locale=tr
msginit $INITOPTS --output-file=new/zh_CN.po --locale=zh_CN
msginit $INITOPTS --output-file=new/fo.po --locale=fo

read
