import os
from pathlib import Path


def main():
    path = Path('~/grafika/Różne/').expanduser()
    for file in path.iterdir():
        if file.is_dir():
            print('DIR FOUND', file)
            continue

        if '~' in file.name:
            new_name = file.name.replace('~', '')
            print('renaming', file.name, 'or', file.absolute(), 'to', new_name)
            file.rename(new_name)
            print('new name is', file.absolute())
    print(os.getcwd())


if __name__ == '__main__':
    main()
