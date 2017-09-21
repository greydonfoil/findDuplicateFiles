#!/usr/bin/python
import sys
import os
from glob import glob
import hashlib
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("original", help="Parent directory with original files", type=str)
parser.add_argument("check", help="Parent directory with files to check for duplicates", type=str)
parser.add_argument("duplicates", help="Location to store all duplicates", type=str)
parser.add_argument("-m", "--move", help="Move the duplicates instead of copying them.", action="store_true");

args = parser.parse_args()

BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

originalDir = args.original
checkDir = args.check
finalDir = args.duplicates

filetypes = ['.jpg', '.jpeg', '.png']

# Simple class to hold file info
class testFile:
    filename = ''
    sha1 = ''
    size = -1

    def __init__(self, filename):
        self.filename = filename
        self.shaFile()
        self.getSize()

    def shaFile(self):
        sha1 = hashlib.sha1()

        with open(self.filename, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha1.update(data)

        self.sha1 = sha1.hexdigest()

    def getSize(self):
        self.size =  os.path.getsize(self.filename)

    # Print the object
    def __str__(self):
        return " ".join((str(self.size), self.sha1, self.filename))

    def equals(self, comp):
        if self.sha1 == comp.sha1 and self.size == comp.size and self.filename != comp.filename:
            return True

        return False


def findFilesInDir(path, filetypes):
    files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*'))]

    retFiles = []

    for f in files:
        extension = os.path.splitext(os.path.basename(f))[1]

        if extension in filetypes:
            goodfile = testFile(f)
            # print "added",goodfile

            retFiles.append(goodfile)

    return retFiles

def compareFileSets(orig, comp):
    logfile = open(finalDir + "/results.txt", 'w');
    dupeCount = 0

    for f in orig:
        for c in comp:
            if f.equals(c):
                # print f.filename,"and", c.filename, "are equal. Moving."
                base = os.path.basename(c.filename)

                if args.move:
                    os.rename(c.filename, finalDir + "/" + base) # Move the file
                else:
                    shutil.copyfile(c.filename, finalDir + "/" + base) # Copy the file

                logfile.write(str(dupeCount) + " " + str(f)+"\n")
                logfile.write(str(dupeCount) + " " + str(c)+"\n\n")
                dupeCount += 1
    logfile.close()

    return dupeCount
                

if __name__ == "__main__":
    originalFiles = findFilesInDir(originalDir, filetypes)
    checkFiles = findFilesInDir(checkDir, filetypes)

    print "Original dir has {} files".format(len(originalFiles))
    print "Check dir has {} files".format(len(checkFiles))

    dupes = compareFileSets(originalFiles, checkFiles)
    if args.move:
        print "Moved {} dupes to {}".format(dupes, finalDir)
    else:
        print "Copied {} dupes to {}".format(dupes, finalDir)
