#!/bin/sh
HEADER=header.html
NAV=navigation.html
FOOTER=footer.html

# Parameter 1: Filename
file_check() {
    if [ ! -f "$1" ]; then
        echo "$1: No such file or directory" > /dev/stderr
        exit 1
    fi  
}

#main
BODY=$1
TARGET=$2

if [ $# -ne 2 ]; then
   echo "usage: pagebuild.sh <body> <pagename>" > /dev/stderr
fi

file_check $BODY
file_check $HEADER
file_check $FOOTER

echo "<!DOCTYPE html>"  > $TARGET
echo "<html lang=\"de\">" >> $TARGET 
cat $HEADER    >> $TARGET
echo "<body>"  >> $TARGET
cat $NAV       >> $TARGET
cat $BODY      >> $TARGET
cat $FOOTER    >> $TARGET 
echo "</body>" >> $TARGET
echo "</html>" >> $TARGET

