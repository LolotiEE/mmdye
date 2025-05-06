import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QColorDialog, QLineEdit, QCheckBox
)
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt, QTimer, QPoint
from overlay import OverlayWindow
from PIL import ImageGrab
import numpy as np
from PyQt5.QtGui import QIntValidator

class ColorMonitorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("염색 도우미")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setGeometry(100, 100, 300, 100)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.init_ui()

        self.monitoring = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_roi_colors)

        self.tolerance1 = 10
        self.tolerance2 = 10

        self.overlay = OverlayWindow()
        self.overlay.set_editable_mode(False)

    def init_ui(self):
        layout = QVBoxLayout()

        # 색 선택1
        self.color1_checkbox = QCheckBox()
        self.color1_checkbox.setChecked(True)
        self.color1_checkbox.setEnabled(False)
        self.color1_preview = QLabel("1")
        self.color1_preview.setFixedSize(20, 20)
        self.color1_preview.setStyleSheet("background-color: #ff0000; border: 1px solid black; border-radius: 10px;")
        self.color1_preview.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.color1_label1 = QLabel("색상1")
        self.color1_label1.setFixedSize(30, 20)
        self.color1_label1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.color1_label2 = QLabel("오차값")
        self.color1_label2.setFixedSize(50, 20)
        self.color1_label2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.color1_input = QLineEdit("#ffffff")
        self.color1_input.setFixedWidth(60)
        self.color1_input.textChanged.connect(lambda text: self.update_preview(self.color1_button, text))
        self.color1_button = QPushButton()
        self.color1_button.setFixedSize(20, 20)
        self.color1_button.setStyleSheet("background-color: #ffffff; border: 1px solid black;")
        self.color1_button.clicked.connect(lambda: self.select_color(self.color1_input))
        self.tolerance_input1 = QLineEdit("10")
        self.tolerance_input1.setFixedWidth(40)
        self.tolerance_input1.setValidator(QIntValidator(0, 255))
                                         
        color1_layout = QHBoxLayout()
        color1_layout.addWidget(self.color1_preview)
        color1_layout.addWidget(self.color1_checkbox)
        color1_layout.addWidget(self.color1_label1)
        color1_layout.addWidget(self.color1_input)
        color1_layout.addWidget(self.color1_button)
        color1_layout.addWidget(self.color1_label2)
        color1_layout.addWidget(self.tolerance_input1)
        layout.addLayout(color1_layout)

        # 색 선택2
        self.color2_checkbox = QCheckBox()
        self.color2_checkbox.setChecked(True)
        self.color2_checkbox.stateChanged.connect(self.toggle_color2_input)
        self.color2_preview = QLabel("2")
        self.color2_preview.setFixedSize(20, 20)
        self.color2_preview.setStyleSheet("background-color: #00ff00; border: 1px solid black; border-radius: 10px;")
        self.color2_preview.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.color2_label1 = QLabel("색상2")
        self.color2_label1.setFixedSize(30, 20)
        self.color2_label1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.color2_label2 = QLabel("오차값")
        self.color2_label2.setFixedSize(50, 20)
        self.color2_label2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.color2_input = QLineEdit("#000000")
        self.color2_input.setFixedWidth(60)
        self.color2_input.textChanged.connect(lambda text: self.update_preview(self.color2_button, text))
        self.color2_button = QPushButton()
        self.color2_button.setFixedSize(20, 20)
        self.color2_button.setStyleSheet("background-color: #000000; border: 1px solid black;")
        self.color2_button.clicked.connect(lambda: self.select_color(self.color2_input))
        self.tolerance_input2 = QLineEdit("10")
        self.tolerance_input2.setFixedWidth(40)
        self.tolerance_input2.setValidator(QIntValidator(0, 255))

        color2_layout = QHBoxLayout()
        color2_layout.addWidget(self.color2_preview)
        color2_layout.addWidget(self.color2_checkbox)
        color2_layout.addWidget(self.color2_label1)
        color2_layout.addWidget(self.color2_input)
        color2_layout.addWidget(self.color2_button)
        color2_layout.addWidget(self.color2_label2)
        color2_layout.addWidget(self.tolerance_input2)
        layout.addLayout(color2_layout)

        self.roi_edit_button = QPushButton("위치/크기 설정")
        self.roi_edit_button.clicked.connect(self.toggle_roi_edit_mode)

        self.start_button = QPushButton("시작")
        self.start_button.clicked.connect(self.toggle_monitoring)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.roi_edit_button)
        button_layout.addWidget(self.start_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def toggle_color2_input(self, state):
        enabled = state == Qt.Checked
        self.color2_input.setEnabled(enabled)
        self.color2_button.setEnabled(enabled)
        self.tolerance_input2.setEnabled(enabled)

    def update_preview(self, button_widget, color_code):
        if QColor(color_code).isValid():
            button_widget.setStyleSheet(f"background-color: {color_code}; border: 1px solid black;")
        else:
            button_widget.setStyleSheet(f"background-color: #000000; border: 1px solid black;")

    def select_color(self, line_edit: QLineEdit):
        color = QColorDialog.getColor()
        if color.isValid():
            line_edit.setText(color.name())
            if line_edit == self.color1_input:
                self.color1_button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
            elif line_edit == self.color2_input:
                self.color2_button.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")

    def toggle_monitoring(self):
        if not self.monitoring:
            try:
                self.tolerance1 = int(self.tolerance_input1.text())
            except ValueError:
                self.tolerance1 = 0
            try:
                self.tolerance2 = int(self.tolerance_input2.text())
            except ValueError:
                self.tolerance2 = 0
            self.start_button.setText("중지")
            self.monitoring = True
            self.timer.start(500)
            # print("모니터링 시작")
        else:
            self.start_button.setText("시작")
            self.monitoring = False
            self.timer.stop()
            self.overlay.detected_points1 = []
            self.overlay.detected_points2 = []
            # print("모니터링 중지")

    def toggle_roi_edit_mode(self):
        if self.roi_edit_button.text() == "위치/크기 설정":
            self.overlay.set_editable_mode(True)
            self.roi_edit_button.setText("설정 완료")
        else:
            self.overlay.set_editable_mode(False)
            self.roi_edit_button.setText("위치/크기 설정")

    def hex_to_rgb(self, hex_color):
        color = QColor(hex_color)
        return (color.red(), color.green(), color.blue())

    def check_roi_colors(self):
        rect = self.overlay.roi_rect
        margin = 3
        bbox = (
            rect.x() + margin,
            rect.y() + margin,
            rect.x() + rect.width() - margin,
            rect.y() + rect.height() - margin
        )
        img = ImageGrab.grab(bbox=bbox).convert("RGB")
        img_np = np.array(img)

        color1 = self.hex_to_rgb(self.color1_input.text())
        points1 = self.find_color_points(img_np, color1, bbox[:2], self.tolerance1)

        if self.color2_checkbox.isChecked():
            color2 = self.hex_to_rgb(self.color2_input.text())
            points2 = self.find_color_points(img_np, color2, bbox[:2], self.tolerance2)
        else:
            points2 = []

        self.overlay.detected_points1 = points1
        self.overlay.detected_points2 = points2

    def find_color_points(self, image, target_bgr, offset, tolerance=10):
        target = np.array(target_bgr)
        lower = np.clip(target - tolerance, 0, 255)
        upper = np.clip(target + tolerance, 0, 255)
        mask = np.all((image >= lower) & (image <= upper), axis=-1)
        points = np.argwhere(mask)
        return [QPoint(offset[0] + p[1], offset[1] + p[0]) for p in points]  # 간격 두고 추림

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorMonitorApp()
    window.show()
    sys.exit(app.exec_())