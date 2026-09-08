
# GloxWatcher.py
# =============================================================
# GLOX WATCHER — Timer + Stopwatch
# Premium floating glass widget
#
# Install:
# pip install PySide6
#
# Sound files must be in the same folder:
#
# nightrain.wav
# sunrise.wav
# groovy.wav
# intense.wav
# drama.wav
#
# Run:
# python GloxWatcher.py
# =============================================================

import sys
import time
import os

from PySide6.QtCore import Qt, QTimer, QPointF, QUrl
from PySide6.QtGui import QColor, QPainter, QPen, QFont
from PySide6.QtMultimedia import QSoundEffect

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMenu,
    QLineEdit,
)


# =============================================================
# GLOX WATCHER
# =============================================================

class GloxWatcher(QWidget):

    WIDTH = 384
    HEIGHT = 360

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

        "Crystal Cream":
            QColor(235, 231, 219, 255),

        "Glowy Sunshine":
            QColor(63, 58, 31, 255),

        "Aurora Night":
            QColor(27, 34, 48, 255),
    }

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self):

        super().__init__()

        self.current_theme = "Obsidian"
        self.opacity_value = 100

        self.dragging = False
        self.drag_offset = QPointF()

        # -----------------------------------------------------
        # TIMER
        # -----------------------------------------------------

        self.timer_running = False
        self.timer_remaining = 0
        self.timer_total = 0

        # -----------------------------------------------------
        # STOPWATCH
        # -----------------------------------------------------

        self.stopwatch_running = False
        self.stopwatch_elapsed = 0
        self.stopwatch_started_at = 0

        # -----------------------------------------------------
        # MODE
        # -----------------------------------------------------

        self.mode = "Timer"

        # -----------------------------------------------------
        # ALARM SOUND
        # -----------------------------------------------------

        self.alarm_sound = "Nightrain"

        self.sound_files = {

            "Nightrain":
                "nightrain.wav",

            "Sunrise":
                "sunrise.wav",

            "Groovy":
                "groovy.wav",

            "Intense":
                "intense.wav",

            "Drama":
                "drama.wav",
        }

        # -----------------------------------------------------
        # SOUND PLAYER
        # -----------------------------------------------------

        self.alarm_player = QSoundEffect(self)

        self.alarm_player.setVolume(1.0)

        # 10 total plays
        self.alarm_player.setLoopCount(10)

        # -----------------------------------------------------
        # WINDOW
        # -----------------------------------------------------

        self.setWindowTitle(
            "GloxWatcher"
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

        # -----------------------------------------------------
        # UPDATE TIMER
        # -----------------------------------------------------

        self.ui_timer = QTimer(self)

        self.ui_timer.timeout.connect(
            self.update_display
        )

        self.ui_timer.start(50)

        # -----------------------------------------------------
        # UI
        # -----------------------------------------------------

        self.build_ui()

        self.update_display()

        self.update_opacity()

        self.load_alarm_sound()

    # =========================================================
    # UI
    # =========================================================

    def build_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            22,
            18,
            22,
            22
        )

        self.main_layout.setSpacing(12)

        # =====================================================
        # HEADER
        # =====================================================

        header = QHBoxLayout()

        title = QLabel("GLOX")

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

        subtitle = QLabel("WATCHER")

        subtitle.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Weight.Bold
            )
        )

        subtitle.setStyleSheet(
            "color: rgba(255,255,255,145);"
        )

        header.addWidget(title)
        header.addWidget(subtitle)

        header.addStretch()

        self.main_layout.addLayout(
            header
        )

        # =====================================================
        # MODE SWITCH
        # =====================================================

        mode_container = QFrame()

        mode_container.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,12);
                border: 1px solid rgba(255,255,255,20);
                border-radius: 12px;
            }
        """)

        mode_layout = QHBoxLayout(
            mode_container
        )

        mode_layout.setContentsMargins(
            4,
            4,
            4,
            4
        )

        mode_layout.setSpacing(4)

        self.timer_mode_button = QPushButton(
            "TIMER"
        )

        self.stopwatch_mode_button = QPushButton(
            "STOPWATCH"
        )

        self.timer_mode_button.clicked.connect(
            lambda: self.change_mode("Timer")
        )

        self.stopwatch_mode_button.clicked.connect(
            lambda: self.change_mode("Stopwatch")
        )

        mode_layout.addWidget(
            self.timer_mode_button
        )

        mode_layout.addWidget(
            self.stopwatch_mode_button
        )

        self.main_layout.addWidget(
            mode_container
        )

        # =====================================================
        # DIGITAL DISPLAY
        # =====================================================

        display_card = QFrame()

        display_card.setStyleSheet("""
            QFrame {
                background: rgba(0,0,0,45);
                border: 1px solid rgba(255,255,255,25);
                border-radius: 18px;
            }
        """)

        display_layout = QVBoxLayout(
            display_card
        )

        display_layout.setContentsMargins(
            12,
            16,
            12,
            16
        )

        self.display = QLabel(
            "00:00:00"
        )

        self.display.setAlignment(
            Qt.AlignCenter
        )

        self.display.setFont(
            QFont(
                "Consolas",
                38,
                QFont.Weight.Bold
            )
        )

        self.display.setStyleSheet("""
            color: white;
            background: transparent;
            letter-spacing: 2px;
        """)

        display_layout.addWidget(
            self.display
        )

        self.status_label = QLabel(
            "READY"
        )

        self.status_label.setAlignment(
            Qt.AlignCenter
        )

        self.status_label.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold
            )
        )

        self.status_label.setStyleSheet(
            "color: rgba(255,255,255,100);"
        )

        display_layout.addWidget(
            self.status_label
        )

        self.main_layout.addWidget(
            display_card
        )

        # =====================================================
        # TIMER PRESETS
        # =====================================================

        self.presets_frame = QFrame()

        presets_layout = QHBoxLayout(
            self.presets_frame
        )

        presets_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        presets_layout.setSpacing(6)

        presets = [
            ("30s", 30),
            ("1m", 60),
            ("5m", 300),
            ("10m", 600),
            ("30m", 1800),
            ("1h", 3600),
            ("2h", 7200),
        ]

        for text, seconds in presets:

            button = QPushButton(
                text
            )

            button.setFixedHeight(
                28
            )

            button.clicked.connect(
                lambda checked=False,
                s=seconds:
                self.set_timer(s)
            )

            presets_layout.addWidget(
                button
            )

        self.main_layout.addWidget(
            self.presets_frame
        )

        # =====================================================
        # CUSTOM TIMER
        # =====================================================

        self.custom_frame = QFrame()

        custom_layout = QHBoxLayout(
            self.custom_frame
        )

        custom_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.custom_input = QLineEdit()

        self.custom_input.setPlaceholderText(
            "Custom seconds..."
        )

        self.custom_input.setFixedHeight(
            32
        )

        custom_button = QPushButton(
            "SET"
        )

        custom_button.setFixedWidth(
            60
        )

        custom_button.setFixedHeight(
            32
        )

        custom_button.clicked.connect(
            self.set_custom_timer
        )

        custom_layout.addWidget(
            self.custom_input
        )

        custom_layout.addWidget(
            custom_button
        )

        self.main_layout.addWidget(
            self.custom_frame
        )

        # =====================================================
        # CONTROLS
        # =====================================================

        controls = QHBoxLayout()

        self.start_button = QPushButton(
            "START"
        )

        self.reset_button = QPushButton(
            "RESET"
        )

        self.stop_button = QPushButton(
            "STOP"
        )

        self.start_button.setFixedHeight(
            40
        )

        self.reset_button.setFixedHeight(
            40
        )

        self.stop_button.setFixedHeight(
            40
        )

        self.start_button.clicked.connect(
            self.toggle_start
        )

        self.reset_button.clicked.connect(
            self.reset
        )

        self.stop_button.clicked.connect(
            self.stop_alarm
        )

        controls.addWidget(
            self.start_button
        )

        controls.addWidget(
            self.reset_button
        )

        controls.addWidget(
            self.stop_button
        )

        self.main_layout.addLayout(
            controls
        )

        # =====================================================
        # STOPWATCH LAPS
        # =====================================================

        self.lap_button = QPushButton(
            "LAP"
        )

        self.lap_button.setFixedHeight(
            32
        )

        self.lap_button.clicked.connect(
            self.add_lap
        )

        self.lap_button.hide()

        self.main_layout.addWidget(
            self.lap_button
        )

        self.apply_styles()

    # =========================================================
    # STYLES
    # =========================================================

    def apply_styles(self):

        button_style = """
            QPushButton {
                background: rgba(255,255,255,18);
                color: white;
                border: 1px solid rgba(255,255,255,25);
                border-radius: 9px;
                font-family: "Segoe UI";
                font-size: 9px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: rgba(255,255,255,30);
            }

            QPushButton:pressed {
                background: rgba(255,255,255,42);
            }
        """

        self.timer_mode_button.setStyleSheet(
            button_style
        )

        self.stopwatch_mode_button.setStyleSheet(
            button_style
        )

        self.start_button.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,30);
                color: white;
                border: 1px solid rgba(255,255,255,40);
                border-radius: 11px;
                font-family: "Segoe UI";
                font-size: 11px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: rgba(255,255,255,45);
            }

            QPushButton:pressed {
                background: rgba(255,255,255,55);
            }
        """)

        self.reset_button.setStyleSheet(
            button_style
        )

        self.stop_button.setStyleSheet(
            button_style
        )

        self.lap_button.setStyleSheet(
            button_style
        )

        self.custom_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,14);
                color: white;
                border: 1px solid rgba(255,255,255,25);
                border-radius: 9px;
                padding-left: 10px;
                font-family: "Segoe UI";
                font-size: 10px;
            }

            QLineEdit:focus {
                border: 1px solid rgba(255,255,255,50);
            }
        """)

    # =========================================================
    # MODE
    # =========================================================

    def change_mode(self, mode):

        self.mode = mode

        self.stopwatch_running = False
        self.timer_running = False

        self.stop_alarm()

        if mode == "Timer":

            self.presets_frame.show()
            self.custom_frame.show()
            self.lap_button.hide()

            self.status_label.setText(
                "TIMER READY"
            )

            self.start_button.setText(
                "START"
            )

        else:

            self.presets_frame.hide()
            self.custom_frame.hide()
            self.lap_button.show()

            self.status_label.setText(
                "STOPWATCH READY"
            )

            self.start_button.setText(
                "START"
            )

            self.stopwatch_elapsed = 0

        self.update_display()

    # =========================================================
    # TIMER
    # =========================================================

    def set_timer(self, seconds):

        if self.mode != "Timer":
            return

        self.stop_alarm()

        self.timer_remaining = seconds
        self.timer_total = seconds

        self.timer_running = False

        self.start_button.setText(
            "START"
        )

        self.status_label.setText(
            "READY"
        )

        self.update_display()

    # =========================================================
    # CUSTOM TIMER
    # =========================================================

    def set_custom_timer(self):

        try:

            seconds = float(
                self.custom_input.text()
            )

            if seconds <= 0:
                return

            self.set_timer(
                int(seconds)
            )

            self.custom_input.clear()

        except ValueError:

            self.custom_input.clear()

    # =========================================================
    # START / PAUSE
    # =========================================================

    def toggle_start(self):

        if self.mode == "Timer":

            if self.timer_remaining <= 0:
                return

            self.timer_running = (
                not self.timer_running
            )

            if self.timer_running:

                self.stop_alarm()

                self.status_label.setText(
                    "COUNTING DOWN"
                )

                self.start_button.setText(
                    "PAUSE"
                )

            else:

                self.status_label.setText(
                    "PAUSED"
                )

                self.start_button.setText(
                    "RESUME"
                )

        else:

            self.stopwatch_running = (
                not self.stopwatch_running
            )

            if self.stopwatch_running:

                self.stopwatch_started_at = (
                    time.monotonic()
                    - self.stopwatch_elapsed
                )

                self.status_label.setText(
                    "RUNNING"
                )

                self.start_button.setText(
                    "PAUSE"
                )

            else:

                self.stopwatch_elapsed = (
                    time.monotonic()
                    - self.stopwatch_started_at
                )

                self.status_label.setText(
                    "PAUSED"
                )

                self.start_button.setText(
                    "RESUME"
                )

    # =========================================================
    # LOAD ALARM SOUND
    # =========================================================

    def load_alarm_sound(self):

        filename = self.sound_files.get(
            self.alarm_sound
        )

        if not filename:
            return

        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(
                os.path.abspath(sys.executable)
            )
        else:
            base_dir = os.path.dirname(
                os.path.abspath(__file__)
            )

        sound_path = os.path.join(
            base_dir,
            filename
        )

        if not os.path.exists(sound_path):

            print(
                f"[GLOX WATCHER] Sound not found: "
                f"{sound_path}"
            )

            return

        self.alarm_player.setSource(
            QUrl.fromLocalFile(
                sound_path
            )
        )

    # =========================================================
    # PLAY ALARM
    # =========================================================

    def play_alarm(self):

        self.load_alarm_sound()

        if self.alarm_player.source().isEmpty():

            print(
                "[GLOX WATCHER] Could not load "
                "alarm sound."
            )

            return

        self.alarm_player.stop()

        # Play the selected sound 10 times
        self.alarm_player.setLoopCount(
            10
        )

        self.alarm_player.play()

    # =========================================================
    # STOP ALARM
    # =========================================================

    def stop_alarm(self):

        self.alarm_player.stop()

    # =========================================================
    # UPDATE
    # =========================================================

    def update_display(self):

        if self.mode == "Timer":

            if self.timer_running:

                self.timer_remaining -= 0.05

                if self.timer_remaining <= 0:

                    self.timer_remaining = 0

                    self.timer_running = False

                    self.start_button.setText(
                        "START"
                    )

                    self.status_label.setText(
                        "TIME'S UP"
                    )

                    # Start 10-loop alarm
                    self.play_alarm()

            seconds = max(
                0,
                int(self.timer_remaining)
            )

            self.display.setText(
                self.format_time(seconds)
            )

        else:

            if self.stopwatch_running:

                self.stopwatch_elapsed = (
                    time.monotonic()
                    - self.stopwatch_started_at
                )

            self.display.setText(
                self.format_stopwatch(
                    self.stopwatch_elapsed
                )
            )

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.timer_running = False
        self.stopwatch_running = False

        self.stop_alarm()

        if self.mode == "Timer":

            self.timer_remaining = 0
            self.timer_total = 0

            self.display.setText(
                "00:00:00"
            )

            self.status_label.setText(
                "READY"
            )

        else:

            self.stopwatch_elapsed = 0

            self.display.setText(
                "00:00:00.00"
            )

            self.status_label.setText(
                "STOPWATCH READY"
            )

        self.start_button.setText(
            "START"
        )

    # =========================================================
    # LAP
    # =========================================================

    def add_lap(self):

        if (
            self.mode == "Stopwatch"
            and self.stopwatch_running
        ):

            elapsed = self.stopwatch_elapsed

            print(
                f"LAP — "
                f"{self.format_stopwatch(elapsed)}"
            )

    # =========================================================
    # FORMAT TIMER
    # =========================================================

    def format_time(self, seconds):

        hours = seconds // 3600

        minutes = (
            seconds % 3600
        ) // 60

        secs = seconds % 60

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d}"
        )

    # =========================================================
    # FORMAT STOPWATCH
    # =========================================================

    def format_stopwatch(self, seconds):

        hours = int(
            seconds // 3600
        )

        minutes = int(
            (seconds % 3600) // 60
        )

        secs = int(
            seconds % 60
        )

        centiseconds = int(
            (seconds * 100) % 100
        )

        return (
            f"{hours:02d}:"
            f"{minutes:02d}:"
            f"{secs:02d}."
            f"{centiseconds:02d}"
        )

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

        # =====================================================
        # THEME
        # =====================================================

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
                theme_name ==
                self.current_theme
            )

            action.triggered.connect(
                lambda checked=False,
                name=theme_name:
                self.change_theme(name)
            )

        # =====================================================
        # ALARM SOUND
        # =====================================================

        sound_menu = menu.addMenu(
            "Alarm Sound"
        )

        sounds = [
            "Nightrain",
            "Sunrise",
            "Groovy",
            "Intense",
            "Drama",
        ]

        for sound in sounds:

            action = sound_menu.addAction(
                sound
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                sound == self.alarm_sound
            )

            action.triggered.connect(
                lambda checked=False,
                s=sound:
                self.change_sound(s)
            )

        # =====================================================
        # OPACITY
        # =====================================================

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

        # =====================================================
        # EXIT
        # =====================================================

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
    # THEME
    # =========================================================

    def change_theme(self, theme_name):

        self.current_theme = theme_name

        self.update()

        self.apply_styles()

    # =========================================================
    # SOUND
    # =========================================================

    def change_sound(self, sound):

        self.stop_alarm()

        self.alarm_sound = sound

        self.load_alarm_sound()

        print(
            f"[GLOX WATCHER] "
            f"Alarm sound: {sound}"
        )

    # =========================================================
    # OPACITY
    # =========================================================

    def change_opacity(self, value):

        self.opacity_value = value

        self.update_opacity()

    def update_opacity(self):

        self.setWindowOpacity(
            self.opacity_value / 100
        )

    # =========================================================
    # PAINT
    # =========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

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
            20,
            20
        )

    # =========================================================
    # DRAG WINDOW
    # =========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.dragging = True

            self.drag_offset = (
                event.globalPosition()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

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

    def mouseReleaseEvent(self, event):

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

    widget = GloxWatcher()

    widget.show()

    sys.exit(
        app.exec()
    )

