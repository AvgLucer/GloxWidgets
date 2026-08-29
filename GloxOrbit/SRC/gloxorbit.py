# ============================================================
# GLOX ORBIT
# Animated desktop application orbit
# GLOX INDUSTRIES
# ============================================================

import sys
import os
import json
import math
import subprocess
import webbrowser

from PySide6.QtCore import (
    Qt,
    QTimer,
    QPointF,
)
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
    QFont,
)
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMenu,
    QInputDialog,
)


# ============================================================
# CONFIG
# ============================================================

CONFIG_FILE = os.path.join(
    os.path.expanduser("~"),
    ".glox_orbit.json"
)


# ============================================================
# GLOX ORBIT
# ============================================================

class GloxOrbit(QWidget):

    WIDTH = 430
    HEIGHT = 430

    # --------------------------------------------------------
    # THEMES
    # --------------------------------------------------------

    THEMES = {

        "Glox Brown": {
            "background": QColor(38, 35, 32, 225),
            "border": QColor(220, 200, 175, 80),
            "accent": QColor(218, 177, 112),
            "accent2": QColor(160, 125, 85),
            "text": QColor(243, 238, 229),
            "muted": QColor(165, 158, 148),
        },

        "Obsidian": {
            "background": QColor(24, 25, 28, 230),
            "border": QColor(150, 155, 165, 70),
            "accent": QColor(145, 190, 255),
            "accent2": QColor(90, 125, 180),
            "text": QColor(240, 242, 246),
            "muted": QColor(150, 154, 162),
        },

        "Espresso": {
            "background": QColor(48, 37, 32, 230),
            "border": QColor(225, 180, 135, 75),
            "accent": QColor(235, 184, 122),
            "accent2": QColor(155, 105, 70),
            "text": QColor(246, 235, 224),
            "muted": QColor(165, 145, 132),
        },

        "Midnight": {
            "background": QColor(25, 28, 42, 232),
            "border": QColor(120, 145, 220, 75),
            "accent": QColor(135, 160, 255),
            "accent2": QColor(80, 100, 180),
            "text": QColor(238, 241, 255),
            "muted": QColor(145, 150, 175),
        },

        "Pearl": {
            "background": QColor(220, 222, 225, 190),
            "border": QColor(255, 255, 255, 180),
            "accent": QColor(75, 90, 105),
            "accent2": QColor(125, 135, 145),
            "text": QColor(35, 38, 42),
            "muted": QColor(90, 95, 102),
        },
    }

    # --------------------------------------------------------
    # DEFAULT APPLICATIONS
    # --------------------------------------------------------

    DEFAULT_NODES = [

        {
            "name": "Browser",
            "type": "url",
            "target": "https://www.google.com",
        },

        {
            "name": "VS Code",
            "type": "exe",
            "target": "code",
        },

        {
            "name": "Files",
            "type": "folder",
            "target": os.path.expanduser("~"),
        },

        {
            "name": "Terminal",
            "type": "command",
            "target": "cmd.exe",
        },

        {
            "name": "GitHub",
            "type": "url",
            "target": "https://github.com",
        },

        {
            "name": "YouTube",
            "type": "url",
            "target": "https://youtube.com",
        },

    ]

    # ========================================================
    # INIT
    # ========================================================

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "GLOX Orbit"
        )

        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        self.theme_name = "Glox Brown"

        self.nodes = []

        self.rotation = 0.0

        self.rotation_speed = 0.25

        self.hover_node = -1

        self.dragging = False

        self.drag_offset = QPointF()

        self.pulse = 0.0

        self.pulse_direction = 1

        self.load_config()

        # ----------------------------------------------------
        # ANIMATION
        # ----------------------------------------------------

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(16)

        self.setup_position()

    # ========================================================
    # POSITION
    # ========================================================

    def setup_position(self):

        screen = QApplication.primaryScreen()

        if screen:

            geometry = screen.availableGeometry()

            self.move(
                geometry.center().x()
                - self.WIDTH // 2,

                geometry.center().y()
                - self.HEIGHT // 2
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

                    self.theme_name = data.get(
                        "theme",
                        "Glox Brown"
                    )

                    self.rotation_speed = data.get(
                        "speed",
                        0.25
                    )

                    self.nodes = data.get(
                        "nodes",
                        self.DEFAULT_NODES.copy()
                    )

            else:

                self.nodes = (
                    self.DEFAULT_NODES.copy()
                )

        except Exception:

            self.nodes = (
                self.DEFAULT_NODES.copy()
            )

    # ========================================================
    # SAVE
    # ========================================================

    def save_config(self):

        try:

            data = {

                "theme":
                    self.theme_name,

                "speed":
                    self.rotation_speed,

                "nodes":
                    self.nodes,

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
    # ANIMATION
    # ========================================================

    def animate(self):

        self.rotation += (
            self.rotation_speed
        )

        self.pulse += (
            0.025 * self.pulse_direction
        )

        if self.pulse >= 1:
            self.pulse_direction = -1

        if self.pulse <= 0:
            self.pulse_direction = 1

        self.update()

    # ========================================================
    # CENTER
    # ========================================================

    def center_point(self):

        return QPointF(
            self.WIDTH / 2,
            self.HEIGHT / 2
        )

    # ========================================================
    # NODE POSITIONS
    # ========================================================

    def node_position(self, index):

        count = len(self.nodes)

        if count == 0:
            return self.center_point()

        center = self.center_point()

        radius = 145

        angle_step = (
            360 / count
        )

        angle = (
            self.rotation
            + index * angle_step
            - 90
        )

        radians = math.radians(
            angle
        )

        x = (
            center.x()
            + math.cos(radians)
            * radius
        )

        y = (
            center.y()
            + math.sin(radians)
            * radius
        )

        return QPointF(
            x,
            y
        )

    # ========================================================
    # LAUNCH
    # ========================================================

    def launch_node(self, node):

        try:

            node_type = node.get(
                "type",
                "url"
            )

            target = node.get(
                "target",
                ""
            )

            if node_type == "url":

                webbrowser.open(
                    target
                )

            elif node_type == "folder":

                os.startfile(
                    target
                )

            elif node_type == "exe":

                subprocess.Popen(
                    target,
                    shell=True
                )

            elif node_type == "command":

                subprocess.Popen(
                    target,
                    shell=True
                )

        except Exception:

            pass

    # ========================================================
    # PAINT
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        theme = self.THEMES[
            self.theme_name
        ]

        center = self.center_point()

        # ----------------------------------------------------
        # OUTER SHADOW
        # ----------------------------------------------------

        painter.setPen(
            Qt.NoPen
        )

        painter.setBrush(
            QColor(
                0,
                0,
                0,
                110
            )
        )

        painter.drawRoundedRect(
            8,
            8,
            self.WIDTH - 16,
            self.HEIGHT - 16,
            30,
            30
        )

        # ----------------------------------------------------
        # MAIN GLASS
        # ----------------------------------------------------

        painter.setBrush(
            theme["background"]
        )

        painter.setPen(
            QPen(
                theme["border"],
                1
            )
        )

        painter.drawRoundedRect(
            4,
            4,
            self.WIDTH - 8,
            self.HEIGHT - 8,
            28,
            28
        )

        # ----------------------------------------------------
        # ORBIT GLOW
        # ----------------------------------------------------

        for radius, alpha in [
            (150, 15),
            (147, 25),
            (144, 40),
        ]:

            pen = QPen(
                theme["accent"]
            )

            pen.setWidth(1)
            pen.setColor(
                QColor(
                    theme["accent"].red(),
                    theme["accent"].green(),
                    theme["accent"].blue(),
                    alpha
                )
            )

            painter.setPen(pen)

            painter.setBrush(
                Qt.NoBrush
            )

            painter.drawEllipse(
                center,
                radius,
                radius
            )

        # ----------------------------------------------------
        # ORBIT TRACK
        # ----------------------------------------------------

        pen = QPen(
            theme["accent"]
        )

        pen.setWidth(1)

        pen.setColor(
            QColor(
                theme["accent"].red(),
                theme["accent"].green(),
                theme["accent"].blue(),
                35
            )
        )

        painter.setPen(pen)

        painter.drawEllipse(
            center,
            145,
            145
        )

        # ----------------------------------------------------
        # CONNECTION LINES
        # ----------------------------------------------------

        for index in range(
            len(self.nodes)
        ):

            position = self.node_position(
                index
            )

            pen = QPen(
                theme["accent"]
            )

            pen.setWidth(1)

            alpha = (
                22
                if index != self.hover_node
                else 70
            )

            pen.setColor(
                QColor(
                    theme["accent"].red(),
                    theme["accent"].green(),
                    theme["accent"].blue(),
                    alpha
                )
            )

            painter.setPen(
                pen
            )

            painter.drawLine(
                center,
                position
            )

        # ----------------------------------------------------
        # CENTER GLOW
        # ----------------------------------------------------

        glow_radius = (
            47
            + self.pulse * 4
        )

        for radius, alpha in [
            (glow_radius + 12, 12),
            (glow_radius + 7, 22),
            (glow_radius + 3, 35),
        ]:

            painter.setBrush(
                QColor(
                    theme["accent"].red(),
                    theme["accent"].green(),
                    theme["accent"].blue(),
                    alpha
                )
            )

            painter.setPen(
                Qt.NoPen
            )

            painter.drawEllipse(
                center,
                radius,
                radius
            )

        # ----------------------------------------------------
        # CENTER CORE
        # ----------------------------------------------------

        painter.setBrush(
            QColor(
                theme["background"].red() + 8,
                theme["background"].green() + 8,
                theme["background"].blue() + 8,
                245
            )
        )

        painter.setPen(
            QPen(
                theme["accent"],
                1
            )
        )

        painter.drawEllipse(
            center,
            42,
            42
        )

        # ----------------------------------------------------
        # CENTER RING
        # ----------------------------------------------------

        painter.setBrush(
            Qt.NoBrush
        )

        painter.setPen(
            QPen(
                theme["accent"],
                1
            )
        )

        painter.drawEllipse(
            center,
            35,
            35
        )

        # ----------------------------------------------------
        # GLOX TEXT
        # ----------------------------------------------------

        painter.setPen(
            theme["text"]
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Weight.Bold
            )
        )

        rect = self.rect()

        painter.drawText(
            rect,
            Qt.AlignCenter,
            "GLOX"
        )

        # ----------------------------------------------------
        # ORBIT TEXT
        # ----------------------------------------------------

        painter.setFont(
            QFont(
                "Segoe UI",
                6,
                QFont.Weight.Medium
            )
        )

        orbit_rect = rect.adjusted(
            0,
            43,
            0,
            0
        )

        painter.setPen(
            theme["muted"]
        )

        painter.drawText(
            orbit_rect,
            Qt.AlignCenter,
            "ORBIT"
        )

        # ----------------------------------------------------
        # NODES
        # ----------------------------------------------------

        for index, node in enumerate(
            self.nodes
        ):

            position = self.node_position(
                index
            )

            hovered = (
                index == self.hover_node
            )

            node_radius = (
                29
                if hovered
                else 25
            )

            # Node glow

            if hovered:

                painter.setBrush(
                    QColor(
                        theme["accent"].red(),
                        theme["accent"].green(),
                        theme["accent"].blue(),
                        30
                    )
                )

                painter.setPen(
                    Qt.NoPen
                )

                painter.drawEllipse(
                    position,
                    39,
                    39
                )

            # Node body

            painter.setBrush(
                QColor(
                    theme["background"].red() + 8,
                    theme["background"].green() + 8,
                    theme["background"].blue() + 8,
                    245
                )
            )

            painter.setPen(
                QPen(
                    theme["accent"]
                    if hovered
                    else theme["border"],
                    1
                )
            )

            painter.drawEllipse(
                position,
                node_radius,
                node_radius
            )

            # Node dot

            painter.setBrush(
                theme["accent"]
            )

            painter.setPen(
                Qt.NoPen
            )

            painter.drawEllipse(
                position,
                5,
                5
            )

            # Name

            name = node.get(
                "name",
                "APP"
            )

            painter.setFont(
                QFont(
                    "Segoe UI",
                    7,
                    QFont.Weight.Medium
                )
            )

            painter.setPen(
                theme["text"]
            )

            label_rect = (
                int(position.x() - 48),
                int(position.y() + 34),
                96,
                20
            )

            painter.drawText(
                *label_rect,
                Qt.AlignCenter,
                name.upper()
            )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        painter.setFont(
            QFont(
                "Segoe UI",
                7,
                QFont.Weight.Bold
            )
        )

        painter.setPen(
            theme["muted"]
        )

        painter.drawText(
            22,
            27,
            "GLOX  ORBIT"
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                6
            )
        )

        painter.drawText(
            22,
            40,
            "YOUR DESKTOP. IN MOTION."
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        painter.setPen(
            QColor(
                theme["muted"]
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                6
            )
        )

        painter.drawText(
            20,
            self.HEIGHT - 17,
            "LEFT CLICK  •  LAUNCH"
        )

        painter.drawText(
            self.WIDTH - 110,
            self.HEIGHT - 17,
            "RIGHT CLICK  •  OPTIONS"
        )

    # ========================================================
    # FIND NODE
    # ========================================================

    def node_at(self, position):

        for index in range(
            len(self.nodes)
        ):

            node_position = (
                self.node_position(index)
            )

            distance = math.sqrt(
                (
                    position.x()
                    - node_position.x()
                ) ** 2
                +
                (
                    position.y()
                    - node_position.y()
                ) ** 2
            )

            if distance <= 32:

                return index

        return -1

    # ========================================================
    # MOUSE MOVE
    # ========================================================

    def mouseMoveEvent(self, event):

        position = (
            event.position()
        )

        new_hover = self.node_at(
            position
        )

        if new_hover != self.hover_node:

            self.hover_node = new_hover

            if new_hover >= 0:

                self.setCursor(
                    Qt.PointingHandCursor
                )

            else:

                self.setCursor(
                    Qt.ArrowCursor
                )

            self.update()

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
    # MOUSE PRESS
    # ========================================================

    def mousePressEvent(self, event):

        # ----------------------------------------------------
        # RIGHT CLICK
        # ----------------------------------------------------

        if event.button() == Qt.RightButton:

            self.show_menu(
                event.globalPosition()
                .toPoint()
            )

            return

        # ----------------------------------------------------
        # LEFT CLICK
        # ----------------------------------------------------

        if event.button() == Qt.LeftButton:

            index = self.node_at(
                event.position()
            )

            if index >= 0:

                self.launch_node(
                    self.nodes[index]
                )

                return

            self.dragging = True

            self.drag_offset = (
                event.globalPosition()
                - self.frameGeometry()
                .topLeft()
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
    # MENU
    # ========================================================

    def show_menu(self, position):

        menu = QMenu(
            self
        )

        menu.setStyleSheet(
            """
            QMenu {
                background: #292825;
                color: #F3EEE5;
                border: 1px solid #4B4842;
                padding: 5px;
            }

            QMenu::item {
                padding: 7px 25px 7px 12px;
                border-radius: 5px;
            }

            QMenu::item:selected {
                background: #3D3A35;
            }

            QMenu::separator {
                height: 1px;
                background: #4A4741;
                margin: 5px;
            }
            """
        )

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

            action.setCheckable(
                True
            )

            action.setChecked(
                name == self.theme_name
            )

            action.triggered.connect(
                lambda checked=False,
                n=name:
                self.change_theme(n)
            )

        # ----------------------------------------------------
        # SPEED
        # ----------------------------------------------------

        speed_menu = menu.addMenu(
            "Orbit Speed"
        )

        speeds = {
            "Slow": 0.08,
            "Normal": 0.25,
            "Fast": 0.55,
            "Very Fast": 0.9,
        }

        for name, value in speeds.items():

            action = speed_menu.addAction(
                name
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                abs(
                    self.rotation_speed
                    - value
                ) < 0.01
            )

            action.triggered.connect(
                lambda checked=False,
                v=value:
                self.change_speed(v)
            )

        # ----------------------------------------------------
        # ADD NODE
        # ----------------------------------------------------

        add_action = menu.addAction(
            "Add Orbit"
        )

        add_action.triggered.connect(
            self.add_node
        )

        # ----------------------------------------------------
        # REMOVE NODE
        # ----------------------------------------------------

        remove_menu = menu.addMenu(
            "Remove Orbit"
        )

        for index, node in enumerate(
            self.nodes
        ):

            action = remove_menu.addAction(
                node.get(
                    "name",
                    f"Node {index + 1}"
                )
            )

            action.triggered.connect(
                lambda checked=False,
                i=index:
                self.remove_node(i)
            )

        menu.addSeparator()

        # ----------------------------------------------------
        # RESET
        # ----------------------------------------------------

        reset_action = menu.addAction(
            "Reset Orbits"
        )

        reset_action.triggered.connect(
            self.reset_nodes
        )

        menu.addSeparator()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        exit_action = menu.addAction(
            "Exit GLOX Orbit"
        )

        exit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(
            position
        )

    # ========================================================
    # ADD NODE
    # ========================================================

    def add_node(self):

        name, ok = QInputDialog.getText(
            self,
            "GLOX Orbit",
            "Orbit name:"
        )

        if not ok or not name.strip():

            return

        target, ok = QInputDialog.getText(
            self,
            "GLOX Orbit",
            "URL / application / folder:"
        )

        if not ok or not target.strip():

            return

        # Automatically detect URL

        if (
            target.startswith(
                "http://"
            )
            or target.startswith(
                "https://"
            )
        ):

            node_type = "url"

        elif os.path.isdir(target):

            node_type = "folder"

        else:

            node_type = "exe"

        self.nodes.append(
            {
                "name":
                    name.strip(),

                "type":
                    node_type,

                "target":
                    target.strip(),
            }
        )

        self.save_config()

        self.update()

    # ========================================================
    # REMOVE NODE
    # ========================================================

    def remove_node(self, index):

        if (
            0 <= index
            < len(self.nodes)
        ):

            self.nodes.pop(
                index
            )

            self.save_config()

            self.hover_node = -1

            self.update()

    # ========================================================
    # RESET
    # ========================================================

    def reset_nodes(self):

        self.nodes = (
            self.DEFAULT_NODES.copy()
        )

        self.save_config()

        self.update()

    # ========================================================
    # THEME
    # ========================================================

    def change_theme(self, name):

        self.theme_name = name

        self.save_config()

        self.update()

    # ========================================================
    # SPEED
    # ========================================================

    def change_speed(self, speed):

        self.rotation_speed = speed

        self.save_config()

    # ========================================================
    # CLOSE
    # ========================================================

    def closeEvent(self, event):

        self.save_config()

        event.accept()


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "GLOX Orbit"
    )

    app.setStyle(
        "Fusion"
    )

    widget = GloxOrbit()

    widget.show()

    sys.exit(
        app.exec()
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()