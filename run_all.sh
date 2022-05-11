#!/bin/bash

echo "Iniciando monitores..."

#Cargamos la pantalla virtual
xvfb=$(pgrep Xvfb)
if [ -z "$xvfb" ]; then
  Xvfb :10 -ac -screen 0 1024x768x8 &
  echo "ejecutando Xvfb $!"
else
  echo "Xvfb ya esta ejecutandose"
fi
export DISPLAY=:10

#Exportamos el path para que contenga el geckodriver
export PATH=$PATH:$(pwd)

#Reiniciamos el archivo pidfile
cat "/dev/null" > pidfile.txt

nohup node "main.js" > "logs/main_log.txt" &
echo "main "$! >> pidfile.txt
echo "main iniciado con pid $!"

declare -a StringArray=("nike" "snkrs" "bold" "shockdrops")

# Iterate the string array using for loop
for val in ${StringArray[@]}; do
   echo "Iniciando $val"
   cd $val"/"
   nohup node $val".js" > "../logs/"$val"_log.txt" &
   cd "../"
   echo "$val "$! >> pidfile.txt
   echo "$val iniciado con pid $!"
   sleep 15 #Esperamos entre monitores para que no se lagee el server
done
