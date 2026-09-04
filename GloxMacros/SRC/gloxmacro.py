# ============================================================
# GLOX MACRO
# Lightweight 3-slot mouse + keyboard macro recorder
# ============================================================

import sys
import json
import time
import threading
import os

from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)

from pynput import mouse, keyboard


# ============================================================
# CONFIG
# ============================================================

CONFIG_FILE = os.path.join(
    os.path.expanduser("~"),
    ".glox_macro.json"
)


# ============================================================
# MACRO RECORDER
# ============================================================

class MacroRecorder:

    def __init__(self):
        self.recording = False
        self.events = []
        self.start_time = 0

        self.mouse_listener = None
        self.keyboard_listener = None

    def start(self):
        self.events = []
        self.recording = True
        self.start_time = time.perf_counter()

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll,
        )

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release,
        )

        self.mouse_listener.start()
        self.keyboard_listener.start()

    def elapsed(self):
        return time.perf_counter() - self.start_time

    def on_move(self, x, y):
        if not self.recording:
            return

        self.events.append({
            "type": "move",
            "x": x,
            "y": y,
            "time": self.elapsed(),
        })

    def on_click(self, x, y, button, pressed):
        if not self.recording:
            return

        self.events.append({
            "type": "click",
            "x": x,
            "y": y,
            "button": button.name,
            "pressed": pressed,
            "time": self.elapsed(),
        })

    def on_scroll(self, x, y, dx, dy):
        if not self.recording:
            return

        self.events.append({
            "type": "scroll",
            "x": x,
            "y": y,
            "dx": dx,
            "dy": dy,
            "time": self.elapsed(),
        })

    def on_key_press(self, key):
        if not self.recording:
            return

        self.events.append({
            "type": "key_press",
            "key": self.serialize_key(key),
            "time": self.elapsed(),
        })

    def on_key_release(self, key):
        if not self.recording:
            return

        self.events.append({
            "type": "key_release",
            "key": self.serialize_key(key),
            "time": self.elapsed(),
        })

    def serialize_key(self, key):

        try:
            if hasattr(key, "char") and key.char is not None:
                return {
                    "kind": "char",
                    "value": key.char,
                }

            return {
                "kind": "special",
                "value": str(key),
            }

        except Exception:
            return {
                "kind": "special",
                "value": str(key),
            }

    def stop(self):

        self.recording = False

        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None

        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None

        return self.events


# ============================================================
# MACRO PLAYER
# ============================================================

class MacroPlayer:

    def __init__(self):
        self.running = False

    def play(self, events):

        if not events or self.running:
            return

        thread = threading.Thread(
            target=self._play,
            args=(events,),
            daemon=True,
        )

        thread.start()

    def _play(self, events):

        self.running = True

        controller_mouse = mouse.Controller()
        controller_keyboard = keyboard.Controller()

        previous_time = 0

        try:

            for event in events:

                if not self.running:
                    break

                delay = event["time"] - previous_time

                if delay > 0:
                    time.sleep(delay)

                previous_time = event["time"]

                event_type = event["type"]

                # ----------------------------
                # Mouse movement
                # ----------------------------

                if event_type == "move":

                    controller_mouse.position = (
                        event["x"],
                        event["y"],
                    )

                # ----------------------------
                # Mouse click
                # ----------------------------

                elif event_type == "click":

                    button = self.get_mouse_button(
                        event["button"]
                    )

                    if button:

                        if event["pressed"]:
                            controller_mouse.press(button)
                        else:
                            controller_mouse.release(button)

                # ----------------------------
                # Mouse scroll
                # ----------------------------

                elif event_type == "scroll":

                    controller_mouse.scroll(
                        event["dx"],
                        event["dy"],
                    )

                # ----------------------------
                # Keyboard
                # ----------------------------

                elif event_type == "key_press":

                    key = self.get_key(
                        event["key"]
                    )

                    if key:
                        controller_keyboard.press(key)

                elif event_type == "key_release":

                    key = self.get_key(
                        event["key"]
                    )

                    if key:
                        controller_keyboard.release(key)

        except Exception:
            pass

        self.running = False

    @staticmethod
    def get_mouse_button(name):

        mapping = {
            "left": mouse.Button.left,
            "right": mouse.Button.right,
            "middle": mouse.Button.middle,
        }

        return mapping.get(name)

    @staticmethod
    def get_key(data):

        try:

            if data["kind"] == "char":
                return data["value"]

            value = data["value"]

            # pynput special key strings look like:
            # Key.enter, Key.ctrl, etc.

            if value.startswith("Key."):
                name = value[4:]

                return getattr(
                    keyboard.Key,
                    name,
                    None,
                )

        except Exception:
            pass

        return None


# ============================================================
# RECORDING DIALOG
# ============================================================

class RecordingDialog(QDialog):

    def __init__(self, slot, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            f"GLOX Macro — Recording M{slot}"
        )

        self.setFixedSize(
            280,
            150
        )

        self.setStyleSheet("""
            QDialog {
                background: #252525;
                color: white;
                border: 1px solid #555555;
            }

            QLabel {
                color: white;
            }

            QPushButton {
                background: #353535;
                color: white;
                border: 1px solid #555555;
                border-radius: 7px;
                padding: 8px;
            }

            QPushButton:hover {
                background: #444444;
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel(
            f"●  Recording M{slot}"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Weight.Bold
            )
        )

        self.info = QLabel(
            "Perform your actions...\n"
            "Click STOP when finished."
        )

        self.info.setAlignment(
            Qt.AlignCenter
        )

        stop_button = QPushButton(
            "STOP RECORDING"
        )

        stop_button.clicked.connect(
            self.accept
        )

        layout.addWidget(title)
        layout.addWidget(self.info)
        layout.addWidget(stop_button)


# ============================================================
# GLOX MACRO
# ============================================================

class GloxMacro(QWidget):

    WIDTH = 300
    HEIGHT = 125

    THEMES = {

        "Obsidian": {
            "bg": QColor(35, 35, 40, 220),
            "border": QColor(120, 220, 255),
            "accent": QColor(120, 220, 255),
            "text": QColor(240, 240, 245),
        },

        "Graphite": {
            "bg": QColor(48, 49, 54, 225),
            "border": QColor(170, 220, 255),
            "accent": QColor(170, 220, 255),
            "text": QColor(240, 240, 245),
        },

        "Espresso": {
            "bg": QColor(65, 51, 45, 225),
            "border": QColor(235, 190, 140),
            "accent": QColor(235, 190, 140),
            "text": QColor(245, 235, 225),
        },

        "Slate": {
            "bg": QColor(42, 55, 62, 225),
            "border": QColor(120, 215, 235),
            "accent": QColor(120, 215, 235),
            "text": QColor(235, 245, 248),
        },

        "Midnight": {
            "bg": QColor(34, 38, 55, 225),
            "border": QColor(145, 170, 255),
            "accent": QColor(145, 170, 255),
            "text": QColor(240, 242, 255),
        },

        "Pearl Glass": {
            "bg": QColor(225, 230, 235, 155),
            "border": QColor(255, 255, 255, 190),
            "accent": QColor(80, 100, 115),
            "text": QColor(35, 40, 45),
        },
    }

    def __init__(self):

        super().__init__()

        self.theme = "Obsidian"
        self.opacity_value = 100

        self.dragging = False
        self.drag_offset = QPointF()
        self.drag_distance = 0

        self.recorder = MacroRecorder()
        self.player = MacroPlayer()

        self.macros = [
            [],
            [],
            [],
        ]

        self.load_config()

        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        self.setWindowTitle(
            "GLOX Macro"
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.buttons = []

        self.setup_position()

    # ========================================================
    # POSITION
    # ========================================================

    def setup_position(self):

        screen = QApplication.primaryScreen()

        if screen:

            geometry = screen.availableGeometry()

            self.move(
                geometry.right()
                - self.WIDTH
                - 35,

                geometry.bottom()
                - self.HEIGHT
                - 35
            )

    # ========================================================
    # CONFIG
    # ========================================================

    def load_config(self):

        try:

            if os.path.exists(CONFIG_FILE):

                with open(
                    CONFIG_FILE,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

                    self.macros = data.get(
                        "macros",
                        [[], [], []]
                    )

                    self.theme = data.get(
                        "theme",
                        "Obsidian"
                    )

                    self.opacity_value = data.get(
                        "opacity",
                        100
                    )

        except Exception:

            self.macros = [
                [],
                [],
                [],
            ]

    def save_config(self):

        try:

            data = {
                "macros": self.macros,
                "theme": self.theme,
                "opacity": self.opacity_value,
            }

            with open(
                CONFIG_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=2
                )

        except Exception:
            pass

    # ========================================================
    # RECORD
    # ========================================================

    def record_macro(self, index):

        if self.recorder.recording:
            return

        dialog = RecordingDialog(
            index + 1,
            self
        )

        self.recorder.start()

        dialog.exec()

        events = self.recorder.stop()

        # Ignore the recorder's own stop-button interaction
        # by keeping only events that were captured before
        # recording ended.

        if events:

            self.macros[index] = events

            self.save_config()

        self.update()

    # ========================================================
    # PLAY
    # ========================================================

    def play_macro(self, index):

        if self.macros[index]:

            self.player.play(
                self.macros[index]
            )

    # ========================================================
    # CLEAR
    # ========================================================

    def clear_macro(self, index):

        self.macros[index] = []

        self.save_config()

        self.update()

    # ========================================================
    # PAINT
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        theme = self.THEMES[
            self.theme
        ]

        # Shadow

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            QColor(
                0,
                0,
                0,
                80
            )
        )

        painter.drawRoundedRect(
            5,
            6,
            self.WIDTH - 10,
            self.HEIGHT - 10,
            18,
            18
        )

        # Glass body

        painter.setBrush(
            theme["bg"]
        )

        painter.setPen(
            QPen(
                theme["border"],
                1
            )
        )

        painter.drawRoundedRect(
            2,
            2,
            self.WIDTH - 6,
            self.HEIGHT - 6,
            18,
            18
        )

        # Header

        painter.setPen(
            theme["text"]
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            18,
            24,
            "GLOX  MACRO"
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                7
            )
        )

        painter.drawText(
            18,
            39,
            "QUICK ACTION RECORDER"
        )

        # Buttons

        for i in range(3):

            x = 15 + i * 93
            y = 52

            recorded = bool(
                self.macros[i]
            )

            # Button background

            if recorded:

                bg = QColor(
                    theme["accent"]
                )

                bg.setAlpha(45)

            else:

                bg = QColor(
                    255,
                    255,
                    255,
                    15
                )

            painter.setBrush(bg)

            painter.setPen(
                QPen(
                    theme["border"],
                    1
                )
            )

            painter.drawRoundedRect(
                x,
                y,
                82,
                55,
                12,
                12
            )

            # Slot number

            painter.setPen(
                theme["text"]
            )

            painter.setFont(
                QFont(
                    "Segoe UI",
                    11,
                    QFont.Weight.Bold
                )
            )

            painter.drawText(
                x + 10,
                y + 21,
                f"M{i + 1}"
            )

            # Status

            painter.setFont(
                QFont(
                    "Segoe UI",
                    7
                )
            )

            if recorded:

                painter.setPen(
                    theme["accent"]
                )

                painter.drawText(
                    x + 10,
                    y + 40,
                    "READY"
                )

            else:

                painter.setPen(
                    theme["text"]
                )

                painter.drawText(
                    x + 10,
                    y + 40,
                    "RECORD"
                )

            # Record indicator

            painter.setBrush(
                theme["accent"]
                if recorded
                else QColor(
                    255,
                    255,
                    255,
                    70
                )
            )

            painter.setPen(
                Qt.NoPen
            )

            painter.drawEllipse(
                x + 61,
                y + 17,
                8,
                8
            )

        painter.setPen(
            QColor(
                theme["text"]
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                6
            )
        )

        painter.drawText(
            18,
            118,
            "Left click: replay   •   Right click: options"
        )

    # ========================================================
    # MOUSE
    # ========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:

            self.show_menu(
                event.globalPosition().toPoint()
            )

            return

        if event.button() == Qt.LeftButton:

            x = event.position().x()
            y = event.position().y()

            if 52 <= y <= 107:

                for i in range(3):

                    bx = 15 + i * 93

                    if bx <= x <= bx + 82:

                        self.play_macro(i)

                        return

            self.dragging = True

            self.drag_distance = 0

            self.drag_offset = (
                event.globalPosition()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if (
            self.dragging
            and event.buttons() & Qt.LeftButton
        ):

            new_pos = (
                event.globalPosition()
                - self.drag_offset
            ).toPoint()

            self.drag_distance += (
                abs(
                    new_pos.x()
                    - self.x()
                )
                +
                abs(
                    new_pos.y()
                    - self.y()
                )
            )

            self.move(
                new_pos
            )

            event.accept()

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = False

            event.accept()

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
                border: 1px solid #555555;
                padding: 5px;
            }

            QMenu::item {
                padding: 7px 28px 7px 12px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background: #3b3b3b;
            }

            QMenu::separator {
                height: 1px;
                background: #444444;
                margin: 5px;
            }
        """)

        # ----------------------------------------------------
        # Record
        # ----------------------------------------------------

        record_menu = menu.addMenu(
            "Record Macro"
        )

        for i in range(3):

            action = record_menu.addAction(
                f"Record M{i + 1}"
            )

            action.triggered.connect(
                lambda checked=False,
                index=i:
                self.record_macro(index)
            )

        # ----------------------------------------------------
        # Clear
        # ----------------------------------------------------

        clear_menu = menu.addMenu(
            "Clear Macro"
        )

        for i in range(3):

            action = clear_menu.addAction(
                f"Clear M{i + 1}"
            )

            action.triggered.connect(
                lambda checked=False,
                index=i:
                self.clear_macro(index)
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

        for value in (
            100,
            80,
            60,
            50
        ):

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

        menu.addSeparator()

        # ----------------------------------------------------
        # Refresh
        # ----------------------------------------------------

        refresh_action = menu.addAction(
            "Refresh"
        )

        refresh_action.triggered.connect(
            self.refresh
        )

        menu.addSeparator()

        # ----------------------------------------------------
        # Exit
        # ----------------------------------------------------

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
    # SETTINGS
    # ========================================================

    def change_theme(self, name):

        self.theme = name

        self.save_config()

        self.update()

    def change_opacity(self, value):

        self.opacity_value = value

        self.setWindowOpacity(
            value / 100
        )

        self.save_config()

    def refresh(self):

        self.load_config()

        self.setWindowOpacity(
            self.opacity_value / 100
        )

        self.update()

    # ========================================================
    # CLOSE
    # ========================================================

    def closeEvent(self, event):

        if self.recorder.recording:
            self.recorder.stop()

        self.save_config()

        event.accept()


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

    widget = GloxMacro()

    widget.show()

    sys.exit(
        app.exec()
    )