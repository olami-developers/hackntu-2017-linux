# !/bin/bash
echo "start pulse\n"
who
sleep 5
/usr/bin/pulseaudio -D
sleep 3

echo "start olamiMain\n"
cd $PWD;/usr/bin/python3 $PWD/olamiMain.py

sleep 100
wait

