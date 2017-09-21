# findDuplicateFiles

This script finds duplicate files within 2 directories and move duplicates out. I have thousands of pictures and don't want to spend time organizing duplicates :).

Given 2 directories, the script recursively searches all files and subdirectories to find `.jpg`, `.jpeg`, and `.png` files. It then compares all files in the `original` directory tree with all files in the `check` directory tree and copies or moves duplicates out to a third folder. The results of the operations are written to `<duplicate folder>/results.txt`. 

By default it only copies the duplicates, but with the `-m` tag it can move them as well.

# Usage

	python findDupes.py -h

    usage: findDupes.py [-h] [-m] original check duplicates

    positional arguments:
      original    Parent directory with original files
      check       Parent directory with files to check for duplicates
      duplicates  Location to store all duplicates

    optional arguments:
      -h, --help  show this help message and exit
      -m, --move  Move the duplicates instead of copying them.

# Test Command

	mkdir duplicates
	python findDupes.py test1 test2 duplicates
