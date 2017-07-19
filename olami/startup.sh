# !/bin/bash
echo "start pulse\n"
who
sleep 5
/usr/bin/pulseaudio -D
sleep 3

echo "start olamiMain\n"
cd /home/pi/olami/;/usr/bin/python3 /home/pi/olami/olamiMain.py

sleep 100
wait

