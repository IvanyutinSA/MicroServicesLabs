import glob
import sys
import os
import re


class TestRunner:
    def __init__(self):
        self.expand_dir()

    def expand_dir(self):
        path = os.path.abspath('.')
        if path not in sys.path:
            sys.path.append(path)

    def find_files(self):
        files = glob.glob('tests/**')
        files = [file for file in files if 'test_' in file]
        return files

    def do_everything(self, file):
        module = file.replace('/', '.')
        module = module[:-3]
        suits = []
        with open(file, 'r') as f:
            for line in f.readlines():
                test_suit = re.search(r'class\s+(.*)\s*\(TestSuit\)', line)
                if test_suit:
                    suits.append(test_suit.group(1))
        for test_suit in suits:
            try:
                exec(f'from {module} import {test_suit}\nwith {test_suit}() as test_class:\n    test_class()')
            except Exception:
                print(f'{test_suit} suit case \033[41mfailed\033[0m to run. path: {file}')  # ]]
                pass

    def run_tests(self):
        files = self.find_files()
        for file in files:
            self.do_everything(file)

    def __call__(self):
        self.run_tests()


if __name__ == '__main__':
    runner = TestRunner()
    runner()
