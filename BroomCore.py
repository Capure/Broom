import os
import re
import sys
import shutil
from ItemType import ItemType
from prettytable import PrettyTable
from Question import Question

class BroomCore:
    def __init__(self, itemType, path, name):
        self.itemType = itemType
        self.path = path
        self.name = name

    def __scandir(self, dirname, counter):
        subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
        for dirname in list(subfolders):
            counter += 1
            if (counter % 2 == 0):
                print("\rScanning: \\", end="")
            else:
                print("\rScanning: /", end="")
            subfolders.extend(self.__scandir(dirname, counter))
        return subfolders

    def __findfiles(self, dirname, counter):
        if (counter % 2 == 0):
                print("\rScanning: \\", end="")
        else:
            print("\rScanning: /", end="")
        return [f.path for f in os.scandir(dirname) if f.is_file()]

    def __parse_path_dir(self, path_to_parse):
        temp = re.sub(self.name, f'{self.name}||||||||||', path_to_parse)
        return temp.split('||||||||||')[0] if temp != path_to_parse else ''

    def __parse_path_file(self, path_to_parse):
        return (path_to_parse.split('\\')[-1] == self.name)

    def __file_search(self):
        paths = []
        counter = 0
        for item in self.__scandir(self.path, 0):
            counter += 1
            for i in self.__findfiles(item, counter):
                if self.__parse_path_file(i):
                    paths.append(i)
        print("\r", end="")
        return [[ItemType.file, i] for i in paths]

    def __dir_search(self):
        paths = []
        for item in self.__scandir(self.path, 0):
            paths.append(self.__parse_path_dir(item))
        print("\r", end="")
        new_paths = []
        for item in paths:
            if item == '':
                continue
            found = False
            for i in new_paths:
                if item == i:
                    found = True
            if not found:
                new_paths.append(item)
        paths = new_paths
        return [[ItemType.directory, i] for i in paths]

    def __get_paths(self):
        if self.itemType == ItemType.file:
            return self.__file_search()
        elif self.itemType == ItemType.directory:
            return self.__dir_search()
        elif self.itemType == ItemType.both:
            paths = []
            for item in self.__file_search():
                paths.append(item)
            for item in self.__dir_search():
                paths.append(item)
            return paths
    
    def __delete(self, paths):
        counter = 0
        for path in paths:
            print(f"\rDeleting {counter}", end="")
            if path[0] == ItemType.file:
                os.remove(path[1])
            elif path[0] == ItemType.directory:
                shutil.rmtree(path[1])
            counter += 1
        print("\r")

    def search(self):
        paths = self.__get_paths()
        q = Question()
        while (True):
            t = PrettyTable(['Index', 'Type', 'Path'])
            counter = 0
            for item in paths:
                _type = "File" if item[0] == ItemType.file else "Dir"
                t.add_row([counter, _type, item[1]])
                counter += 1
            print(t)
            print("\n")
            opt = q.askInt("[0 - Edit, 1 - Delete, 2 - Quit]", limit=3)
            if opt == 2:
                sys.exit(0)
            elif opt == 0:
                stop = False
                while(not stop):
                    print("")
                    index = q.askInt("Index of an item you want to exclude", limit=counter)
                    paths.pop(index)
                    print(f"Broom won't touch item {index} anymore.")
                    t = PrettyTable(['Index', 'Type', 'Path'])
                    counter = 0
                    for item in paths:
                        _type = "File" if item[0] == ItemType.file else "Dir"
                        t.add_row([counter, _type, item[1]])
                        counter += 1
                    print(t)
                    print("")
                    stop = q.askBool("Are you done editing the items?")
                print("")
            else:
                break
        self.__delete(paths)
        print(f"\nDeleted {len(paths)} items.")
