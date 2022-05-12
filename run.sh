#!/bin/bash

#Cargamos la pantalla virtual
xvfb=$(pgrep Xvfb)
if [ -z "$xvfb" ]; then
  Xvfb :10 -ac -screen 0 1024x768x8 &
  echo "ejecutando Xvfb $!"
else
  echo "Xvfb ya esta ejecutandose"
fi
export DISPLAY=:10

export PATH=$PATH:$(pwd)
echo $PATH

val=$1
echo $val

cd $val"/"
nohup node $val".js" > "../logs/"$val"_log.txt" &
cd "../"
