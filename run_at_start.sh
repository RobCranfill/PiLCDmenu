#!/usr/bin/bash
# run the menu system at startup
pid_file="process.pid"

cd /home/pi/proj/PiLCDmenu/
python3 ./lcd_menu_example.py &

echo kill -SIGUSR1 $! > $pid_file
