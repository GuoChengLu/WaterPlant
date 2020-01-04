#/bin/bash
python soiltest.py
gnuplot plot.gp
scp soildata.png luguocheng@192.168.43.72:/Users/luguocheng/Documents/test/
