# ============================================================
# GLOX BAR
# Lightweight Quick Apps Widget
# ============================================================

import sys
import os
import json
import subprocess
import webbrowser

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)


# ============================================================
# CONFIG
# ============================================================

CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "gloxbar_config.json"
)


DEFAULT_CONFIG = {
    "slots": [
        {"name": "App 1", "target": ""},
        {"name": "App 2", "target": ""},
        {"name": "App 3", "target": ""},
    ],
    "theme": "Obsidian",
    "opacity": 100,
}


# ============================================================
# GLOX BAR
# ============================================================

class GloxBar(QWidget):

    THEMES = {

        "Obsidian": {
            "background": QColor(30, 30, 34, 245),
            "border": QColor(90, 90, 100),
            "text": QColor(245, 245, 248),
            "button": QColor(48, 48, 54),
            "hover": QColor(65, 65, 72),
            "accent": QColor(130, 210, 255),
        },

        "Graphite": {
            "background": QColor(38, 39, 43, 245),
            "border": QColor(105, 105, 110),
            "text": QColor(245, 245, 245),
            "button": QColor(55, 56, 61),
            "hover": QColor(72, 73, 79),
            "accent": QColor(180, 210, 255),
        },

        "Espresso": {
            "background": QColor(48, 38, 34, 245),
            "border": QColor(115, 88, 75),
            "text": QColor(245, 235, 225),
            "button": QColor(70, 53, 46),
            "hover": QColor(88, 67, 57),
            "accent": QColor(255, 190, 120),
        },

        "Slate": {
            "background": QColor(31, 40, 46, 245),
            "border": QColor(80, 105, 115),
            "text": QColor(235, 242, 245),
            "button": QColor(46, 58, 65),
            "hover": QColor(61, 76, 84),
            "accent": QColor(110, 220, 255),
        },

        "Midnight": {
            "background": QColor(27, 30, 43, 245),
            "border": QColor(72, 79, 105),
            "text": QColor(238, 240, 250),
            "button": QColor(43, 47, 63),
            "hover": QColor(59, 64, 84),
            "accent": QColor(145, 165, 255),
        },

        "Carbon": {
            "background": QColor(24, 24, 24, 245),
            "border": QColor(75, 75, 75),
            "text": QColor(240, 240, 240),
            "button": QColor(42, 42, 42),
            "hover": QColor(58, 58, 58),
            "accent": QColor(210, 210, 210),
        },
    }


    # ========================================================
    # INIT
    # ========================================================

    def __init__(self):

        super().__init__()

        self.setWindowTitle("GLOX Quick Apps")

        self.setFixedSize(300, 105)

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.dragging = False
        self.drag_offset = QPoint()

        self.config = self.load_config()

        self.theme = self.config.get(
            "theme",
            "Obsidian"
        )

        self.opacity_value = self.config.get(
            "opacity",
            100
        )

        self.setWindowOpacity(
            self.opacity_value / 100
        )

        self.slot_rects = []

        self.setup_position()

    # ========================================================
    # CONFIG LOAD
    # ========================================================

    def load_config(self):

        if not os.path.exists(CONFIG_FILE):

            self.save_config(DEFAULT_CONFIG)

            return json.loads(
                json.dumps(DEFAULT_CONFIG)
            )

        try:

            with open(
                CONFIG_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            # Make sure exactly 3 slots exist
            slots = data.get("slots", [])

            while len(slots) < 3:

                slots.append({
                    "name": f"App {len(slots) + 1}",
                    "target": ""
                })

            data["slots"] = slots[:3]

            return data

        except Exception:

            return json.loads(
                json.dumps(DEFAULT_CONFIG)
            )

    # ========================================================
    # CONFIG SAVE
    # ========================================================

    def save_config(self, data=None):

        if data is None:
            data = self.config

        try:

            with open(
                CONFIG_FILE,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4
                )

        except Exception as e:

            print(
                "Could not save config:",
                e
            )

    # ========================================================
    # POSITION
    # ========================================================

    def setup_position(self):

        screen = QApplication.primaryScreen()

        if screen:

            geometry = screen.availableGeometry()

            self.move(
                geometry.right()
                - self.width()
                - 35,

                geometry.bottom()
                - self.height()
                - 35
            )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_widget(self):

        """
        Reload configuration from disk and redraw.

        This is intentionally done without closing
        or recreating the widget.
        """

        current_pos = self.pos()

        self.config = self.load_config()

        self.theme = self.config.get(
            "theme",
            "Obsidian"
        )

        self.opacity_value = self.config.get(
            "opacity",
            100
        )

        self.setWindowOpacity(
            self.opacity_value / 100
        )

        self.move(current_pos)

        self.update()

    # ========================================================
    # LAUNCH TARGET
    # ========================================================

    def launch_target(self, target):

        if not target:
            return

        target = target.strip()

        try:

            # Website
            if (
                target.startswith("http://")
                or target.startswith("https://")
            ):

                webbrowser.open(target)

                return

            # Windows shell paths
            if os.path.exists(target):

                os.startfile(target)

                return

            # Try as a shell command / executable
            subprocess.Popen(
                target,
                shell=True
            )

        except Exception as e:

            QMessageBox.warning(
                self,
                "GLOX Bar",
                f"Could not open:\n\n{target}\n\n{e}"
            )

    # ========================================================
    # MOUSE PRESS
    # ========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:

            self.show_context_menu(
                event.globalPosition().toPoint()
            )

            return

        if event.button() == Qt.LeftButton:

            pos = event.position().toPoint()

            # Check quick app buttons
            for index, rect in enumerate(
                self.slot_rects
            ):

                if rect.contains(pos):

                    target = self.config["slots"][index][
                        "target"
                    ]

                    if target:

                        self.launch_target(
                            target
                        )

                    return

            # Otherwise drag
            self.dragging = True

            self.drag_offset = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    # ========================================================
    # MOUSE MOVE
    # ========================================================

    def mouseMoveEvent(self, event):

        if (
            self.dragging
            and event.buttons() & Qt.LeftButton
        ):

            self.move(
                event.globalPosition().toPoint()
                - self.drag_offset
            )

            event.accept()

    # ========================================================
    # MOUSE RELEASE
    # ========================================================

    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = False

            event.accept()

    # ========================================================
    # CONTEXT MENU
    # ========================================================

    def show_context_menu(self, position):

        menu = QMenu(self)

        menu.setStyleSheet("""
            QMenu {
                background: #252525;
                color: white;
                border: 1px solid #444444;
                padding: 5px;
                border-radius: 8px;
            }

            QMenu::item {
                padding: 7px 30px 7px 12px;
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
        # Manage
        # ----------------------------------------------------

        manage_action = menu.addAction(
            "Manage Apps"
        )

        manage_action.triggered.connect(
            self.open_manager
        )

        # ----------------------------------------------------
        # REFRESH
        # ----------------------------------------------------

        refresh_action = menu.addAction(
            "Refresh"
        )

        refresh_action.triggered.connect(
            self.refresh_widget
        )

        menu.addSeparator()

        # ----------------------------------------------------
        # THEME
        # ----------------------------------------------------

        theme_menu = menu.addMenu(
            "Theme"
        )

        for name in self.THEMES:

            action = theme_menu.addAction(
                name
            )

            action.setCheckable(True)

            action.setChecked(
                name == self.theme
            )

            action.triggered.connect(
                lambda checked=False,
                n=name:
                self.change_theme(n)
            )

        # ----------------------------------------------------
        # OPACITY
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

            action.setCheckable(True)

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
        # EXIT
        # ----------------------------------------------------

        exit_action = menu.addAction(
            "Exit"
        )

        exit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(position)

    # ========================================================
    # THEME
    # ========================================================

    def change_theme(self, name):

        self.theme = name

        self.config["theme"] = name

        self.save_config()

        self.update()

    # ========================================================
    # OPACITY
    # ========================================================

    def change_opacity(self, value):

        self.opacity_value = value

        self.config["opacity"] = value

        self.setWindowOpacity(
            value / 100
        )

        self.save_config()

    # ========================================================
    # PAINT
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        theme = self.THEMES.get(
            self.theme,
            self.THEMES["Obsidian"]
        )

        background = theme["background"]
        border = theme["border"]
        text = theme["text"]
        button = theme["button"]
        accent = theme["accent"]

        # ----------------------------------------------------
        # Main background
        # ----------------------------------------------------

        painter.setPen(
            QPen(
                border,
                1
            )
        )

        painter.setBrush(
            background
        )

        painter.drawRoundedRect(
            1,
            1,
            self.width() - 2,
            self.height() - 2,
            18,
            18
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        painter.setPen(text)

        painter.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold
            )
        )

        painter.drawText(
            15,
            22,
            "GLOX"
        )

        painter.setPen(
            QColor(
                text.red(),
                text.green(),
                text.blue(),
                150
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                8
            )
        )

        painter.drawText(
            53,
            22,
            "QUICK APPS"
        )

        # Accent line
        painter.setPen(
            QPen(
                accent,
                1
            )
        )

        painter.drawLine(
            15,
            29,
            285,
            29
        )

        # ----------------------------------------------------
        # Slots
        # ----------------------------------------------------

        self.slot_rects = []

        slots = self.config.get(
            "slots",
            []
        )

        for i in range(3):

            x = 12 + i * 92
            y = 39
            width = 84
            height = 50

            rect = self.rect().adjusted(
                x,
                y,
                -(self.width() - x - width),
                -(self.height() - y - height)
            )

            self.slot_rects.append(rect)

            painter.setPen(
                QPen(
                    border,
                    1
                )
            )

            painter.setBrush(
                button
            )

            painter.drawRoundedRect(
                rect,
                11,
                11
            )

            slot = (
                slots[i]
                if i < len(slots)
                else {}
            )

            name = slot.get(
                "name",
                f"App {i + 1}"
            )

            target = slot.get(
                "target",
                ""
            )

            if not target:

                name_color = QColor(
                    text.red(),
                    text.green(),
                    text.blue(),
                    110
                )

            else:

                name_color = text

            painter.setPen(
                name_color
            )

            painter.setFont(
                QFont(
                    "Segoe UI",
                    8,
                    QFont.Weight.Bold
                )
            )

            painter.drawText(
                rect.adjusted(
                    5,
                    5,
                    -5,
                    -5
                ),
                Qt.AlignCenter,
                name[:14]
            )

        painter.end()

    # ========================================================
    # MANAGER
    # ========================================================

    def open_manager(self):

        dialog = ManageDialog(
            self
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:

            # IMPORTANT:
            # Manager saves to disk, then immediately
            # reloads the visible widget.

            self.refresh_widget()


# ============================================================
# MANAGE DIALOG
# ============================================================

class ManageDialog(QDialog):

    def __init__(self, parent):

        super().__init__(parent)

        self.parent_bar = parent

        self.setWindowTitle(
            "GLOX Quick Apps"
        )

        self.setFixedSize(
            500,
            350
        )

        self.setStyleSheet("""
            QDialog {
                background: #252525;
                color: white;
            }

            QLabel {
                color: #eeeeee;
            }

            QLineEdit {
                background: #303030;
                color: white;
                border: 1px solid #505050;
                border-radius: 7px;
                padding: 7px;
            }

            QPushButton {
                background: #383838;
                color: white;
                border: 1px solid #555555;
                border-radius: 7px;
                padding: 7px 12px;
            }

            QPushButton:hover {
                background: #484848;
            }
        """)

        self.name_inputs = []
        self.target_inputs = []

        layout = QVBoxLayout(self)

        title = QLabel(
            "GLOX QUICK APPS"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Weight.Bold
            )
        )

        layout.addWidget(title)

        # ----------------------------------------------------
        # Three slots
        # ----------------------------------------------------

        for i in range(3):

            slot = self.parent_bar.config[
                "slots"
            ][i]

            label = QLabel(
                f"Slot {i + 1}"
            )

            label.setFont(
                QFont(
                    "Segoe UI",
                    9,
                    QFont.Weight.Bold
                )
            )

            layout.addWidget(label)

            name_row = QHBoxLayout()

            name_input = QLineEdit()

            name_input.setText(
                slot.get(
                    "name",
                    f"App {i + 1}"
                )
            )

            name_input.setPlaceholderText(
                "Name"
            )

            name_row.addWidget(
                name_input
            )

            layout.addLayout(
                name_row
            )

            target_row = QHBoxLayout()

            target_input = QLineEdit()

            target_input.setText(
                slot.get(
                    "target",
                    ""
                )
            )

            target_input.setPlaceholderText(
                "Website, app, file or folder"
            )

            target_row.addWidget(
                target_input
            )

            browse_button = QPushButton(
                "Select"
            )

            browse_button.clicked.connect(
                lambda checked=False,
                inp=target_input:
                self.select_target(inp)
            )

            target_row.addWidget(
                browse_button
            )

            layout.addLayout(
                target_row
            )

            self.name_inputs.append(
                name_input
            )

            self.target_inputs.append(
                target_input
            )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        layout.addStretch()

        button_row = QHBoxLayout()

        save_button = QPushButton(
            "SAVE"
        )

        save_button.clicked.connect(
            self.save
        )

        cancel_button = QPushButton(
            "CANCEL"
        )

        cancel_button.clicked.connect(
            self.reject
        )

        button_row.addStretch()

        button_row.addWidget(
            cancel_button
        )

        button_row.addWidget(
            save_button
        )

        layout.addLayout(
            button_row
        )

    # ========================================================
    # SELECT
    # ========================================================

    def select_target(self, input_box):

        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select App or File",
            "",
            "All Files (*.*)"
        )

        if path:

            input_box.setText(
                path
            )

            return

        # If user cancels file picker, offer folder picker
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder"
        )

        if folder:

            input_box.setText(
                folder
            )

    # ========================================================
    # SAVE
    # ========================================================

    def save(self):

        slots = []

        for i in range(3):

            name = self.name_inputs[i].text().strip()

            target = self.target_inputs[i].text().strip()

            if not name:

                name = f"App {i + 1}"

            slots.append({
                "name": name,
                "target": target
            })

        self.parent_bar.config[
            "slots"
        ] = slots

        self.parent_bar.save_config()

        self.accept()


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

    widget = GloxBar()

    widget.show()

    sys.exit(
        app.exec()
    )