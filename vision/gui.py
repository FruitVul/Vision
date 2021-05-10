from PyQt5 import QtGui, QtWidgets,QtCore
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit,QPushButton, QCheckBox
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import shutil
import sys
import os
import PIL.Image as Image
import numpy as np

from vision.config import path_unlabled, path_labled, path_used, path_skipped
from vision.dop import get_from_folder


class VisionLabelling(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

        self.i_classified = 0

        self.setGeometry(50, 50, 800, 600)
        self.setFixedSize(800, 600)
        self.setWindowTitle("Vision")

        self.statusBar()

        mainMenu = self.menuBar()
        self.app = QtWidgets.QApplication(sys.argv)

        self.imgw = QtWidgets.QLabel(self)
        self.imgw.setGeometry(200, 0, 500, 500)
        self.image, self.gitter_id = self.set_image()
        self.home()

    def home(self):

        btn=QtWidgets.QPushButton("Quit", self)
        btn.clicked.connect(self.close_app)
        btn.resize(btn.minimumSizeHint())
        btn.move(30, 550)

        x_start = 150
        y_upper_row = 500
        y_lower_row = 530

        distance = 150

        classes = {"Freistehend": (x_start, y_upper_row),
                   "EFH/ZFH/DH": (x_start + distance*1, y_upper_row),
                   "MFH": (x_start + distance*2, y_upper_row),
                   "Zeilenbebauung": (x_start + distance*3, y_upper_row),
                   "Hochhäuser": (x_start, y_lower_row),
                   "Blockbebauung": (x_start + distance*1, y_lower_row),
                   "Industrie/Gewerbe": (x_start + distance*2, y_lower_row),
                   "L.schaft/Wasser": (x_start + distance*3, y_lower_row),
                   "Sonstiges": (x_start + distance*2 - 80, y_lower_row + 30)}

        i_cls = 0
        for cls, loc in classes.items():
            btn = QtWidgets.QPushButton(cls, self)
            btn.clicked.connect(lambda: self.classify(cl=i_cls))
            btn.move(loc[0], loc[1])
            i_cls += 1

        btn = QtWidgets.QPushButton("Skip", self)
        btn.clicked.connect(lambda: self.skip())
        btn.move(660, 450)

        self.textbox = QLineEdit(self)
        self.textbox.move(200, 460)
        self.textbox.resize(400, 25)
        self.update_textbox()

        self.show()

    def classify(self, cl):
        files_remaining = os.listdir(path=path_unlabled)
        self.i_classified += 1
        self.update_textbox()

        if len(files_remaining) > 0:
            img_save_name = f"{self.gitter_id}_{str(cl)}.png"
            self.image.save(os.path.join(path_labled, img_save_name))

            prev_img_path = os.path.join(path_unlabled, f"{self.gitter_id}.jpeg")
            new_img_path = os.path.join(path_used, f"{self.gitter_id}.jpeg")
            shutil.move(prev_img_path, new_img_path)
            self.image, self.gitter_id = self.set_image()

        else:
            print("No More files left!")

    def update_textbox(self):
        files_remaining = os.listdir(path=path_unlabled)
        self.textbox.setText(f"Files Remaing: {len(files_remaining)}, "
                             f"Classified this session: {self.i_classified}")

    def skip(self):
        files_remaining = os.listdir(path=path_unlabled)

        if len(files_remaining) > 0:
            prev_img_path = os.path.join(path_unlabled, f"{self.gitter_id}.jpeg")
            new_img_path = os.path.join(path_skipped, f"{self.gitter_id}.jpeg")
            shutil.move(prev_img_path, new_img_path)
            self.image, self.gitter_id = self.set_image()
            self.update_textbox()
        else:
            print("No more files left!")

    def close_app(self):
        choice = QtWidgets.QMessageBox.question(self,
                                                "Close",
                                                "Close application?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            print("Closing Application")
            sys.exit()
        else:
            pass

    def redo_id(self):
        pass

    def resize_all(self):
        pass

    def set_image(self):
        img_name = get_from_folder(path_unlabled)
        image = Image.open(os.path.join(path_unlabled, img_name))
        im = np.transpose(image, (1, 0, 2)).copy()
        qimage = QImage(im, im.shape[1], im.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        self.imgw.setPixmap(pixmap)
        return image, self.get_metadata(img_name)

    def get_metadata(self, img_name):
        gitter_id = img_name.split(".")[0]
        return gitter_id


