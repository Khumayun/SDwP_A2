import sys
import timeit
import subprocess
import os


def usage():
    print("""
        Usage: compare.py [filenames]
        This program compares execution time of individual .py scripts""")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if list(set([os.path.exists(file) for file in sys.argv[1:]]))[0]:
            result = {}
            for file in sys.argv[1:]:
                timer = timeit.timeit(lambda : subprocess.run(['python3', file], capture_output=True), number=1)
                result[file] = timer
            result = sorted(result.items(), key = lambda item: item[1])
            print('PROGRAM | RANK | TIME ELAPSED')
            for i, row in enumerate(result, 1):
                print(row[0], ' ', i, '\t', str(row[1])[:6]+'s')
        else:
            print('The list of arguments is incorrect. Please check usage by running cumpare.py without arguments.')
    else:
        usage()
