import os
import sys

src = sys.argv[1]
dest = sys.argv[2]
path = sys.argv[3]

fullSrc = path + "\\" + src

print(src)

dest = dest + "/"

folderPath = src.split("/")
print(dest + folderPath[len(folderPath) - 1])
