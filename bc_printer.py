import sys
import dis
import marshal
from os.path import exists


def usage():
	print("""
        Usage: bc_printer.py -py <filename>
               bc_printer.py -pyc <filename>
               bc_printer.py -s "python code"
        This program generates an opcodes that are passed to PVM from source code.""")


def expand_bytecode(bytecode):
	res = []
	for instruction in bytecode:
		if str(type(instruction.argval)) == "<class 'code'>":
			res += expand_bytecode(get_bytecode(instruction.argval))
		else:
			res.append(instruction)
	return res


def get_bytecode(code):
	return dis.Bytecode(code)


def print_bc(filenames, operand):
	for file in filenames:
		if not exists(file) and not operand == '-s':
			print(f"\tFile {file} does not exists")
			usage()
		else:
			if operand == '-py':
				print('filename is', file)
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
			for instruction in instructions:
				print(f"{instruction.opname} \t {instruction.argrepr}")


if __name__ == '__main__':
	operand = sys.argv[1]
	filenames = sys.argv[2:]
	print_bc(filenames, operand)
