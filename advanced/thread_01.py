import math
from datetime import datetime

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


# for filename in filenames:
#     create_file(TEMP_DIR + filename)

s = datetime.now()
for i in range(300_000_000):
    x = math.sin(i)

print(datetime.now() - s)
