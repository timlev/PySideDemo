#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from PySide import QtGui
from PySide import QtCore


class CenterWindow(QtGui.QFrame):

    style = '''
        QFrame#CenterWindow{
            background-color: lightgray;
        }
        QComboBox{
            color:white;
            font-size: 15px;
            font-family: "Verdana";
            background-color: rgb(5, 9, 21);
        }

        QComboBox:on{
            background-color: rgb(5, 9, 21);
        }

        QComboBox::drop-down :on{
            background-color: rgb(5, 9, 21);
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 15px;
        }


        QComboBox QAbstractItemView {
            border: none;
            color:white;
            font-size: 15px;
            font-family: "Verdana";
         }

        QComboBox QAbstractItemView {
            color:white;
            font-size: 15px;
         }

        QComboBox QAbstractItemView::item{
            height: 25px;
            color:white;
            font-size: 15px;
         }

        QComboBox QAbstractItemView::item:selected{
            background-color: rgb(63, 147, 168);
        }

        QComboBox QAbstractItemView::item:hover{
            background-color: rgb(69, 187, 217);
        }

        QListView {
     show-decoration-selected: 1; /* make the selection span the entire width of the view */
 }

 QListView::item:alternate {
     background: #EEEEEE;
 }

 QListView::item:selected {
     border: 1px solid #6a6ea9;
 }

 QListView::item:selected:!active {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #ABAFE5, stop: 1 #8588B2);
 }

 QListView::item:selected:active {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #6a6ea9, stop: 1 #888dd9);
 }

 QListView::item:hover {
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #FAFBFE, stop: 1 #DCDEF1);
 }
    '''

    def __init__(self, parent=None):
        super(CenterWindow, self).__init__(parent)
        self.setObjectName("CenterWindow")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon(os.sep.join([os.getcwd(), "skin", "images", "icon.ico"])))  # 设置程序图标
        self.setFixedSize(800, 500)
        self.initUI()
        self.setStyleSheet(self.style)
        print self.a.pos(), self.mapFromGlobal(self.a.pos())

    def initUI(self):
        self.selectPanel = QtGui.QFrame()
        self.listwidget = ListItemWidget(self)
        self.listwidget.installEventFilter(self)
        mainlayout = QtGui.QVBoxLayout(self)
        mainlayout.addWidget(self.selectPanel)
        mainlayout.addWidget(self.listwidget)
        mainlayout.addStretch()
        self.setLayout(mainlayout)
        self.layout().setContentsMargins(5, 5, 5, 5)

        self.selectPanel.setFixedHeight(50)
        self.a = ListItemWidget(self.selectPanel)
        self.a.move(20, 0)

    def updateText(self, index):
        print index
        self.combox.setEditText(unicode(index))

    def highlighted(self, index):
        print 'highlighted', index

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseMove:
            return True
        else:
            return super(CenterWindow, self).eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        self.setFocus()
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            if hasattr(self, "dragPosition"):
                self.move(event.globalPos() - self.dragPosition)
                event.accept()


class EventEater(QtCore.QObject):

    def __init__(self, parent=None):
        super(EventEater, self).__init__(parent)
        self.parent = parent

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseMove:
            return True
        elif event.type() == QtCore.QEvent.Wheel:
            return True
        else:
            return super(EventEater, self).eventFilter(obj, event)


class ItemWidget(QtGui.QLabel):

    style = '''
        QLabel{
            background-color: transparent;
        }
        QLabel: pressed{
            background-color: green;
        }

        QPushButton#deleteButton{
            background-color: green;
        }

        QPushButton#deleteButton:pressed {
            background-color: red;
        }

        QLabel#itemLabel{
            color: white;
            font-size: 13px;
            font-family: "Verdana";
            background-color: black;
            border: none;
        }
    '''
    width = 200
    height = 40

    def __init__(self, text, deleteflag=True):
        super(ItemWidget, self).__init__()
        self.text = text
        self.deleteflag = deleteflag
        self.initUI()

    def initUI(self):
        self.setFixedSize(self.width, self.height)
        mainlayout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel(self.text)
        self.label.setObjectName('itemLabel')

        mainlayout.addWidget(self.label)
        if self.deleteflag:
            self.deleteButton = QtGui.QPushButton('x', self)
            self.deleteButton.setObjectName('deleteButton')
            self.deleteButton.setFixedSize(20, 20)
            mainlayout.addWidget(self.deleteButton)
        else:
            pass
        mainlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainlayout)
        # self.setStyleSheet(self.style)


class ListItemWidget(QtGui.QWidget):

    style = '''

        QPushButton#downButton{
            background-color: green;
        }

        QPushButton#downButton:pressed {
            background-color: red;
        }

        QLabel{
            color: black;
            font-size: 13px;
            font-family: "Verdana";
            background-color: red;
            border: none;
        }
        QLabel:hover{
            color: black;
            font-size: 13px;
            font-family: "Verdana";
            background-color: green;
            border: none;
        }

        QLabel#currentText{
            color: black;
            font-size: 13px;
            font-family: "Verdana";
            background-color: red;
            border: none;
        }
    '''

    def __init__(self, parent=None):
        super(ListItemWidget, self).__init__(parent)
        self.initUI()
        self.setStyleSheet(self.style)

    def initUI(self):
        self.label = QtGui.QLabel('1212121212')
        self.label.setObjectName('currentText')
        self.downButton = QtGui.QPushButton('^')
        self.downButton.setObjectName('downButton')
        self.listScrollArea = QtGui.QScrollArea()
        self.listScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.initSize()
        self.listwidget = QtGui.QWidget()
        listlayout = QtGui.QVBoxLayout()
        for i in xrange(10):
            route = "Route%d" % i
            itemWidget = QtGui.QLabel(route)
            listlayout.addWidget(itemWidget)
        listlayout.setContentsMargins(0, 0, 0, 0)
        listlayout.setSpacing(0)
        self.listwidget.setLayout(listlayout)
        self.listScrollArea.setWidget(self.listwidget)

        self.listScrollArea.hide()

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.label, 0, 0)
        mainLayout.addWidget(self.downButton, 0, 1)
        mainLayout.addWidget(self.listScrollArea, 1, 0, 1, 2)
        self.setLayout(mainLayout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        self.downButton.clicked.connect(self.showListWidget)

    def initSize(self):
        self.setFixedSize(ItemWidget.width + 20, 200)
        self.downButton.setFixedWidth(40)
        self.label.setFixedWidth(self.width() - self.downButton.width())
        self.listScrollArea.setFixedHeight(80)

    def showListWidget(self):
        self.listScrollArea.setVisible(not self.listScrollArea.isVisible())


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    main = CenterWindow()
    main.show()
    sys.exit(app.exec_())
