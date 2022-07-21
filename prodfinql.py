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
        self.scrollArea = None

    def load_image(self):
        self.fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(),"Image files (*.png *.jpg *.gif)")
        image = QtGui.QImage(self.fname[0])
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
        point = eventQMouseEvent.pos()
        if point.x() > 850:
            scrollBarh = self.scrollArea.horizontalScrollBar()
            scrollBarh.setValue(scrollBarh.value() + 5)
        if point.x() < self.originQPoint.x():
            scrollBarh = self.scrollArea.horizontalScrollBar()
            scrollBarh.setValue(scrollBarh.value() - 5)
        if point.y() > 850:
            scrollBarv = self.scrollArea.verticalScrollBar()
            scrollBarv.setValue(scrollBarv.value() + 5)
        if point.y() < self.originQPoint.y():
            scrollBarv = self.scrollArea.verticalScrollBar()
            scrollBarv.setValue(scrollBarv.value() - 5)




class Stresh2(QtWidgets.QLabel):
    
    DELTA = 50 #for the minimum distance   default were 10  
    def __init__(self):
        super(Stresh2, self).__init__()
        self.is_expanded = False # self.setStyleSheet("border: 2px solid black;") # self.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)


    def set_ui(self, bitmax, pad):
        self.draggin_idx = -1 
        self.setScaledContents(True)
        self._image = bitmax

        if bitmax.width() > 620:
            self.scaled_w = bitmax.width() / 620
        else:
            self.scaled_w = 1.0
        if bitmax.height() > 877:
            self.scaled_h = bitmax.height() / 877
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
            pen2 = QtGui.QPen(QtGui.QColor(50, 50, 50, 120), 3, QtCore.Qt.SolidLine)
            painter.setPen(pen2)
            painter.drawPolygon(points) # painter.drawLine(100, 100, 400, 400)
            pen = QtGui.QPen(QtGui.QColor(50, 50, 50, 120), 20, QtCore.Qt.SolidLine)
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
        MainWindow.resize(1900, 950)
        # MainWindow.showMaximized()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        # geometry = app.desktop().availableGeometry()
        # titleBarHeight = self.horizontalLayoutWidget.style().pixelMetric(
        #     QtWidgets.QStyle.PM_TitleBarHeight,
        #     QtWidgets.QStyleOptionTitleBar(),
        #     self.horizontalLayoutWidget
        # )
        # geometry.setHeight(geometry.height() - (titleBarHeight*2+10))
        # geometry.setWidth(geometry.width() - (20))
        # print(geometry.width(), geometry.height())
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1880, 900)) # QtCore.QRect(10, 10, 1550, 850)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_1 = Stresh1()
        # self.label_1.setStyleSheet("Stresh1 {\n"
        # "    border: 1px solid rgb(200, 198, 191);\n"
        # "    border-radius: 10px;\n"
        # "    background-color: rgb(250, 250, 250);\n"
        # "    margin: 10px;\n"
        # "    padding: 10px;\n"
        # "}")
        
        # self.label_1.setMinimumSize(QtCore.QSize(0, 0))
        # self.label_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        
        self.scrollArea = QtWidgets.QScrollArea()
        self.label_1.scrollArea = self.scrollArea
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        # frame=QtWidgets.QFrame.Box
        # scrollArea.setFrameShape(frame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.label_1)

        # scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setFixedSize(QtCore.QSize(877, 877))
        self.scrollArea.setStyleSheet("QScrollArea {\n"
        "    border: 1px solid rgb(200, 198, 191);\n"
        "    border-radius: 10px;\n"
        "    background-color: rgb(250, 250, 250);\n"
        "    margin: 10px;\n"
        "    padding: 10px;\n"
        "}")

        self.horizontalLayout.addWidget(self.scrollArea, stretch=4, alignment=QtCore.Qt.AlignCenter)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        # self.label_3.setMinimumSize(QtCore.QSize(0, 10))
        # self.label_3.setMaximumSize(QtCore.QSize(16777215, 10))
        self.verticalLayout.addWidget(self.label_3, stretch=1, alignment=QtCore.Qt.AlignCenter)
        self.btn_load = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        # self.btn_load.setMinimumSize(QtCore.QSize(0, 30))
        # self.btn_load.setMaximumSize(QtCore.QSize(100, 30))
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
        # self.combo_select = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        # # self.combo_select.setMinimumSize(QtCore.QSize(0, 20))
        # self.combo_select.setStyleSheet("QComboBox {\n"
        # "    border: 1px solid gray;\n"
        # "    border-radius: 3px;\n"
        # "    padding: 1px 18px 1px 3px;\n"
        # "}\n"
        # "\n"
        # "QComboBox:editable {\n"
        # "    background: white;\n"
        # "}\n"
        # "\n"
        # "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        # "     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
        # "                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
        # "                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
        # "}\n"
        # "\n"
        # "/* QComboBox gets the \"on\" state when the popup is open */\n"
        # "QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
        # "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
        # "                                stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,\n"
        # "                                stop: 0.5 #DDDDDD, stop: 1.0 #E1E1E1);\n"
        # "}\n"
        # "\n"
        # "QComboBox:on { /* shift the text when the popup opens */\n"
        # "    padding-top: 3px;\n"
        # "    padding-left: 4px;\n"
        # "}\n"
        # "\n"
        # "QComboBox::drop-down {\n"
        # "    subcontrol-origin: padding;\n"
        # "    subcontrol-position: top right;\n"
        # "    width: 15px;\n"
        # "\n"
        # "    border-left-width: 1px;\n"
        # "    border-left-color: darkgray;\n"
        # "    border-left-style: solid; /* just a single line */\n"
        # "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        # "    border-bottom-right-radius: 3px;\n"
        # "}\n"
        # "\n"
        # "QComboBox::down-arrow {\n"
        # "    image: url(icons/downarrow24.png);\n"
        # "}\n"
        # "\n"
        # "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        # "    top: 1px;\n"
        # "    left: 1px;\n"
        # "}\n"
        # "")
        # self.combo_select.addItem("")
        # self.combo_select.addItem("")
        # self.verticalLayout.addWidget(self.combo_select, stretch=1, alignment=QtCore.Qt.AlignCenter)
        
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
        # self.btn_rotate2.setMinimumSize(QtCore.QSize(100, 30))
        # self.btn_rotate2.setMaximumSize(QtCore.QSize(100, 30))
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
        self.label_2.setMaximumSize(QtCore.QSize(877, 877))
        
        

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
        self.wdg.setFixedSize(QtCore.QSize(640, 897))
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


    def on_crop_image(self, pad=10.0):
        try:
            self.label_2.is_expanded = False
            self.label_2.expand_rate = 1.0 
            self.label_1.currentQRubberBand.hide()
            currentQRect = self.label_1.currentQRubberBand.geometry()
            self.label_1.currentQRubberBand.deleteLater() # cropQPixmap = self.label_1.pixmap().copy(currentQRect.x()-10, currentQRect.y()-10, currentQRect.width()+20, currentQRect.height()+20) # cropQPixmap = cropQPixmap.copy(currentQRect.x()-10, currentQRect.y()-10, currentQRect.width()+20, currentQRect.height()+20) # 
            cropQPixmap = self.label_1.pixmap().copy(currentQRect)
            self.label_2.set_ui(cropQPixmap, pad)
        except Exception as e:
            print(e)


    def correct_input_angle(self):
        outfile = skew_im(file_in=self.label_1.fname[0])
        self.label_1.fname = (outfile,)
        image = QtGui.QImage(outfile)
        self.label_1.setPixmap(QtGui.QPixmap.fromImage(image))


    def on_rotate_image(self, rotate_left=False, pad=10.0):
        # if self.label_2.is_expanded:
        #     pixmap = self.label_2.scaled_img.copy()
        # else:
        #     pixmap = self.label_2._image.copy()
        
        if rotate_left:
            rotation = 90
            # self.label_2.rotating_angle -= 90
        else:
            rotation = -90
            # self.label_2.rotating_angle += 90
        transform = QtGui.QTransform().rotate(rotation)

        # pmx_org = self.label_2._image.copy()
        # if self.label_2.rotating_angle % 180 == 0:
        #     pmx = pmx_org.scaled(620, 877, QtCore.Qt.KeepAspectRatio) # , QtCore.Qt.SmoothTransformation
        # else:
        #     pmx = pmx.scaled(877, 620, QtCore.Qt.KeepAspectRatio)
        r_pixmap = self.label_2._image.transformed(transform) # , QtCore.Qt.SmoothTransformation
        # r_pixmap = self.label_2._image.transformed(transform, QtCore.Qt.SmoothTransformation)  #, QtCore.Qt.SmoothTransformation  # r_pixmap = pmx.transformed(QtGui.QTransform().rotate(90 if rotate_left else -90))

        # if is_width_biger_thn_a4:
        #     pixmap = pixmap.scaledToWidth(620)
        #     r_pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation) 
        #     self.label_2.chosen_points = np.array([[10.0,10.0],[r_pixmap.width()-10.0,10.0],[r_pixmap.width()-10.0,r_pixmap.height()-10.0],[10.0,r_pixmap.height()-10.0]], dtype=np.float64)
        #     self.label_2.setPixmap(r_pixmap)
        #     self.label_2._image = self.label_2._image
        # else:
        #     r_pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation) 
        #     self.label_2.chosen_points = np.array([[10.0,10.0],[r_pixmap.width()-10.0,10.0],[r_pixmap.width()-10.0,r_pixmap.height()-10.0],[10.0,r_pixmap.height()-10.0]], dtype=np.float64)
        #     self.label_2.setPixmap(r_pixmap)
        #     self.label_2._image = r_pixmap
        # if r_pixmap.width() <= r_pixmap.height():
        #     # if self.label_2.is_expanded:
        #     #     r_pixmap = r_pixmap.scaled(620, 877, QtCore.Qt.KeepAspectRatio) 
        #     self.label_2.chosen_points = np.array([[10.0,10.0],[r_pixmap.width()-10.0,10.0],[r_pixmap.width()-10.0,r_pixmap.height()-10.0],[10.0,r_pixmap.height()-10.0]], dtype=np.float64) 
        # else:
        #     # if self.label_2.is_expanded:
        #     #     r_pixmap = r_pixmap.scaled(877, 620, QtCore.Qt.KeepAspectRatio)
        #     self.label_2.chosen_points = np.array([[10.0,10.0],[r_pixmap.width()-10.0,10.0],[r_pixmap.width()-10.0,r_pixmap.height()-10.0],[10.0,r_pixmap.height()-10.0]], dtype=np.float64) 
        self.label_2.chosen_points = np.array([[pad, pad],[r_pixmap.width()-pad, pad],[r_pixmap.width()-pad, r_pixmap.height()-pad],[pad, r_pixmap.height()-pad]], dtype=np.float64) 
        # self.label_2.scaled_img = self.label_2._image.scaledToWidth(620)
        # self.label_2.scaled_img = self.label_2._image.scaledToHeight(877)
        self.label_2.setPixmap(r_pixmap)
        # self.label_2.setMaximumSize(QtCore.QSize(877, 620))
        # self.label_2.scaled_img = r_pixmap
        self.label_2._image = r_pixmap
        

    def on_center_image(self):
        # self.horizontalLayout.setAlignment(self.label_2, QtCore.Qt.AlignCenter)
        self.cstum_lyt.setAlignment(self.label_2, QtCore.Qt.AlignCenter)


    def on_expand_image(self, pad=10.0): 
        # to get the expand change rate
        # if not self.label_2.is_expanded:
        #     self.label_2._image = self.label_2._image.scaled(620, 877, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) #, QtCore.Qt.SmoothTransformation 
        #     self.label_2.is_expanded = True
        # self.label_2.setPixmap(self.label_2._image)
        # self.label_2.chosen_points = np.array([[10.0,10.0],[self.label_2._image.width()-10.0,10.0],[self.label_2._image.width()-10.0,
        #                                         self.label_2._image.height()-10.0],[10.0,self.label_2._image.height()-10.0]], dtype=np.float64)
        
        
        try:
            if not self.label_2.is_expanded:

                cropQPixmap = self.label_2._image.copy()
                width, height = cropQPixmap.width(), cropQPixmap.height()
                if width < 620 and height < 877:
                    cropQPixmap = cropQPixmap.scaled(620, 877, QtCore.Qt.KeepAspectRatio)

                self.label_2.setPixmap(cropQPixmap)
                self.label_2.chosen_points = np.array([[pad, pad],[cropQPixmap.width(), pad],[cropQPixmap.width(), 
                                                        cropQPixmap.height()],[pad, cropQPixmap.height()]], dtype=np.float64)
        except Exception as e:
            print(str(e))
        


    def on_save_image(self, pad=0.0):
        pth = os.path.join(os.getcwd(), 'data', 'cropped_1.png') 
        
        # creqte apix;qp object
        # pmx = QtGui.QPixmap(self.label_1.fname[0])
        # if self.label_1.is_scaled:
        pmx = self.label_2._image.copy(pad, pad, self.label_2._image.width()-(2*pad), self.label_2._image.height()-(2*pad))
        # else:
        #     mp = self.label_2.pixmap()
        #     pmx = self.label_2.pixmap().copy(pad, pad, mp.width()-(2*pad), mp.height()-(2*pad))
        pmx.save(pth)

        img = cv2.imread(pth, cv2.IMREAD_COLOR)
        height, width = img.shape[0], img.shape[1]
        mask = np.zeros((height, width), dtype=np.uint8)

        if self.label_2.is_expanded:
            r = self.label_2.expand_rate
            print("r: ", r)
            if r > 1:
                cv2.fillPoly(mask, np.int64([self.label_2.chosen_points * r * self.label_1.scalling_rate]), (255)) # cv2.fillPoly(mask, np.int64([self.label_2.chosen_points * r ]), (255))
            elif r < 1:
                cv2.fillPoly(mask, np.int64([(self.label_2.chosen_points * r) / (r / self.label_1.scalling_rate)]), (255))  # * self.label_1.scalling_rate
            else:
                cv2.fillPoly(mask, np.int64([self.label_2.chosen_points * r]), (255)) 
        else:
            cv2.fillPoly(mask, np.int64([self.label_2.chosen_points]), (255))
        res = cv2.bitwise_and(img, img, mask=mask)  

        # set to transparent background
        tmp = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        _,alpha = cv2.threshold(tmp,0,255,cv2.THRESH_BINARY)
        b, g, r = cv2.split(res)
        rgba = [b,g,r, alpha]
        dst = cv2.merge(rgba,4)

        # # scale to fit A4
        # if pmx.width() > 620:
        #     dst = self.image_resize(dst, width=600)
        #     height, width = dst.shape[0], img.shape[1]

        
        

        pth2 = os.path.join(os.getcwd(), 'data', 'cropped_2.png')
        cv2.imwrite(pth2, dst)

        


        pdf = FPDF("P", "mm", "A4") # P = Portrait, L = Landscape 
        pdf.add_page()

        # size = 7016, 4961
        # if pmx.width() > 4961 or pmx.height() > 7016:
        #     size = width, height
        #     im = Image.open(pth2)
        #     im_resized = im.resize(size, Image.ANTIALIAS)
        #     im_resized.save("cropped_3.png", "PNG")
        #     pdf.image(pth2, x=0, y=0)

        # # pdf.image("cropped_3.png", x=0, y=0, w=pdf.w, h=pdf.h)
        # pdf_pth = os.path.join(os.getcwd(), "data", "croped", f"croped_pdf.pdf")
        # pdf.output(pdf_pth)
        # pdf.close()
        # QMessageBox.information(self.horizontalLayoutWidget, "Pdf Saved", "your pdf is saved as croped_pdf.pdf, check the folder data/croped")

        print(width, height)
        # decimal millimeters = (pixels * 25.4d) / dpi;
        if pmx.width() > 620:
            r = 620 / pmx.width()
            mw = width * 8 * r * 25.4 / 600
            mh = height * 8 * r * 25.4 / 600
        else:
            mw = (width * 8 * 25.4) / 600
            mh = (height * 8 * 25.4) / 600
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

            sr = self.label_1.scalling_rate
            if sr is None:
                sr = 1
            pixmapp = QtGui.QPixmap(self.label_1.fname[0])
            self.label_1.selected_rect = currentQRect
            # (currentQRect.x()*sr)-10, (currentQRect.y()*sr)-10, (currentQRect.width()*sr)+20, (currentQRect.height()*sr)+20

            qimage = QtGui.QImage(pixmapp.copy().toImage())
            buffer = QtCore.QBuffer()
            buffer.open(QtCore.QIODevice.ReadWrite)
            qimage.save(buffer, "PNG")

            strio = BytesIO()
            strio.write(buffer.data())
            buffer.close()
            strio.seek(0)
            im = Image.open(strio)

            # im = Image.open(self.label_1.fname[0])
            
            

            shapes = []

            # for i in range(10):
            #     shapes.append(
            #         [[(currentQRect.x(), currentQRect.y()), (currentQRect.width()+currentQRect.x(), currentQRect.y()+(cut_rate*i))],
            #         [(currentQRect.x(), currentQRect.y()+(cut_rate*i)+(cut_rate)), (currentQRect.width()+currentQRect.x(), currentQRect.y()+currentQRect.height())]]
            #     )

            # (currentQRect.x()*sr)-10, (currentQRect.y()*sr)-10, (currentQRect.width()*sr)+20, (currentQRect.height()*sr)+20
            x, y , w, h = (currentQRect.x()*sr), (currentQRect.y()*sr), (currentQRect.width()*sr), (currentQRect.height()*sr)
            offset = 1
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
            bp.scaled(620, 877, QtCore.Qt.KeepAspectRatio)
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
        self.label_2.chosen_points = np.array([[10.0,10.0],[self.label_2._image.width()-10.0,10.0],[self.label_2._image.width()-10.0,
                                                self.label_2._image.height()-10.0],[10.0,self.label_2._image.height()-10.0]], dtype=np.float64)
            

    def image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('PhotoEditor V1.0')
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setStyleSheet("""* {
            background-color: #f2f2f2;
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
