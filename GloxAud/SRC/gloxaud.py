import sys
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QColor, QPainter, QPen, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMenu,
)

from pycaw.pycaw import AudioUtilities


# =============================================================
# AUDIO CONTROLLER
# =============================================================

class AudioController:

    def __init__(self):

        # -----------------------------------------------------
        # DEFAULT SPEAKER
        # -----------------------------------------------------

        speaker = AudioUtilities.GetSpeakers()
        self.output = speaker.EndpointVolume

        # -----------------------------------------------------
        # MICROPHONE
        # -----------------------------------------------------

        self.mic = None

        devices = AudioUtilities.GetAllDevices()

        for device in devices:

            try:
                name = device.FriendlyName.lower()

                if (
                    "microphone" in name
                    or "mic" in name
                ):
                    self.mic = device.EndpointVolume
                    break

            except Exception:
                continue

    # =========================================================
    # MIC
    # =========================================================

    def get_mic_mute(self):

        if self.mic is None:
            return False

        return bool(
            self.mic.GetMute()
        )

    def set_mic_mute(self, state):

        if self.mic is not None:

            self.mic.SetMute(
                1 if state else 0,
                None
            )


# =============================================================
# GLOX AUD
# =============================================================

class GloxAud(QWidget):

    WIDTH = 330
    HEIGHT = 250

    # =========================================================
    # THEMES
    # =========================================================

    THEMES = {

        "Obsidian":
            QColor(22, 23, 25, 255),

        "Graphite":
            QColor(34, 35, 38, 255),

        "Charcoal":
            QColor(43, 43, 43, 255),

        "Espresso":
            QColor(49, 39, 34, 255),

        "Slate":
            QColor(35, 42, 48, 255),

        "Midnight":
            QColor(25, 29, 40, 255),
    }

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self):

        super().__init__()

        self.audio = AudioController()

        self.current_theme = "Obsidian"

        self.opacity_value = 100

        self.dragging = False
        self.drag_offset = QPointF()

        self.mic_killed = (
            self.audio.get_mic_mute()
        )

        self.setWindowTitle(
            "GloxAud"
        )

        self.setFixedSize(
            self.WIDTH,
            self.HEIGHT
        )

        # -----------------------------------------------------
        # WINDOW
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
        # UI
        # -----------------------------------------------------

        self.build_ui()

        self.update_opacity()

    # =========================================================
    # UI
    # =========================================================

    def build_ui(self):

        self.main_layout = QVBoxLayout(
            self
        )

        self.main_layout.setContentsMargins(
            20,
            18,
            20,
            20
        )

        self.main_layout.setSpacing(
            12
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = QHBoxLayout()

        title = QLabel(
            "GLOX"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                16,
                QFont.Weight.Bold
            )
        )

        title.setStyleSheet(
            "color: white;"
        )

        subtitle = QLabel(
            "AUD"
        )

        subtitle.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Weight.Bold
            )
        )

        subtitle.setStyleSheet(
            "color: rgba(255,255,255,150);"
        )

        header.addWidget(
            title
        )

        header.addWidget(
            subtitle
        )

        header.addStretch()

        self.main_layout.addLayout(
            header
        )

        # -----------------------------------------------------
        # DESCRIPTION
        # -----------------------------------------------------

        description = QLabel(
            "Hardware microphone control"
        )

        description.setFont(
            QFont(
                "Segoe UI",
                9
            )
        )

        description.setStyleSheet(
            "color: rgba(255,255,255,110);"
        )

        self.main_layout.addWidget(
            description
        )

        # -----------------------------------------------------
        # MIC CARD
        # -----------------------------------------------------

        mic_card = QFrame()

        mic_card.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,15);
                border: 1px solid rgba(255,255,255,25);
                border-radius: 16px;
            }
        """)

        mic_layout = QVBoxLayout(
            mic_card
        )

        mic_layout.setContentsMargins(
            15,
            14,
            15,
            14
        )

        # -----------------------------------------------------
        # MIC HEADER
        # -----------------------------------------------------

        mic_header = QHBoxLayout()

        mic_title = QLabel(
            "MICROPHONE"
        )

        mic_title.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Weight.Bold
            )
        )

        mic_title.setStyleSheet(
            "color: rgba(255,255,255,190);"
        )

        self.mic_status = QLabel()

        self.mic_status.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold
            )
        )

        mic_header.addWidget(
            mic_title
        )

        mic_header.addStretch()

        mic_header.addWidget(
            self.mic_status
        )

        mic_layout.addLayout(
            mic_header
        )

        # -----------------------------------------------------
        # KILL SWITCH
        # -----------------------------------------------------

        self.kill_button = QPushButton()

        self.kill_button.setFixedHeight(
            52
        )

        self.kill_button.clicked.connect(
            self.toggle_mic
        )

        mic_layout.addWidget(
            self.kill_button
        )

        self.main_layout.addWidget(
            mic_card
        )

        self.update_mic_button()

        self.main_layout.addStretch()

    # =========================================================
    # MIC SWITCH
    # =========================================================

    def toggle_mic(self):

        self.mic_killed = (
            not self.mic_killed
        )

        self.audio.set_mic_mute(
            self.mic_killed
        )

        self.update_mic_button()

    # =========================================================
    # MIC UI
    # =========================================================

    def update_mic_button(self):

        if self.mic_killed:

            self.mic_status.setText(
                "KILLED"
            )

            self.mic_status.setStyleSheet(
                "color: #ff7777;"
            )

            self.kill_button.setText(
                "MIC OFF"
            )

            self.kill_button.setStyleSheet("""
                QPushButton {
                    background: rgba(180,55,55,190);
                    color: white;
                    border: none;
                    border-radius: 11px;
                    font-family: "Segoe UI";
                    font-size: 11px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background: rgba(205,65,65,210);
                }

                QPushButton:pressed {
                    background: rgba(150,45,45,220);
                }
            """)

        else:

            self.mic_status.setText(
                "ACTIVE"
            )

            self.mic_status.setStyleSheet(
                "color: rgba(255,255,255,150);"
            )

            self.kill_button.setText(
                "MIC ON"
            )

            self.kill_button.setStyleSheet("""
                QPushButton {
                    background: rgba(255,255,255,22);
                    color: white;
                    border: 1px solid rgba(255,255,255,30);
                    border-radius: 11px;
                    font-family: "Segoe UI";
                    font-size: 11px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background: rgba(255,255,255,35);
                }

                QPushButton:pressed {
                    background: rgba(255,255,255,48);
                }
            """)

    # =========================================================
    # RIGHT CLICK MENU
    # =========================================================

    def contextMenuEvent(self, event):

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

        # -----------------------------------------------------
        # THEME
        # -----------------------------------------------------

        theme_menu = menu.addMenu(
            "Theme"
        )

        for theme_name in self.THEMES:

            action = theme_menu.addAction(
                theme_name
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                theme_name
                == self.current_theme
            )

            action.triggered.connect(
                lambda checked=False,
                name=theme_name:
                self.change_theme(name)
            )

        # -----------------------------------------------------
        # OPACITY
        # -----------------------------------------------------

        opacity_menu = menu.addMenu(
            "Opacity"
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

        # -----------------------------------------------------
        # EXIT
        # -----------------------------------------------------

        exit_action = menu.addAction(
            "Exit"
        )

        exit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(
            event.globalPos()
        )

    # =========================================================
    # CHANGE THEME
    # =========================================================

    def change_theme(
        self,
        theme_name
    ):

        self.current_theme = (
            theme_name
        )

        self.update()

    # =========================================================
    # OPACITY
    # =========================================================

    def change_opacity(
        self,
        value
    ):

        self.opacity_value = value

        self.update_opacity()

    def update_opacity(self):

        self.setWindowOpacity(
            self.opacity_value / 100
        )

    # =========================================================
    # PAINT
    # =========================================================

    def paintEvent(
        self,
        event
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        background = self.THEMES[
            self.current_theme
        ]

        painter.setBrush(
            background
        )

        painter.setPen(
            QPen(
                QColor(
                    255,
                    255,
                    255,
                    35
                ),
                1
            )
        )

        painter.drawRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            18,
            18
        )

    # =========================================================
    # DRAG WINDOW
    # =========================================================

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.drag_offset = (
                event.globalPosition()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(
        self,
        event
    ):

        if (
            self.dragging
            and event.buttons()
            & Qt.LeftButton
        ):

            self.move(
                (
                    event.globalPosition()
                    - self.drag_offset
                ).toPoint()
            )

            event.accept()

    def mouseReleaseEvent(
        self,
        event
    ):

        self.dragging = False

        event.accept()


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    app.setStyle(
        "Fusion"
    )

    widget = GloxAud()

    widget.show()

    sys.exit(
        app.exec()
    )