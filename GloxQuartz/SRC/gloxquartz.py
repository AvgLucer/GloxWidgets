import sys
import math
import ctypes
from datetime import datetime

from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QSystemTrayIcon,
)


# =============================================================
# WINDOWS API
# =============================================================

user32 = ctypes.windll.user32

GetForegroundWindow = user32.GetForegroundWindow
GetForegroundWindow.restype = ctypes.c_void_p

GetWindowThreadProcessId = user32.GetWindowThreadProcessId
GetWindowThreadProcessId.argtypes = [
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_ulong)
]
GetWindowThreadProcessId.restype = ctypes.c_ulong


# =============================================================
# QUARTZ
# =============================================================

class Quartz(QWidget):

    SIZE = 240

    # ---------------------------------------------------------
    # CLASSY DARK THEMES
    # ---------------------------------------------------------

    THEMES = {

        "Warm Brown":
            QColor(55, 52, 48, 248),

        "Obsidian":
            QColor(25, 26, 28, 248),

        "Graphite":
            QColor(38, 40, 42, 248),

        "Charcoal":
            QColor(45, 45, 44, 248),

        "Espresso":
            QColor(48, 39, 34, 248),

        "Slate":
            QColor(39, 43, 47, 248),

        "Midnight":
            QColor(27, 30, 38, 248),
    }

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "GLOX Quartz"
        )

        self.setFixedSize(
            self.SIZE,
            self.SIZE
        )

        # -----------------------------------------------------
        # Floating window
        # -----------------------------------------------------

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        # -----------------------------------------------------
        # Current theme
        # -----------------------------------------------------

        self.current_theme = "Warm Brown"

        # -----------------------------------------------------
        # Dragging
        # -----------------------------------------------------

        self.dragging = False
        self.drag_offset = QPointF()

        # -----------------------------------------------------
        # Clock timer
        # -----------------------------------------------------

        self.clock_timer = QTimer(self)

        self.clock_timer.timeout.connect(
            self.update
        )

        # ~60 FPS = smooth hands
        self.clock_timer.start(16)

        # -----------------------------------------------------
        # Application detection
        # -----------------------------------------------------

        self.opacity_timer = QTimer(self)

        self.opacity_timer.timeout.connect(
            self.check_foreground_window
        )

        self.opacity_timer.start(250)

    # =========================================================
    # FOREGROUND APPLICATION DETECTION
    # =========================================================

    def check_foreground_window(self):

        foreground = GetForegroundWindow()

        if not foreground:
            return

        own_hwnd = int(
            self.winId()
        )

        foreground_hwnd = int(
            foreground
        )

        # -----------------------------------------------------
        # If Quartz itself is focused
        # -----------------------------------------------------

        if foreground_hwnd == own_hwnd:

            self.setWindowOpacity(
                1.0
            )

            return

        # -----------------------------------------------------
        # Otherwise another window is active
        # -----------------------------------------------------

        self.setWindowOpacity(
            0.50
        )

    # =========================================================
    # PAINT
    # =========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.setRenderHint(
            QPainter.TextAntialiasing
        )

        center = QPointF(
            self.width() / 2,
            self.height() / 2
        )

        radius = (
            self.SIZE / 2 - 10
        )

        # =====================================================
        # SHADOW
        # =====================================================

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            QColor(
                0,
                0,
                0,
                100
            )
        )

        painter.drawEllipse(
            center,
            radius + 4,
            radius + 4
        )

        # =====================================================
        # CLOCK FACE
        # =====================================================

        painter.setBrush(
            self.THEMES[
                self.current_theme
            ]
        )

        painter.drawEllipse(
            center,
            radius,
            radius
        )

        # =====================================================
        # INNER RING
        # =====================================================

        painter.setBrush(
            Qt.NoBrush
        )

        painter.setPen(
            QPen(
                QColor(
                    170,
                    145,
                    110,
                    35
                ),
                2
            )
        )

        painter.drawEllipse(
            center,
            radius - 5,
            radius - 5
        )

        # =====================================================
        # OUTER RING
        # =====================================================

        painter.setPen(
            QPen(
                QColor(
                    235,
                    225,
                    210,
                    55
                ),
                1
            )
        )

        painter.drawEllipse(
            center,
            radius,
            radius
        )

        # =====================================================
        # TICK MARKS
        # =====================================================

        for i in range(60):

            angle = math.radians(
                i * 6
            )

            if i % 5 == 0:

                inner = radius - 25
                outer = radius - 13
                width = 2.5
                alpha = 190

            else:

                inner = radius - 19
                outer = radius - 13
                width = 1
                alpha = 65

            x1 = (
                center.x()
                + math.sin(angle)
                * inner
            )

            y1 = (
                center.y()
                - math.cos(angle)
                * inner
            )

            x2 = (
                center.x()
                + math.sin(angle)
                * outer
            )

            y2 = (
                center.y()
                - math.cos(angle)
                * outer
            )

            painter.setPen(
                QPen(
                    QColor(
                        235,
                        230,
                        220,
                        alpha
                    ),
                    width,
                    Qt.SolidLine,
                    Qt.RoundCap
                )
            )

            painter.drawLine(
                QPointF(x1, y1),
                QPointF(x2, y2)
            )

        # =====================================================
        # NUMBERS
        # =====================================================

        painter.setPen(
            QColor(
                235,
                230,
                220,
                180
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Light
            )
        )

        number_radius = (
            radius - 37
        )

        for number in range(1, 13):

            angle = math.radians(
                number * 30
            )

            x = (
                center.x()
                + math.sin(angle)
                * number_radius
            )

            y = (
                center.y()
                - math.cos(angle)
                * number_radius
            )

            painter.drawText(
                int(x - 15),
                int(y - 10),
                30,
                20,
                Qt.AlignCenter,
                str(number)
            )

        # =====================================================
        # CURRENT TIME
        # =====================================================

        now = datetime.now()

        seconds = (
            now.second
            + now.microsecond / 1_000_000
        )

        minutes = (
            now.minute
            + seconds / 60
        )

        hours = (
            now.hour % 12
            + minutes / 60
        )

        hour_angle = hours * 30
        minute_angle = minutes * 6
        second_angle = seconds * 6

        # =====================================================
        # HOUR HAND
        # White + red tint
        # =====================================================

        self.draw_hand(
            painter,
            center,
            radius * 0.48,
            hour_angle,
            QColor(
                255,
                242,
                242,
                250
            ),
            6
        )

        # =====================================================
        # MINUTE HAND
        # White + green tint
        # =====================================================

        self.draw_hand(
            painter,
            center,
            radius * 0.67,
            minute_angle,
            QColor(
                240,
                255,
                244,
                250
            ),
            4
        )

        # =====================================================
        # SECOND HAND
        # White + gold tint
        # =====================================================

        self.draw_hand(
            painter,
            center,
            radius * 0.76,
            second_angle,
            QColor(
                255,
                248,
                220,
                255
            ),
            2
        )

        # =====================================================
        # SECOND HAND COUNTERWEIGHT
        # =====================================================

        angle = math.radians(
            second_angle
        )

        counter_length = (
            radius * 0.14
        )

        cx = (
            center.x()
            - math.sin(angle)
            * counter_length
        )

        cy = (
            center.y()
            + math.cos(angle)
            * counter_length
        )

        painter.setPen(
            QPen(
                QColor(
                    225,
                    190,
                    110,
                    240
                ),
                2
            )
        )

        painter.drawLine(
            center,
            QPointF(cx, cy)
        )

        # =====================================================
        # CENTER HUB
        # =====================================================

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            QColor(
                230,
                195,
                115,
                255
            )
        )

        painter.drawEllipse(
            center,
            5,
            5
        )

        painter.setBrush(
            QColor(
                45,
                43,
                40,
                255
            )
        )

        painter.drawEllipse(
            center,
            2,
            2
        )

        # =====================================================
        # GLOX
        # =====================================================

        painter.setPen(
            QColor(
                230,
                225,
                215,
                150
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                8,
                QFont.Weight.Medium
            )
        )

        painter.drawText(
            0,
            int(
                center.y()
                + radius * 0.43
            ),
            self.width(),
            18,
            Qt.AlignCenter,
            "GLOX"
        )

    # =========================================================
    # DRAW HAND
    # =========================================================

    def draw_hand(
        self,
        painter,
        center,
        length,
        angle_degrees,
        color,
        width
    ):

        angle = math.radians(
            angle_degrees
        )

        x = (
            center.x()
            + math.sin(angle)
            * length
        )

        y = (
            center.y()
            - math.cos(angle)
            * length
        )

        painter.setPen(
            QPen(
                color,
                width,
                Qt.SolidLine,
                Qt.RoundCap
            )
        )

        painter.drawLine(
            center,
            QPointF(x, y)
        )

    # =========================================================
    # DRAGGING
    # =========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.drag_offset = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            self.setWindowOpacity(
                1.0
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if self.dragging:

            position = (
                event.globalPosition().toPoint()
                - self.drag_offset
            )

            self.move(
                position
            )

            event.accept()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = False

            event.accept()

    # =========================================================
    # RIGHT CLICK MENU
    # =========================================================

    def contextMenuEvent(self, event):

        menu = QMenu(self)

        menu.setStyleSheet("""
            QMenu {
                background: #292825;
                color: #F3EEE5;
                border: 1px solid #4B4842;
                padding: 5px;
            }

            QMenu::item {
                padding: 7px 22px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background: #3D3A35;
            }

            QMenu::separator {
                height: 1px;
                background: #4A4741;
                margin: 5px 8px;
            }
        """)

        # -----------------------------------------------------
        # Background submenu
        # -----------------------------------------------------

        backgrounds = QMenu(
            "Background",
            menu
        )

        backgrounds.setStyleSheet(
            menu.styleSheet()
        )

        for theme_name in self.THEMES:

            action = backgrounds.addAction(
                theme_name
            )

            action.triggered.connect(
                lambda checked=False,
                name=theme_name:
                self.change_theme(name)
            )

        menu.addMenu(
            backgrounds
        )

        # -----------------------------------------------------
        # Opacity
        # -----------------------------------------------------

        opacity_menu = QMenu(
            "Opacity",
            menu
        )

        opacity_menu.setStyleSheet(
            menu.styleSheet()
        )

        for value in [
            100,
            80,
            60,
            50
        ]:

            action = opacity_menu.addAction(
                f"{value}%"
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.setWindowOpacity(
                    v / 100
                )
            )

        menu.addMenu(
            opacity_menu
        )

        menu.addSeparator()

        # -----------------------------------------------------
        # Quit
        # -----------------------------------------------------

        quit_action = menu.addAction(
            "Quit Quartz"
        )

        quit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(
            event.globalPos()
        )

    # =========================================================
    # CHANGE THEME
    # =========================================================

    def change_theme(self, theme):

        self.current_theme = theme

        self.update()


# =============================================================
# MAIN
# =============================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "GLOX Quartz"
    )

    app.setQuitOnLastWindowClosed(
        True
    )

    quartz = Quartz()

    # ---------------------------------------------------------
    # Start top-right
    # ---------------------------------------------------------

    screen = (
        app.primaryScreen()
        .availableGeometry()
    )

    quartz.move(
        screen.right()
        - quartz.width()
        - 35,

        screen.top()
        + 35
    )

    quartz.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()