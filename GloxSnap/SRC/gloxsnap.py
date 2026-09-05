# ============================================================
# GLOX SNAP
# Lightweight Screenshot Widget
# ============================================================

import sys
import os
import time

from PySide6.QtCore import Qt, QRect, QPoint, QTimer
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QFont,
    QPixmap,
    QGuiApplication,
)
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QFileDialog,
)


# ============================================================
# REGION SELECTOR
# ============================================================

class RegionSelector(QWidget):

    def __init__(self, callback):

        super().__init__()

        self.callback = callback
        self.origin = QPoint()
        self.current = QPoint()
        self.selecting = False

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.setCursor(
            Qt.CrossCursor
        )

        # Cover the virtual desktop
        geometry = QGuiApplication.primaryScreen().virtualGeometry()

        self.setGeometry(
            geometry
        )

        self.show()

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.origin = event.position().toPoint()
            self.current = self.origin
            self.selecting = True

            self.update()

    def mouseMoveEvent(self, event):

        if self.selecting:

            self.current = event.position().toPoint()

            self.update()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton and self.selecting:

            self.selecting = False

            rect = QRect(
                self.origin,
                self.current
            ).normalized()

            if rect.width() >= 5 and rect.height() >= 5:

                global_rect = QRect(
                    self.mapToGlobal(rect.topLeft()),
                    rect.size()
                )

                self.close()

                QTimer.singleShot(
                    100,
                    lambda: self.callback(global_rect)
                )

            else:

                self.close()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:

            self.close()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        # Dark overlay

        painter.fillRect(
            self.rect(),
            QColor(0, 0, 0, 110)
        )

        if self.selecting:

            rect = QRect(
                self.origin,
                self.current
            ).normalized()

            # Clear selected region visually

            painter.setCompositionMode(
                QPainter.CompositionMode_Clear
            )

            painter.fillRect(
                rect,
                Qt.transparent
            )

            painter.setCompositionMode(
                QPainter.CompositionMode_SourceOver
            )

            painter.setPen(
                QPen(
                    QColor(120, 220, 255),
                    2
                )
            )

            painter.setBrush(
                Qt.NoBrush
            )

            painter.drawRect(
                rect
            )

            # Dimensions

            painter.setPen(
                Qt.white
            )

            painter.setFont(
                QFont(
                    "Segoe UI",
                    9,
                    QFont.Weight.Bold
                )
            )

            painter.drawText(
                rect.x(),
                max(
                    20,
                    rect.y() - 8
                ),
                f"{rect.width()} × {rect.height()}"
            )


# ============================================================
# GLOX SNAP
# ============================================================

class GloxSnap(QWidget):

    WIDTH = 280
    HEIGHT = 250

    THEMES = {

        "Obsidian": {
            "bg": QColor(28, 29, 33),
            "panel": QColor(38, 40, 46),
            "accent": QColor(120, 220, 255),
            "text": QColor(240, 240, 245),
            "muted": QColor(150, 155, 165),
        },

        "Graphite": {
            "bg": QColor(34, 35, 39),
            "panel": QColor(46, 47, 52),
            "accent": QColor(170, 220, 255),
            "text": QColor(242, 242, 245),
            "muted": QColor(155, 158, 165),
        },

        "Charcoal": {
            "bg": QColor(39, 37, 36),
            "panel": QColor(52, 49, 47),
            "accent": QColor(255, 205, 120),
            "text": QColor(245, 240, 235),
            "muted": QColor(170, 160, 150),
        },

        "Espresso": {
            "bg": QColor(43, 34, 30),
            "panel": QColor(57, 44, 38),
            "accent": QColor(255, 185, 110),
            "text": QColor(245, 235, 225),
            "muted": QColor(175, 150, 135),
        },

        "Slate": {
            "bg": QColor(29, 38, 44),
            "panel": QColor(40, 51, 58),
            "accent": QColor(110, 225, 255),
            "text": QColor(235, 245, 248),
            "muted": QColor(150, 170, 180),
        },

        "Midnight": {
            "bg": QColor(25, 28, 40),
            "panel": QColor(36, 40, 56),
            "accent": QColor(145, 170, 255),
            "text": QColor(235, 238, 250),
            "muted": QColor(150, 158, 185),
        },
    }

    def __init__(self):

        super().__init__()

        self.theme = "Obsidian"
        self.opacity_value = 100

        self.dragging = False
        self.drag_offset = QPoint()

        self.delay_seconds = 0
        self.last_pixmap = None

        self.save_directory = os.path.join(
            os.path.expanduser("~"),
            "Pictures",
            "GLOX Screenshots"
        )

        os.makedirs(
            self.save_directory,
            exist_ok=True
        )

        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        self.setWindowTitle(
            "GLOX Snap"
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        screen = QGuiApplication.primaryScreen()

        if screen:

            geometry = screen.availableGeometry()

            self.move(
                geometry.right()
                - self.WIDTH
                - 30,

                geometry.top()
                + 40
            )

        self.update()


    # ========================================================
    # SCREEN CAPTURE
    # ========================================================

    def capture_screen(self):

        self.hide()

        QTimer.singleShot(
            120,
            self._capture_screen
        )

    def _capture_screen(self):

        screen = QGuiApplication.primaryScreen()

        if not screen:
            self.show()
            return

        pixmap = screen.grabWindow(0)

        self.handle_capture(
            pixmap
        )


    # ========================================================
    # REGION CAPTURE
    # ========================================================

    def capture_region(self):

        self.hide()

        QTimer.singleShot(
            150,
            self._start_region_selector
        )

    def _start_region_selector(self):

        self.selector = RegionSelector(
            self.capture_region_rect
        )


    def capture_region_rect(self, rect):

        screen = QGuiApplication.screenAt(
            rect.center()
        )

        if not screen:

            self.show()
            return

        geometry = screen.geometry()

        local_rect = QRect(
            rect.x() - geometry.x(),
            rect.y() - geometry.y(),
            rect.width(),
            rect.height()
        )

        pixmap = screen.grabWindow(
            0,
            local_rect.x(),
            local_rect.y(),
            local_rect.width(),
            local_rect.height()
        )

        self.handle_capture(
            pixmap
        )


    # ========================================================
    # ACTIVE WINDOW
    # ========================================================

    def capture_window(self):

        self.hide()

        QTimer.singleShot(
            150,
            self._capture_window
        )


    def _capture_window(self):

        window = QGuiApplication.focusWindow()

        if window:

            try:

                screen = window.screen()

                pixmap = screen.grabWindow(
                    window.winId()
                )

                self.handle_capture(
                    pixmap
                )

                return

            except Exception:
                pass

        # Fallback

        self._capture_screen()


    # ========================================================
    # CAPTURE HANDLER
    # ========================================================

    def handle_capture(self, pixmap):

        self.last_pixmap = pixmap

        self.copy_to_clipboard()

        self.save_screenshot(
            pixmap
        )

        self.show()

        self.show_status(
            "Screenshot captured"
        )


    # ========================================================
    # COPY
    # ========================================================

    def copy_to_clipboard(self):

        if self.last_pixmap:

            QApplication.clipboard().setPixmap(
                self.last_pixmap
            )


    # ========================================================
    # SAVE
    # ========================================================

    def save_screenshot(self, pixmap=None):

        if pixmap is None:

            pixmap = self.last_pixmap

        if not pixmap:
            return

        timestamp = time.strftime(
            "%Y%m%d_%H%M%S"
        )

        path = os.path.join(
            self.save_directory,
            f"GLOX_Snap_{timestamp}.png"
        )

        pixmap.save(
            path,
            "PNG"
        )


    # ========================================================
    # SAVE AS
    # ========================================================

    def save_as(self):

        if not self.last_pixmap:

            self.show_status(
                "No screenshot yet"
            )

            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save GLOX Screenshot",
            os.path.join(
                self.save_directory,
                "GLOX_Screenshot.png"
            ),
            "PNG Image (*.png)"
        )

        if path:

            self.last_pixmap.save(
                path,
                "PNG"
            )

            self.show_status(
                "Screenshot saved"
            )


    # ========================================================
    # FOLDER
    # ========================================================

    def choose_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Screenshot Folder",
            self.save_directory
        )

        if folder:

            self.save_directory = folder

            self.show_status(
                "Folder updated"
            )


    # ========================================================
    # DELAY
    # ========================================================

    def set_delay(self, seconds):

        self.delay_seconds = seconds

        self.show_status(
            f"Delay: {seconds}s"
        )


    # ========================================================
    # STATUS
    # ========================================================

    def show_status(self, text):

        self.status_text = text

        self.update()

        QTimer.singleShot(
            1800,
            self.clear_status
        )


    def clear_status(self):

        self.status_text = ""

        self.update()


    # ========================================================
    # THEME
    # ========================================================

    def change_theme(self, name):

        self.theme = name

        self.update()


    # ========================================================
    # OPACITY
    # ========================================================

    def change_opacity(self, value):

        self.opacity_value = value

        self.setWindowOpacity(
            value / 100
        )


    # ========================================================
    # MENU
    # ========================================================

    def show_menu(self, position):

        menu = QMenu(
            self
        )

        menu.setStyleSheet("""
            QMenu {
                background: #252525;
                color: white;
                border: 1px solid #444444;
                padding: 5px;
                border-radius: 8px;
            }

            QMenu::item {
                padding: 7px 28px 7px 12px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background: #3a3a3a;
            }

            QMenu::separator {
                height: 1px;
                background: #444444;
                margin: 5px;
            }
        """)

        # ----------------------------------------------------
        # Delay
        # ----------------------------------------------------

        delay_menu = menu.addMenu(
            "Delay"
        )

        for seconds in (0, 3, 5):

            action = delay_menu.addAction(
                "No Delay"
                if seconds == 0
                else f"{seconds} Seconds"
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                seconds == self.delay_seconds
            )

            action.triggered.connect(
                lambda checked=False,
                s=seconds:
                self.set_delay(s)
            )

        # ----------------------------------------------------
        # Theme
        # ----------------------------------------------------

        theme_menu = menu.addMenu(
            "Theme"
        )

        for name in self.THEMES:

            action = theme_menu.addAction(
                name
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                name == self.theme
            )

            action.triggered.connect(
                lambda checked=False,
                n=name:
                self.change_theme(n)
            )

        # ----------------------------------------------------
        # Opacity
        # ----------------------------------------------------

        opacity_menu = menu.addMenu(
            "Opacity"
        )

        for value in (100, 80, 60, 50):

            action = opacity_menu.addAction(
                f"{value}%"
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                value == self.opacity_value
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.change_opacity(v)
            )

        # ----------------------------------------------------
        # Save folder
        # ----------------------------------------------------

        menu.addSeparator()

        folder_action = menu.addAction(
            "Screenshot Folder..."
        )

        folder_action.triggered.connect(
            self.choose_folder
        )

        save_action = menu.addAction(
            "Save Last Screenshot As..."
        )

        save_action.triggered.connect(
            self.save_as
        )

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

        menu.addSeparator()

        exit_action = menu.addAction(
            "Exit"
        )

        exit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(
            position
        )


    # ========================================================
    # BUTTONS
    # ========================================================

    def button_at(self, x, y):

        # Full screen

        if (
            20 <= x <= 260
            and 70 <= y <= 108
        ):
            return "screen"

        # Region

        if (
            20 <= x <= 140
            and 118 <= y <= 156
        ):
            return "region"

        # Window

        if (
            150 <= x <= 260
            and 118 <= y <= 156
        ):
            return "window"

        # Save

        if (
            20 <= x <= 260
            and 166 <= y <= 201
        ):
            return "save"

        return None


    # ========================================================
    # MOUSE PRESS
    # ========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:

            self.show_menu(
                event.globalPosition().toPoint()
            )

            return

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.drag_offset = (
                event.globalPosition()
                - self.frameGeometry().topLeft()
            )

            event.accept()


    # ========================================================
    # MOUSE MOVE
    # ========================================================

    def mouseMoveEvent(self, event):

        if (
            self.dragging
            and event.buttons()
            & Qt.LeftButton
        ):

            new_position = (
                event.globalPosition()
                - self.drag_offset
            ).toPoint()

            self.move(
                new_position
            )

            event.accept()


    # ========================================================
    # MOUSE RELEASE
    # ========================================================

    def mouseReleaseEvent(self, event):

        if event.button() != Qt.LeftButton:
            return

        self.dragging = False

        x = int(
            event.position().x()
        )

        y = int(
            event.position().y()
        )

        button = self.button_at(
            x,
            y
        )

        if button == "screen":

            if self.delay_seconds:

                self.hide()

                QTimer.singleShot(
                    self.delay_seconds * 1000,
                    self._capture_after_delay
                )

            else:

                self.capture_screen()

        elif button == "region":

            if self.delay_seconds:

                self.hide()

                QTimer.singleShot(
                    self.delay_seconds * 1000,
                    self._region_after_delay
                )

            else:

                self.capture_region()

        elif button == "window":

            if self.delay_seconds:

                self.hide()

                QTimer.singleShot(
                    self.delay_seconds * 1000,
                    self._window_after_delay
                )

            else:

                self.capture_window()

        elif button == "save":

            self.save_as()

        event.accept()


    # ========================================================
    # DELAYED ACTIONS
    # ========================================================

    def _capture_after_delay(self):

        self._capture_screen()


    def _region_after_delay(self):

        self._start_region_selector()


    def _window_after_delay(self):

        self._capture_window()


    # ========================================================
    # PAINT
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        theme = self.THEMES[
            self.theme
        ]

        bg = theme["bg"]
        panel = theme["panel"]
        accent = theme["accent"]
        text = theme["text"]
        muted = theme["muted"]

        # ----------------------------------------------------
        # Shadow
        # ----------------------------------------------------

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

        painter.drawRoundedRect(
            6,
            7,
            self.WIDTH - 12,
            self.HEIGHT - 12,
            18,
            18
        )

        # ----------------------------------------------------
        # Main background
        # ----------------------------------------------------

        painter.setBrush(
            bg
        )

        painter.drawRoundedRect(
            2,
            2,
            self.WIDTH - 6,
            self.HEIGHT - 6,
            18,
            18
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        painter.setPen(
            text
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                11,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            20,
            30,
            "GLOX SNAP"
        )

        painter.setPen(
            muted
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                8
            )
        )

        painter.drawText(
            20,
            47,
            "SCREENSHOT UTILITY"
        )

        # ----------------------------------------------------
        # Full Screen
        # ----------------------------------------------------

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            panel
        )

        painter.drawRoundedRect(
            20,
            70,
            240,
            38,
            10,
            10
        )

        painter.setPen(
            text
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            20,
            70,
            240,
            38,
            Qt.AlignCenter,
            "FULL SCREEN"
        )

        # ----------------------------------------------------
        # Region
        # ----------------------------------------------------

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            panel
        )

        painter.drawRoundedRect(
            20,
            118,
            115,
            38,
            10,
            10
        )

        painter.setBrush(
            panel
        )

        painter.drawRoundedRect(
            145,
            118,
            115,
            38,
            10,
            10
        )

        painter.setPen(
            text
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                8,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            20,
            118,
            115,
            38,
            Qt.AlignCenter,
            "REGION"
        )

        painter.drawText(
            145,
            118,
            115,
            38,
            Qt.AlignCenter,
            "WINDOW"
        )

        # ----------------------------------------------------
        # Save
        # ----------------------------------------------------

        painter.setPen(
            QPen(
                accent,
                1
            )
        )

        painter.setBrush(
                QColor(
                    accent.red(),
                    accent.green(),
                    accent.blue(),
                    25
                )
        )

        painter.drawRoundedRect(
            20,
            166,
            240,
            36,
            10,
            10
        )

        painter.setPen(
            accent
        )

        painter.drawText(
            20,
            166,
            240,
            36,
            Qt.AlignCenter,
            "SAVE LAST SCREENSHOT"
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        status = getattr(
            self,
            "status_text",
            ""
        )

        if status:

            painter.setPen(
                accent
            )

            painter.setFont(
                QFont(
                    "Segoe UI",
                    8,
                    QFont.Weight.Bold
                )
            )

            painter.drawText(
                20,
                224,
                240,
                15,
                Qt.AlignCenter,
                status
            )

        else:

            painter.setPen(
                muted
            )

            painter.setFont(
                QFont(
                    "Segoe UI",
                    7
                )
            )

            painter.drawText(
                20,
                224,
                240,
                15,
                Qt.AlignCenter,
                "Right-click for options"
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    app.setStyle(
        "Fusion"
    )

    app.setQuitOnLastWindowClosed(
        True
    )

    widget = GloxSnap()

    widget.show()

    sys.exit(
        app.exec()
    )