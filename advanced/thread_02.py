from datetime import datetime
from threading import Thread

COUNT = 10
TEMP_DIR = "d:/temp/"
FN_PREFIX = "big_file"
FN_POSTFIX = "txt"
FN_COPY = "copy"



filenames = [f"{FN_PREFIX}_{num}.{FN_POSTFIX}" for num in range(COUNT)]
print(filenames)

def create_file(filename):
    with open(filename, "w") as f:
        f.write("0" * 1024 * 1024 * 100)

def copy_file(filename):
    with open(filename, "r") as f:
        f.read()


for filename in filenames:
    create_file(TEMP_DIR + filename)

s = datetime.now()
thread_list = [Thread(target=copy_file, args=(TEMP_DIR + filename,)) for filename in filenames]
for thread in thread_list:
    thread.start()

for thread in thread_list:
    thread.join()

print(datetime.now() - s)
