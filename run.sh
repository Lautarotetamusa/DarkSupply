#!/bin/bash

Xvfb :10 -ac -screen 0 1024x768x8 &
export DISPLAY=:10
export PATH=$PATH:$(pwd)

val=$1
echo $val

cd $val"/"
pwd
nohup node $val".js" > "../logs/"$val"_log.txt" &
cd "../"
