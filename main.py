import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2


class MyWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0,0,screen_width, screen_height)
        self.setWindowTitle('')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.1)
        self.num_snip = 0
        self.is_snipping = False
        
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        print('Press Key_Space to Quit')
        self.show()
        
    def paintEvent(self, event):
        if self.is_snipping:
            brush_color = (0,0,0,0)
            lw = 0
            opacity = 0
        else:
            brush_color = (128,128,255,128)
            lw=1
            opacity=0.3
        
        self.setWindowOpacity(opacity)
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), lw))
        qp.setBrush(QtGui.QColor(*brush_color))
        qp.drawRect(QtCore.QRect(self.begin, self.end))
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            # print('Quit')
            self.close()
        event.accept()
    
    def mousePressEvent(self,event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()
    
    def mouseMoveEvent(self,event):
        self.end = event.pos()
        self.update()
    
    def mouseReleaseEvent(self, event):
        self.num_snip+=1
        x1=min(self.begin.x(), self.end.x())
        y1=min(self.begin.y(), self.end.y())
        x2=max(self.begin.x(), self.end.x())
        y2=max(self.begin.y(), self.end.y())
        print(x1,y1,x2,y2)
        
        self.is_snipping = True
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        
        self.close()
        # self.is_snipping=False
        # self.repaint()
        # QtWidgets.QApplication.processEvents()
        
        # img_name = f'Image_{self.num_snip}.png'
        img.save(f'Image_{self.num_snip}.png')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        
        
        
        
        
        
        
if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())