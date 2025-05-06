import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect, QPoint, QSize, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygon
import win32api, win32gui, win32con

class OverlayWindow(QWidget):
    def __init__(self, x=600, y=300, w=500, h=400):
        super().__init__()
        self.editable = False

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
        self.show()

        self.roi_rect = QRect(x, y, w, h)
        self.handle_size = 20
        self.dragging_mode = None
        self.drag_offset = QPoint()

        self.detected_points1 = []
        self.detected_points2 = []
        self.blink_visible = True

        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.toggle_blink)
        self.blink_timer.start(500)

    def set_editable_mode(self, editable: bool):
        self.editable = editable
        hwnd = self.winId().__int__()
        ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if editable:
            # 마우스 이벤트 받도록
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style & ~win32con.WS_EX_TRANSPARENT)
            self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        else:
            # 마우스 통과
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style | win32con.WS_EX_TRANSPARENT)
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.update()

    def toggle_blink(self):
        self.blink_visible = not self.blink_visible
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(self.roi_rect)

        # 이동 핸들
        if self.editable:
            move_handle_pos = self.roi_rect.topLeft() + QPoint(self.roi_rect.width() // 2 - self.handle_size // 2, -self.handle_size - 5)
            self.move_handle_rect = QRect(move_handle_pos, QSize(self.handle_size, self.handle_size))
            painter.setBrush(QColor(255, 255, 255, 1))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.move_handle_rect)

            cx, cy = self.move_handle_rect.center().x(), self.move_handle_rect.center().y()
            painter.setPen(QPen(Qt.red, 1))
            painter.setBrush(Qt.red)
            painter.drawLine(cx - 5, cy, cx + 5, cy)
            painter.drawLine(cx, cy - 5, cx, cy + 5)

            offset = 5
            triangle_up = QPolygon([
                QPoint(cx, cy - 15),
                QPoint(cx - offset, cy - offset),
                QPoint(cx + offset, cy - offset)
            ])
            triangle_down = QPolygon([
                QPoint(cx, cy + 15),
                QPoint(cx - offset, cy + offset),
                QPoint(cx + offset, cy + offset)
            ])
            triangle_left = QPolygon([
                QPoint(cx - 15, cy),
                QPoint(cx - offset, cy - offset),
                QPoint(cx - offset, cy + offset)
            ])
            triangle_right = QPolygon([
                QPoint(cx + 15, cy),
                QPoint(cx + offset, cy - offset),
                QPoint(cx + offset, cy + offset)
            ])
            painter.drawPolygon(triangle_up)
            painter.drawPolygon(triangle_down)
            painter.drawPolygon(triangle_left)
            painter.drawPolygon(triangle_right)

            # 크기 조절 핸들
            resize_handle_pos = self.roi_rect.bottomRight() + QPoint(3, 3)
            self.resize_handle_rect = QRect(resize_handle_pos, QSize(self.handle_size, self.handle_size))
            painter.setBrush(QColor(255, 255, 255, 1))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.resize_handle_rect)

            painter.setPen(QPen(Qt.red, 1))
            top_left = self.resize_handle_rect.topLeft()
            bottom_right = self.resize_handle_rect.bottomRight()
            painter.drawLine(top_left, bottom_right)
            painter.setBrush(Qt.red)

            triangle_topleft = QPolygon([
                top_left + QPoint(0, 10),
                top_left + QPoint(0, 0),
                top_left + QPoint(10, 0)
            ])
            painter.drawPolygon(triangle_topleft)

            triangle_bottomright = QPolygon([
                bottom_right + QPoint(0, -10),
                bottom_right + QPoint(0, 0),
                bottom_right + QPoint(-10, 0)
            ])
            painter.drawPolygon(triangle_bottomright)

        # 감지된 색상 위치 표시
        if self.blink_visible:
            painter.setPen(Qt.NoPen)
            for pt in self.detected_points1:
                painter.setBrush(QColor(255, 0, 0))
                painter.drawEllipse(pt, 2, 2)
            for pt in self.detected_points2:
                painter.setBrush(QColor(0, 255, 0))
                painter.drawEllipse(pt, 2, 2)    

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.move_handle_rect.contains(event.pos()):
                self.dragging_mode = 'move'
                self.drag_offset = event.pos() - self.roi_rect.topLeft()
            elif self.resize_handle_rect.contains(event.pos()):
                self.dragging_mode = 'resize'
                self.drag_offset = event.pos() - self.roi_rect.bottomRight()
            else:
                self.dragging_mode = None

    def mouseMoveEvent(self, event):
        if self.dragging_mode == 'move':
            new_top_left = event.pos() - self.drag_offset
            self.roi_rect.moveTopLeft(new_top_left)
            self.update()
        elif self.dragging_mode == 'resize':
            new_bottom_right = event.pos() - self.drag_offset
            self.roi_rect.setBottomRight(new_bottom_right)
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragging_mode = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = OverlayWindow()
    sys.exit(app.exec_())
