set term svg size 800,600 fixed enhanced font 'Arial,18'

set key off

set boxwidth 0.5
set style fill solid
set style line 1 linecolor rgb '#8A2BE2'

set title 'Total Hours Spent Versus Activity'
set xlabel 'Activity'
set ylabel 'Hours Spent'

plot '/dev/stdin' using 1:2:xtic(3) with boxes linestyle 1
