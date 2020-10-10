import sys, getopt
from BroomCore import BroomCore
from ItemType import ItemType

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "df",["path=", "name="])
        _dir = False
        _file = False
        _path = ''
        _name = ''
        for opt, arg in opts:
            if (opt == '-d'):
                _dir = True
            elif (opt == '-f'):
                _file = True
            elif (opt == '--path'):
                _path = arg
            elif (opt == '--name'):
                _name = arg
        if (_path == ''):
            print("You must provide a non-empty path!")
            sys.exit(2)
        elif (_name == ''):
            print("You must provide the name of the file you are looking for!")
            sys.exit(2)
        elif (_dir == False and _file == False):
            print("You must choose what type of files you are looking for! [-d] for directories [-f] for files")
            sys.exit(2)
        _itemType = ItemType.both
        if (_dir == False and _file == True):
            _itemType = ItemType.file
        elif (_dir == True and _file == False):
            _itemType = ItemType.directory
        broom = BroomCore(_itemType, _path, _name)
        broom.search()
    except getopt.GetoptError:
        print('Invalid arguments!')
        sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])