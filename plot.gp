reset
set term png enhanced font 'Verdana,10'
set style fill solid
set output 'soildata.png'
set xtics rotate by -90
set xtics 10
set grid x
set title "Last Run: " .strftime("%a %b %d %H:%M", time(0)+28800)


plot [:][0:130] 'soildata.txt' using ($0):4:xtic(2) with linespoints linewidth 2 title 'temperature', \
'' using ($0):5:xtic(2) with linespoints linewidth 2 title 'humidity', \
'' using ($0):($4+0.3):3 with labels center offset 0,char 3 notitle, \
'' using ($0):($5):5 with labels center offset 0,1 rotate by -45 notitle, \
'' using ($0):($4):4 with labels center offset 0,1 rotate by -45 notitle
