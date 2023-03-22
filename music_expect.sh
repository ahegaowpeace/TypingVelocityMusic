#!/bin/bash
# trap処理
trap 'klps=`ps -ef | grep key.py | grep -v grep | tr -s " " | cut -d " " -f 2`;kill $klps;echo "" > expect.txt' 2 15

python3.6 key.py &

expect -c "
set timeout -1
set OUTFILE_PATH \"expect.txt\"
spawn vlc -I rc ~/音楽/
sleep 1
send \n

while {true} {
	#2秒毎に速度チェックしてコマンド決定
	set OUTFILE [exec cat \"\${OUTFILE_PATH}\"]
	sleep 2
	expect -re \">.*\"
	#set OUTFILE \"next\"
	send \$OUTFILE
	send \n
}
expect eof exit 0
"
