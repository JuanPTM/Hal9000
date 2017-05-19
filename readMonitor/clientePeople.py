import sys, traceback, Ice
import readHallComp
from PySide import QtCore, QtGui, QtSvg
from PyQt4.QtCore import QString
from gui import *
import cv2
import numpy as np
from PIL import Image
import StringIO

class people():
    """docstring forpeop."""
    def __init__(self):
        self.id = None
        self.label = None
        self.item = None
class main():
    """docstring fo main."""
    def __init__(self):
        status = 0
        ic = None
        try:
            ic = Ice.initialize(sys.argv)
            self.camaras =[]
            base = ic.stringToProxy("readhall:tcp -h localhost -p 20001")
            self.camaras.append(readHallComp.readHallPrx.checkedCast(base))
            for c in self.camaras:
                if not c:
                    print "Camera", c, "Error to connect"
                    self.camaras.remove(c)
            self.Dialog = QtGui.QDialog()
            self.ui = Ui_Dialog()
            self.ui.setupUi(self.Dialog)
            self.Dialog.showMaximized()
            self.scene = QtGui.QGraphicsScene()
            self.image = QtGui.QGraphicsPixmapItem("./Plano_Informatica.png")
            self.scene.addItem(self.image);
            self.ui.view.setScene(self.scene)
# Connect the slots
            self.timer = QtCore.QTimer()
            QtCore.QTimer.connect(self.timer, QtCore.SIGNAL("timeout()"), self.render)
            # self.timer.start(100)
            self.timer2 = QtCore.QTimer()
            QtCore.QTimer.connect(self.timer2, QtCore.SIGNAL("timeout()"), self.leer)
            self.timer2.start(500)

            self.labelL = []
            self.itemL = []
# draw the Coordinates origin
            item=QtGui.QGraphicsEllipseItem(-5,-5,10,10)
            item.setBrush(QtGui.QBrush(QtCore.Qt.red, style = QtCore.Qt.SolidPattern))
            self.scene.addItem(item)
            y = 1.85
            self.image.setScale(y)
            self.image.setPos(-51*y, -113*y)
            self.Dialog.exec_()

        except:
            traceback.print_exc()
            status = 1

        if ic:
            # Clean up
            try:
                ic.destroy()
            except:
                traceback.print_exc()
                status = 1

        sys.exit(status)

    def qimage_to_pil_image(self, img):
        buffer = QtCore.QBuffer()
        buffer.open(QtCore.QIODevice.ReadWrite)
        img.save(buffer, "PNG")

        strio = StringIO.StringIO()
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        return Image.open(strio)

#     cv::Mat qimage_to_mat_ref(QImage &img, int format)
#     return cv::Mat(img.height(), img.width(),
#             format, img.bits(), img.bytesPerLine());
    @QtCore.Slot()
    def render(self):
        pixm = QtGui.QPixmap()
        i = QtGui.QImage(self.scene.sceneRect().size().toSize(),QtGui.QImage.Format_ARGB32)
        p = QtGui.QPainter(pixm)
        # self.scene.render(p)
        self.ui.view.render(p)
        i = p.toImage()
        img = self.qimage_to_pil_image(i)


    @QtCore.Slot()
    def leer(self):
	for l in self.labelL:
            self.scene.removeItem(l)
        for i in self.itemL:
            self.scene.removeItem(i)
        self.itemL = []
        self.labelL = []

        for c in self.camaras:
            d = c.getHall()
            print "Hay ", len(d.data), "Personas"
            for p in d.data:
                x = p.pos.x
                y = p.pos.y
                z = 0
                print "   Posicion:", x, y, z
                item=QtGui.QGraphicsEllipseItem(x/50-5,y/50-5,10,10)
                item.setBrush(QtGui.QBrush(QtCore.Qt.blue, style = QtCore.Qt.SolidPattern))
                label = QtGui.QGraphicsTextItem(str(p.id))
                label.moveBy(x/50-1,y/50-1)
                self.itemL.append(item)
                self.labelL.append(label)
                self.scene.addItem(self.labelL[-1])
                self.scene.addItem(self.itemL[-1])

app = QtGui.QApplication(sys.argv)
main()
