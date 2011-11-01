#!/usr/bin/python

import os
import re
import sys
import easygui

def file_replace(fname, pattern, mobile_after):
	# first, see if the patterntern is even in the file.
	with open(fname) as f:
		if not any(re.search(pattern, line) for line in f):
			return

	# patterntern is in the file, so perform replace operation.
	with open(fname) as f:
		out_fname = fname + ".tmp"
		out = open(out_fname, "w")
		for line in f:
			print line
			out.write(re.sub(pattern, mobile_after, line))
		f.close()
                os.remove(fname)
		out.close()
		os.rename(out_fname,fname)


def replace_vcf(mobile_before, mobile_after, dir_name):
	pattern = re.compile(mobile_before , re.MULTILINE)
	for dirpath, dirnames, filenames in os.walk(dir_name):
		for fname in filenames:
			fullname = os.path.join(dirpath, fname)
			file_replace(fullname, pattern, mobile_after)

def main():
	dir_name = str(easygui.diropenbox(title="please choose contacts folder"))
	dict = {
			"01([2|7|8]{1})([0-9]{7})(\r|\n)$": r"012\1\2\3",
			"01([0|9|6]{1})([0-9]{7})(\r|\n)$": r"010\1\2\3",
			"01([1|4]{1})([0-9]{7})(\r|\n)$": r"011\1\2\3",
			"0150([0-9]{7})(\r|\n)$": r"0120\1\2",
			"0151([0-9]{7})(\r|\n)$": r"0101\1\2",
			"0152([0-9]{7})(\r|\n)$": r"0112\1\2"
			}
	if dir_name != 'None' :
		msg = "Are you sure you wanna update cellphone numbers in " + dir_name
		title = "Please Confirm"
		if easygui.ccbox(msg, title):
			for key in dict:
				replace_vcf(key, dict[key], dir_name)
			easygui.msgbox("Contacts have been updated successfully :) ")
		else:
			sys.exit(0)
	else:
		sys.exit(0)

if __name__ == "__main__":
    main()