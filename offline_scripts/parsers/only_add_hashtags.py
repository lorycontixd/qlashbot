#add hashtags to tags
import sys

assert len(sys.argv)==3
filename_input = sys.argv[1]
filename_output = sys.argv[2]


def read_file(filename_in):
	file = open(filename_in,'r+')
	content = file.read()
	lines = content.split('\n')
	list = []
	for i in range(len(lines)):
		tag='#'
		temp=lines[i]
		temp=temp.replace('O','0')
		tag+=temp
		list.append(str(tag))
	return list

def write_to_file(list,filename_output):
	file = open(filename_output,'a+')
	for item in list:
		file.write(item+'\n')

def main_program(iin,out):
	list = read_file(iin)
	write_to_file(list,out)

main_program(filename_input,filename_output)

	
	