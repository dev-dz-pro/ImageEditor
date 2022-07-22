from tkinter import image_names
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter
from PyQt5.QtWidgets import QMessageBox
import os
from io import BytesIO
from skew import skew_im
from fpdf import FPDF


class Stresh1(QtWidgets.QLabel):
    def __init__(self):
        super(Stresh1, self).__init__()
        self.scaled_rate_1_w = 1.0
        self.scaled_rate_1_h = 1.0

    def load_image(self):
        self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(),"Image files (*.png *.jpg *.gif)")
        image = QtGui.QImage(self.fname[0])
        self.scaled_rate_1_w = 1.0
        self.scaled_rate_1_h = 1.0
        if image.width() > 779 or image.height() > 779:
            self.setFixedSize(QtCore.QSize(779, 779))
            self.setScaledContents(True)
            if image.width() > self.width():
                self.scaled_rate_1_w = image.width() / self.width()
            else:
                self.scaled_rate_1_w = 1.0
            if image.height() > self.height():
                self.scaled_rate_1_h = image.height() / self.height()
            else:
                self.scaled_rate_1_h = 1.0
        else:
            self.setFixedSize(image.size())
            self.setScaledContents(False)
        self.setPixmap(QtGui.QPixmap.fromImage(image))
        

    def mousePressEvent (self, eventQMouseEvent):
        try:
            self.currentQRubberBand.hide()
            self.currentQRubberBand.deleteLater()
        except:
            pass
        self.originQPoint = eventQMouseEvent.pos()
        self.currentQRubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
        self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, QtCore.QSize()))
        self.currentQRubberBand.show()

    def mouseMoveEvent (self, eventQMouseEvent):
        self.currentQRubberBand.setGeometry(QtCore.QRect(self.originQPoint, eventQMouseEvent.pos()).normalized())



class Stresh2(QtWidgets.QLabel):
    
    DELTA = 30 #for the minimum distance   default were 10  
    def __init__(self):
        super(Stresh2, self).__init__()
        self.is_expanded = False # self.setStyleSheet("border: 2px solid black;") # self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)


    def set_ui(self, bitmax, pad):
        self.draggin_idx = -1 
        self.setScaledContents(True)
        self._image = bitmax

        if bitmax.width() > 551:
            self.scaled_w = bitmax.width() / 551
        else:
            self.scaled_w = 1.0
        if bitmax.height() > 779:
            self.scaled_h = bitmax.height() / 779
        else:
            self.scaled_h = 1.0
        
        self.chosen_points = np.array([[pad, pad],[(bitmax.width()/self.scaled_w)-pad, pad],[(bitmax.width()/self.scaled_w)-pad, 
                                    (bitmax.height()/self.scaled_h)-pad], [pad, (bitmax.height()/self.scaled_h)-pad]], dtype=np.float64) 
        self.setPixmap(bitmax)
        
        
    def paintEvent(self, paint_event):
        try:
            painter = QtGui.QPainter(self)
            painter.drawPixmap(self.rect(), self._image)
            qpnt = []
            for pos in self.chosen_points:
                qpnt.append(QtCore.QPoint(pos[0], pos[1]))
            points = QtGui.QPolygon(qpnt)
            pen2 = QtGui.QPen(QtGui.QColor(255, 50, 50, 120), 3, QtCore.Qt.DashLine)
            painter.setPen(pen2)
            painter.drawPolygon(points) # painter.drawLine(100, 100, 400, 400)
            pen = QtGui.QPen(QtGui.QColor(255, 50, 50, 255), 15, QtCore.Qt.SolidLine)
            painter.setPen(pen) # painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            painter.drawPoints(qpnt)
        except Exception as e:
            print("error", str(e))

   
    def _get_point(self, evt):
        return np.array([evt.pos().x(),evt.pos().y()])


    def mousePressEvent(self, evt):
        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx == -1:
            point = self._get_point(evt)
            #dist will hold the square distance from the click to the points
            dist = self.chosen_points - point
            dist = dist[:,0]**2 + dist[:,1]**2
            dist[dist>self.DELTA] = np.inf #obviate the distances above DELTA
            if dist.min() < np.inf:
                self.draggin_idx = dist.argmin() 


    def mouseMoveEvent(self, evt):
        if self.draggin_idx != -1:
            point = self._get_point(evt)
            self.chosen_points[self.draggin_idx] = point
            self.update()
            


    def mouseReleaseEvent(self, evt):
        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx != -1:
            point = self._get_point(evt)
            self.chosen_points[self.draggin_idx] = point
            self.draggin_idx = -1
            self.update() 




class Ui_MainWindow(object):  
    def setupUi(self, MainWindow):
        MainWindow.resize(1525, 840) # MainWindow.showMaximized()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1500, 800)) # QtCore.QRect(10, 10, 1550, 850)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_1 = Stresh1()
        self.label_1.setStyleSheet("background-color: white;")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        # self.label_1.setMinimumSize(QtCore.QSize(10, 10))
        self.label_1.setFixedSize(QtCore.QSize(779, 779))

        self.horizontalLayout.addWidget(self.label_1, stretch=4, alignment=QtCore.Qt.AlignCenter)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.verticalLayout.addWidget(self.label_3, stretch=1, alignment=QtCore.Qt.AlignCenter)
        self.btn_load = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_load.setStyleSheet("QPushButton {\n"
        "    color: #333;\n"
        "    border: 1px solid #555;\n"
        "    border-radius: 5px;\n"
        "    border-style: outset;\n"
        "    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(177, 177, 177, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "    padding: 5px;\n"
        "    }\n"
        "\n"
        "QPushButton:hover {\n"
        "    background: qradialgradient(\n"
        "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
        "        );\n"
        "    }\n"
        "\n"
        "QPushButton:pressed {\n"
        "    border-style: inset;\n"
        "    background: qradialgradient(\n"
        "        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
        "        );\n"
        "    }")
        self.btn_load.setFixedWidth(100)
        self.btn_load.clicked.connect(self.on_load_image)
        self.verticalLayout.addWidget(self.btn_load, stretch=1, alignment=QtCore.Qt.AlignCenter)
        self.line_5 = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_5)
        self.btn_crop = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_crop.setStyleSheet(
                "QPushButton {\n"
                "    background-image: url(icons/crop0.png);\n"
                "    background-color: transparent;\n"
                "    height: 64px;\n"
                "    height: 64px;\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    }\n"
                "QPushButton:hover {\n"
                "    background-image: url(icons/crop1.png);\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    height: 70px;\n"
                "    height: 70px;\n"
                "    }\n")
        self.btn_crop.clicked.connect(self.on_crop_image)
        self.verticalLayout.addWidget(self.btn_crop, stretch=1)

        self.btn_angl = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_angl.setStyleSheet(
                "QPushButton {\n"
                "    background-image: url(icons/angle0.png);\n"
                "    background-color: transparent;\n"
                "    height: 64px;\n"
                "    height: 64px;\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    }\n"
                "QPushButton:hover {\n"
                "    background-image: url(icons/angle1.png);\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    height: 70px;\n"
                "    height: 70px;\n"
                "    }\n")
        self.btn_angl.clicked.connect(self.correct_input_angle)
        self.verticalLayout.addWidget(self.btn_angl, stretch=1)

        self.btn_blur = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_blur.setStyleSheet(
                "QPushButton {\n"
                "    background-image: url(icons/blur0.png);\n"
                "    background-color: transparent;\n"
                "    height: 64px;\n"
                "    height: 64px;\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    }\n"
                "QPushButton:hover {\n"
                "    background-image: url(icons/blur1.png);\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    height: 70px;\n"
                "    height: 70px;\n"
                "    }\n")
        self.btn_blur.clicked.connect(self.on_blur_image)
        self.verticalLayout.addWidget(self.btn_blur, stretch=1)

        self.line_4 = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_4)

        self.btn_rotate1 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_rotate1.setStyleSheet("QPushButton {\n"
        "    color: #333;\n"
        "    border: 1px solid #555;\n"
        "    border-radius: 5px;\n"
        "    border-style: outset;\n"
        "    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(177, 177, 177, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "    padding: 5px;\n"
        "    }\n"
        "\n"
        "QPushButton:hover {\n"
        "    background: qradialgradient(\n"
        "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
        "        );\n"
        "    }\n"
        "\n"
        "QPushButton:pressed {\n"
        "    border-style: inset;\n"
        "    background: qradialgradient(\n"
        "        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
        "        );\n"
        "    }")
        self.btn_rotate1.setFixedWidth(100)
        self.btn_rotate1.clicked.connect(lambda : self.on_rotate_image(True))
        self.verticalLayout.addWidget(self.btn_rotate1, stretch=1, alignment=QtCore.Qt.AlignCenter)
        self.btn_rotate2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_rotate2.setStyleSheet("QPushButton {\n"
        "    color: #333;\n"
        "    border: 1px solid #555;\n"
        "    border-radius: 5px;\n"
        "    border-style: outset;\n"
        "    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(177, 177, 177, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "    padding: 5px;\n"
        "    }\n"
        "\n"
        "QPushButton:hover {\n"
        "    background: qradialgradient(\n"
        "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
        "        );\n"
        "    }\n"
        "\n"
        "QPushButton:pressed {\n"
        "    border-style: inset;\n"
        "    background: qradialgradient(\n"
        "        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
        "        );\n"
        "    }")
        self.btn_rotate2.setFixedWidth(100)
        self.btn_rotate2.clicked.connect(self.on_rotate_image)
        self.verticalLayout.addWidget(self.btn_rotate2, stretch=1, alignment=QtCore.Qt.AlignCenter)

        
        self.btn_fliph = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_fliph.setStyleSheet("QPushButton {\n"
        "    color: #333;\n"
        "    border: 1px solid #555;\n"
        "    border-radius: 5px;\n"
        "    border-style: outset;\n"
        "    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(177, 177, 177, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "    padding: 5px;\n"
        "    }\n"
        "\n"
        "QPushButton:hover {\n"
        "    background: qradialgradient(\n"
        "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
        "        );\n"
        "    }\n"
        "\n"
        "QPushButton:pressed {\n"
        "    border-style: inset;\n"
        "    background: qradialgradient(\n"
        "        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
        "        );\n"
        "    }")
        self.btn_fliph.setFixedWidth(100)
        self.btn_fliph.clicked.connect(lambda: self.on_flip(direction="horizontal"))
        self.verticalLayout.addWidget(self.btn_fliph, stretch=1, alignment=QtCore.Qt.AlignCenter)

        self.btn_flipv = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_flipv.setStyleSheet("QPushButton {\n"
        "    color: #333;\n"
        "    border: 1px solid #555;\n"
        "    border-radius: 5px;\n"
        "    border-style: outset;\n"
        "    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(177, 177, 177, 255), stop:1 rgba(255, 255, 255, 255));\n"
        "    padding: 5px;\n"
        "    }\n"
        "\n"
        "QPushButton:hover {\n"
        "    background: qradialgradient(\n"
        "        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
        "        );\n"
        "    }\n"
        "\n"
        "QPushButton:pressed {\n"
        "    border-style: inset;\n"
        "    background: qradialgradient(\n"
        "        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
        "        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
        "        );\n"
        "    }")
        self.btn_flipv.setFixedWidth(100)
        self.btn_flipv.clicked.connect(lambda: self.on_flip(direction="vertical"))
        self.verticalLayout.addWidget(self.btn_flipv, stretch=1, alignment=QtCore.Qt.AlignCenter)

        self.line_3 = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_3)
        self.btn_center = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_center.setStyleSheet(
                "QPushButton {\n"
                "    background-image: url(icons/center0.png);\n"
                "    background-color: transparent;\n"
                "    height: 64px;\n"
                "    height: 64px;\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    }\n"
                "QPushButton:hover {\n"
                "    background-image: url(icons/center1.png);\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    height: 70px;\n"
                "    height: 70px;\n"
                "    }\n")
        self.btn_center.clicked.connect(self.on_center_image)
        self.btn_center.setIconSize(QtCore.QSize(64,64))
        self.verticalLayout.addWidget(self.btn_center, stretch=1)
        self.line_2 = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line_2)
        self.btn_expand = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_expand.setStyleSheet(
                "QPushButton {\n"
                "    background-image: url(icons/expand0.png);\n"
                "    background-color: transparent;\n"
                "    height: 64px;\n"
                "    height: 64px;\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    }\n"
                "QPushButton:hover {\n"
                "    background-image: url(icons/expand1.png);\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    height: 70px;\n"
                "    height: 70px;\n"
                "    }\n")
        self.btn_expand.clicked.connect(self.on_expand_image)
        self.verticalLayout.addWidget(self.btn_expand, stretch=1)
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.btn_save = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_save.setStyleSheet(
                "QPushButton {\n"
                "    background-image: url(icons/save0.png);\n"
                "    background-color: transparent;\n"
                "    height: 64px;\n"
                "    height: 64px;\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    }\n"
                "QPushButton:hover {\n"
                "    background-image: url(icons/save1.png);\n"
                "    background-repeat: no-repeat;\n"
                "    background-position: center;\n"
                "    height: 70px;\n"
                "    height: 70px;\n"
                "    }\n")
        self.btn_save.clicked.connect(lambda: self.on_save_image(pad=0.0))
        self.verticalLayout.addWidget(self.btn_save, stretch=1)

        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.verticalLayout.addWidget(self.label, stretch=1, alignment=QtCore.Qt.AlignCenter)
        self.horizontalLayout.addLayout(self.verticalLayout, stretch=1)
        self.label_2 = Stresh2() 
        
        self.label_2.setMinimumSize(QtCore.QSize(10, 10))
        self.label_2.setMaximumSize(QtCore.QSize(551, 779))
        
        

        self.wdg = QtWidgets.QWidget()
        self.wdg.setStyleSheet("QWidget {\n"
        "    border : 1px solid grey;\n"
        "    border-radius : 5px;\n"
        "    margin: 0px;\n"
        "    padding: 0px;\n"
        "    background-color: white;\n"
        "}")
        
        self.cstum_lyt = QtWidgets.QVBoxLayout()
        self.cstum_lyt.addWidget(self.label_2, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, stretch=0)
        self.wdg.setFixedSize(QtCore.QSize(580, 805)) # + 21 for border
        self.wdg.setLayout(self.cstum_lyt)

        self.horizontalLayout.addWidget(self.wdg, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, stretch=5) # self.horizontalLayout.addWidget(self.label_2, alignment=QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter, stretch=5)
        MainWindow.setCentralWidget(self.centralwidget)


        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1110, 21))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.actionclose = QtWidgets.QAction(MainWindow)
        self.menuFile.addAction(self.actionclose)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_load.setText(_translate("MainWindow", "Load Image"))
        self.btn_rotate1.setText(_translate("MainWindow", "Rotate Right 90°"))
        self.btn_rotate2.setText(_translate("MainWindow", "Rotate Left  90°"))
        self.btn_fliph.setText(_translate("MainWindow", "Flip Horizontal"))
        self.btn_flipv.setText(_translate("MainWindow", "Flip Vertical"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionclose.setText(_translate("MainWindow", "close"))


    def on_load_image(self):
        self.label_1.load_image()


    def on_crop_image(self, pad=0.0):
        try:
            self.label_2.is_expanded = False
            self.label_1.currentQRubberBand.hide()
            currentQRect = self.label_1.currentQRubberBand.geometry()
            self.label_1.currentQRubberBand.deleteLater() 
            x = int(currentQRect.x() * self.label_1.scaled_rate_1_w)
            y = int(currentQRect.y() * self.label_1.scaled_rate_1_h)
            w = int(currentQRect.width() * self.label_1.scaled_rate_1_w)
            h = int(currentQRect.height() * self.label_1.scaled_rate_1_h)
            cropQPixmap = self.label_1.pixmap().copy(x, y, w, h)
            self.label_2.set_ui(cropQPixmap, pad)
        except Exception as e:
            print(e)


    def correct_input_angle(self):
        outfile = skew_im(file_in=self.label_1.fname[0])
        self.label_1.fname = (outfile,)
        image = QtGui.QImage(outfile)
        self.label_1.setPixmap(QtGui.QPixmap.fromImage(image))


    def on_rotate_image(self, rotate_left=False, pad=0.0):
        if rotate_left:
            rotation = 90
        else:
            rotation = -90
        transform = QtGui.QTransform().rotate(rotation)
        r_pixmap = self.label_2._image.transformed(transform)
        self.label_2.chosen_points = np.array([[pad, pad],[r_pixmap.width()-pad, pad],[r_pixmap.width()-pad, r_pixmap.height()-pad],[pad, r_pixmap.height()-pad]], dtype=np.float64) 
        self.label_2.setPixmap(r_pixmap)
        self.label_2._image = r_pixmap
        

    def on_center_image(self):
        self.cstum_lyt.setAlignment(self.label_2, QtCore.Qt.AlignCenter)


    def on_expand_image(self, pad=10.0): 
        try:
            if not self.label_2.is_expanded:

                cropQPixmap = self.label_2._image.copy()
                width, height = cropQPixmap.width(), cropQPixmap.height()
                if width < 551 and height < 779:
                    cropQPixmap = cropQPixmap.scaled(551, 779, QtCore.Qt.KeepAspectRatio)
                    self.label_2.chosen_points = np.array([[pad, pad],[cropQPixmap.width(), pad],[cropQPixmap.width(), 
                                                        cropQPixmap.height()],[pad, cropQPixmap.height()]], dtype=np.float64)
                else:
                    self.label_2.chosen_points = np.array([[pad, pad],[cropQPixmap.width()/self.label_2.scaled_w, pad],
                                                        [cropQPixmap.width()/self.label_2.scaled_w, 
                                                        cropQPixmap.height()/self.label_2.scaled_h],
                                                        [pad, cropQPixmap.height()/self.label_2.scaled_h]], dtype=np.float64)
                self.label_2.setPixmap(cropQPixmap)
                self.label_2._image = cropQPixmap
                
        except Exception as e:
            print(str(e))
        


    def on_save_image(self, pad=0.0):
        pth = os.path.join(os.getcwd(), 'data', 'cropped_1.png') 
        pmx = self.label_2._image.copy(pad, pad, self.label_2._image.width()-(2*pad), self.label_2._image.height()-(2*pad))
        pmx.save(pth)

        img = cv2.imread(pth, cv2.IMREAD_COLOR)
        height, width = img.shape[0], img.shape[1]
        mask = np.zeros((height, width), dtype=np.uint8)
        
        if self.label_2._image.width() > 551 or self.label_2._image.height() > 779:
            x10 = self.label_2.chosen_points[0][0] * self.label_2.scaled_w
            y10 = self.label_2.chosen_points[0][1] * self.label_2.scaled_h
            x11 = self.label_2.chosen_points[1][0] * self.label_2.scaled_w
            y11 = self.label_2.chosen_points[1][1] * self.label_2.scaled_h
            x12 = self.label_2.chosen_points[2][0] * self.label_2.scaled_w
            y12 = self.label_2.chosen_points[2][1] * self.label_2.scaled_h
            x13 = self.label_2.chosen_points[3][0] * self.label_2.scaled_w
            y13 = self.label_2.chosen_points[3][1] * self.label_2.scaled_h
            pts = np.array([[x10, y10],[x11, y11],[x12, y12],[x13, y13]], dtype=np.float64)
            cv2.fillPoly(mask, np.int64([pts]), (255)) 
        else:
            cv2.fillPoly(mask, np.int64([self.label_2.chosen_points]), (255))
        res = cv2.bitwise_and(img, img, mask=mask)  

        # set to transparent background
        tmp = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
        b, g, r = cv2.split(res)
        rgba = [b,g,r, alpha]
        dst = cv2.merge(rgba,4)

        pth2 = os.path.join(os.getcwd(), 'data', 'cropped_2.png')
        cv2.imwrite(pth2, dst)

        pdf = FPDF("P", "mm", "A4") # P = Portrait, L = Landscape 
        pdf.add_page()

        # decimal millimeters = (pixels * 25.4d) / dpi;
        if width > 551 or height > 779:
            sw = width / 551
            sh = height / 779
            mw = width / sw * 9 * 25.4 / 600
            mh = height / sh * 9 * 25.4 / 600
        else:
            mw = (width * 9 * 25.4) / 600
            mh = (height * 9 * 25.4) / 600
        pdf.image(pth2, x=((pdf.w/2)-(mw/2)), y=((pdf.h/2)-(mh/2)), w=mw, h=mh)

        
        pdf_pth = os.path.join(os.getcwd(), "data", "croped", f"croped_pdf.pdf")
        pdf.output(pdf_pth)
        pdf.close()
        QMessageBox.information(self.horizontalLayoutWidget, "Pdf Saved", "your pdf is saved as croped_pdf.pdf, check the folder data/croped")
        

    
    def on_blur_image(self):
        try:
            self.label_1.currentQRubberBand.hide()
            currentQRect = self.label_1.currentQRubberBand.geometry()
            self.label_1.currentQRubberBand.deleteLater()

            pixmapp = QtGui.QPixmap(self.label_1.fname[0])
            qimage = QtGui.QImage(pixmapp.copy().toImage())
            buffer = QtCore.QBuffer()
            buffer.open(QtCore.QIODevice.ReadWrite)
            qimage.save(buffer, "PNG")

            strio = BytesIO()
            strio.write(buffer.data())
            buffer.close()
            strio.seek(0)
            im = Image.open(strio)

            shapes = []
            x, y , w, h = currentQRect.x(), currentQRect.y(), currentQRect.width(), currentQRect.height()
            offset = 0
            cut_rate = (h / 10)
            for i in range(10):
                shapes.append(
                    [[(x, y), (w+x, y+(cut_rate*i)-offset)],
                    [(x, y+(cut_rate*i)+(cut_rate)), (w+x, y+h+offset)]]
                )
                    

            # Create rectangle mask
            self.list_imgs = []
            for i, shape in enumerate(shapes):
                imgg = im.copy()
                for shp in shape:
                    draw = ImageDraw.Draw(imgg)
                    draw.rectangle(shp, fill='#000000')

                    # Blur image
                    blurred = imgg.filter(ImageFilter.GaussianBlur(0))

                    # Paste blurred region and save result
                    imgg.paste(blurred)
                filename = os.path.join(os.getcwd(), "data", "blured", f"blurredImg_{i+1}.png")
                imgg.save(filename)
                self.list_imgs.append(filename)
                
                pdf = FPDF()
                pdf.add_page()
                pdf.image(filename,10,10,pdf.w-20,pdf.h-20)
                pdf_pth = os.path.join(os.getcwd(), "data", "blured", f"blurredPdf_{i+1}.pdf")
                pdf.output(pdf_pth, "F")
                pdf.close()

            bp = QtGui.QPixmap(self.list_imgs[0])
            bp.scaled(551, 779, QtCore.Qt.KeepAspectRatio)
            self.label_2.setPixmap(bp)
            self.label_2._image = bp
            reply = QMessageBox.question(self.horizontalLayoutWidget, "Image Blured", 
                    "your image is blured, \nClick OK to see the blured documents", 
                    QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                blr_dir = os.path.join(os.getcwd(), "data", "blured")
                os.startfile(blr_dir)
            
        
        except Exception as e:
            QMessageBox.warning(self.horizontalLayoutWidget, "Error", f"please select a region first,\n{str(e)}")
                

    def on_flip(self, direction):
        if direction == "horizontal":
            self.label_2._image = self.label_2._image.transformed(QtGui.QTransform().scale(-1, 1))
        elif direction == "vertical":
            self.label_2._image = self.label_2._image.transformed(QtGui.QTransform().scale(1, -1))
        self.label_2.setPixmap(self.label_2._image)
        self.label_2.chosen_points = np.array([[0.0,0.0],[self.label_2._image.width(),0.0],[self.label_2._image.width(), self.label_2._image.height()],
                                                [0.0,self.label_2._image.height()]], dtype=np.float64)
            


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('PhotoEditor V1.0')
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setStyleSheet("""* {
            background-color: #e5e5e5;
        }
        .QLabel {
            border-style: solid;
        }
        .QMainWindow {
            border-style: none;
        }
        """)
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
