set datafile separator ","

set term x11 1 noraise
set nokey 
unset ytics
unset xtics
set multiplot layout 9, 3

set title "rto" offset 0,-2
plot "current.csv" using 0:1 with lines
set title "rtt" offset 0,-2
plot "current.csv" using 0:2 with lines
set title "rtt" offset 0,-2
plot "current.csv" using 0:3 with lines
set title "ato" offset 0,-2
plot "current.csv" using 0:4 with lines
set title "mss" offset 0,-2
plot "current.csv" using 0:5 with lines
set title "rcvmss" offset 0,-2
plot "current.csv" using 0:6 with lines
set title "advmss" offset 0,-2
plot "current.csv" using 0:7 with lines
set title "cwnd" offset 0,-2
plot "current.csv" using 0:8 with lines
set title "bytes-acked" offset 0,-2
plot "current.csv" using 0:9 with lines
set title "bytes-received" offset 0,-2
plot "current.csv" using 0:10 with lines
set title "segs-out" offset 0,-2
plot "current.csv" using 0:11 with lines
set title "segs-in" offset 0,-2
plot "current.csv" using 0:12 with lines
set title "data-segs-out" offset 0,-2
plot "current.csv" using 0:13 with lines
set title "data-segs-in" offset 0,-2
plot "current.csv" using 0:14 with lines
set title "bbr-bw" offset 0,-2
plot "current.csv" using 0:15 with lines
set title "bbr-mrtt" offset 0,-2
plot "current.csv" using 0:16 with lines
set title "bbr-pacing-gain" offset 0,-2
plot "current.csv" using 0:17 with lines
set title "bbr-cwnd-gain" offset 0,-2
plot "current.csv" using 0:18 with lines
set title "send" offset 0,-2
plot "current.csv" using 0:19 with lines
set title "lastsnd" offset 0,-2
plot "current.csv" using 0:20 with lines
set title "lastrcv" offset 0,-2
plot "current.csv" using 0:21 with lines
set title "lastack" offset 0,-2
plot "current.csv" using 0:22 with lines
set title "pacing-rate" offset 0,-2
plot "current.csv" using 0:23 with lines
set title "delivery-rate" offset 0,-2
plot "current.csv" using 0:24 with lines
set title "rcv-rtt" offset 0,-2
plot "current.csv" using 0:25 with lines
set title "rcv-space" offset 0,-2
plot "current.csv" using 0:26 with lines
set title "minrtt" offset 0,-2
plot "current.csv" using 0:27 with lines

unset multiplot

pause 1
reread
