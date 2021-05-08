import sys
from PyQt5 import QtWidgets

from vision.gui import VisionLabelling

def main():

    app = QtWidgets.QApplication(sys.argv)
    GUI = VisionLabelling()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()