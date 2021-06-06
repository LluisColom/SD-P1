
import os
import json

def write_file(x):
	text_file = open("/home/cobra/Documents/output.txt", "w")
	text_file.write(x)
	text_file.close()
	return x

def print_function(x):
	print(x)

def countWords(x):
	return len(os.popen("curl "+x+" 2> /dev/null").read().split())

def wordCount(x):
	counts = dict()
	text = os.popen("curl "+x+" 2> /dev/null").read().split()

	for word in text:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1

	return json.dumps(counts)