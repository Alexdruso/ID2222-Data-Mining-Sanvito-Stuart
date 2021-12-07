#set terminal postscript eps enhanced color font "Helvetica,18"  #monochrome
#set output '| ps2pdf - graph.eps'

set term png small size 1024,786
set output 'graph.png'



set style line 1 lc rgb "#1a9850" lw 1.5
set style line 2 lc rgb "black" lw 1.5
set style line 3 lc rgb "brown" lw 1.5
set style line 4 lc rgb "green" lw 1.5
set style line 5 lc rgb "orange" lw 1.5
set style line 6 lc rgb "#d73027" lw 1.5

set multiplot layout 3,1 title filename  font ",14"
set yrange [0:]

set ylabel "Edge Cut" 
set xlabel "Rounds" 
plot filename using 1:2 with l ls 1 title "Edge-Cut"
set ylabel "Swaps" 
set xlabel "Rounds" 
plot filename using 1:3 with l ls 2 title "Swaps"
set ylabel "Migrations" 
set xlabel "Rounds" 
plot filename using 1:4 with l ls 3 title "Migrations"

unset multiplot


