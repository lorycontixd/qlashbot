#data from game.tv (copy-paste)
import sys
assert len(sys.argv)==3
input_filename = str(sys.argv[1])
destination_filename = str(sys.argv[2])

def read_file(filename_in):
	file = open(filename_in,'r+')
	content = file.read()
	lines = content.split('\n')
	list=[]
	file.close()
	for line in lines:
		ll=line.split('\t')
		name=ll[0]
		ll2=name.split('#')
		tag='#'
		temp=str(ll2[1]).replace('O','0')
		temp=temp.replace(" ","")
		tag+=temp	
		list.append(tag)
	return list

def write_to_file(list,filename_dest):
	file = open(filename_dest,'a+')
	for i in range(len(list)):
		file.write(list[i]+'\n')

def main_program(filename_input,filename_destination):
	list = read_file(filename_input)
	write_to_file(list,filename_destination)

main_program(input_filename,destination_filename)
	