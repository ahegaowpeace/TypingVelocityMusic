# バイナリファイル構造体
# struct input_event {
# 	struct timeval time;
# 	unsigned short type;
# 	unsigned short code;
# 	unsigned int value;
# };

infile_path = "/dev/input/event12"
V_ZERO = 4
count = 0

# thread_1
# キーイベント処理部分
#
import struct
import re
EVENT_FORMAT = "llHHI";
EVENT_SIZE = struct.calcsize(EVENT_FORMAT)

def keyfunc():
	global count
	with open(infile_path, "rb") as file:
		while True:
			event = file.read(EVENT_SIZE)
			strtmp = struct.unpack(EVENT_FORMAT, event)[3:]
			listtmp = strtmp
			if listtmp[0] != 0 and listtmp[1] == 0:
				count = count + 1

# thread_2
# ラップ処理部分
#
import time
expfile_path = '~/py/monokon/union/expect.txt'

def timerfunc():
	global count
	btime = time.time()
	while True:
		ntime = time.time()
		if (ntime - btime >= 2):
			vel = (count / round(ntime - btime))
			if (vel < 3):
				with open(expfile_path, mode='w') as f:
					f.write('key key-rate-slower-fine\n')
			elif (3 <= vel and vel <= 5):
				with open(expfile_path, mode='w') as f:
					f.write('\n')
			else:
				with open(expfile_path, mode='w') as f:
					f.write('key key-rate-faster-fine\n')
			btime = time.time()
			count = 0

# main
import threading

if __name__ == "__main__":
	thread_1 = threading.Thread(target=keyfunc)
	thread_2 = threading.Thread(target=timerfunc)

	thread_1.start()
	thread_2.start()
