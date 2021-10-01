import marshal
import sys
from tempfile import NamedTemporaryFile

from bc_printer import print_bc, get_bytecode, expand_bytecode
from os.path import exists
import py_compile


def usage():
	print("""
        This program ...
        compile
            -py file.py compile file into bytecode and store it as file.pyc
            -s "src" compile src into bytecode and store it as out.pyc
        print
            -py src.py produce human-readable bytecode from python file
            -pyc src.pyc produce human-readable bytecode from compiled .pyc file
            -s "src" produce human-readable bytecode from normal string""")


def compile(filenames, operand):
	for file in filenames:
		if not exists(file) and not operand == '-s':
			print(f"\tFile {file} does not exists")
			usage()
		else:
			if operand == '-py':
				try:
					py_compile.compile(file, cfile=file+'c')
				except Exception as e:
					print(e)
					print("Some errors occured, please check usage.")
			elif operand == '-s':
				with NamedTemporaryFile('w', delete=True) as tmp:
					tmp.write(file)
					tmp.seek(0)
					py_compile.compile(tmp.name, cfile='out.pyc')


def compare(filenames, operand):
	data = {}
	all_ins = []
	row_format = "{:13s}"
	for file in filenames:
		row_format += " | {:^13}"
		if not exists(file) and not operand == '-s':
			print(f"\tFile {file} does not exists")
			usage()
		else:
			if operand == '-py':
				source = open(file, 'r').read()
			elif operand == '-pyc':
				try:
					header = 12
					if sys.version_info >= (3, 7):
						header = 16
					with open(file, 'rb') as target:
						target.seek(header)
						source = marshal.load(target)
				except Exception as e:
					print(f"Skipping {file}, {e}")
			elif operand == '-s':
				source = file
			byte_code = get_bytecode(source)
			instructions = expand_bytecode(byte_code)
			all_ins += [x.opname for x in instructions]
			data[file] = [x.opname for x in instructions]
	table = {}
	all_ins = list(set(all_ins))
	for file in data:
		table[file] = {i: data[file].count(i) for i in data[file]}
	print(row_format.format('INSTRUCTION', *[x[:13] for x in filenames]))
	for ins in all_ins:
		atuple = []
		for file in data:
			try:
				atuple.append(table[file][ins])
			except:
				atuple.append(0)
		print(row_format.format(ins[:13], *atuple))


if __name__ == '__main__':
	command = sys.argv[1]
	operand = sys.argv[2]
	file = sys.argv[3:]
	if command == 'print':
		print_bc([file], operand)
	elif command == 'compile':
		compile([file], operand)
	elif command == 'compare':
		compare(file, operand)
	else:
		usage()
