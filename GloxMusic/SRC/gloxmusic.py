# ============================================================
# GloxMusic
# Glox Industries | AvgLucer | Gaurav W
#
# Requirements:
#     pip install PySide6
#
# Folder:
#     GMusic/
#         song1.mp3
#         song2.mp3
#         song3.mp3
#
# Run:
#     python gloxmusic.py
#
# No pygame required.
# Uses PySide6.QtMultimedia.
# ============================================================

import sys
import os
import math
import json

from PySide6.QtCore import (
    Qt,
    QTimer,
    QRect,
    QPoint,
    QEasingCurve,
    QPropertyAnimation,
    Signal,
    QUrl,
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPen,
    QBrush,
    QFont,
    QAction,
)

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QSlider,
    QMenu,
    QGraphicsDropShadowEffect,
)

from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput,
)


# ============================================================
# CONFIG
# ============================================================

APP_NAME = "GloxMusic"

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GMUSIC_DIR = os.path.join(
    BASE_DIR,
    "GMusic"
)

CONFIG_DIR = os.path.join(
    os.path.expanduser("~"),
    ".gloxmusic"
)

CONFIG_FILE = os.path.join(
    CONFIG_DIR,
    "config.json"
)

os.makedirs(
    GMUSIC_DIR,
    exist_ok=True
)

os.makedirs(
    CONFIG_DIR,
    exist_ok=True
)


# ============================================================
# 8 GLOX THEMES
# ============================================================

THEMES = {

    "Crystal Cream": {
        "bg": "#E9E0D4",
        "panel": "#F3EBE1",
        "card": "#DED2C3",
        "text": "#43382F",
        "muted": "#817365",
        "accent": "#92785A",
        "accent2": "#B59A76",
        "border": "#C9B9A5",
    },

    "Midnight": {
        "bg": "#111217",
        "panel": "#1B1D24",
        "card": "#282B34",
        "text": "#F1F1F4",
        "muted": "#9699A5",
        "accent": "#8D82C4",
        "accent2": "#AAA0E0",
        "border": "#383B47",
    },

    "Ocean": {
        "bg": "#D5E4E7",
        "panel": "#E6F0F1",
        "card": "#C3D7DA",
        "text": "#304247",
        "muted": "#698087",
        "accent": "#5D8992",
        "accent2": "#7EAAB2",
        "border": "#ABC3C7",
    },

    "Lavender": {
        "bg": "#DCD4E9",
        "panel": "#ECE7F3",
        "card": "#CEC2DE",
        "text": "#44394F",
        "muted": "#786C83",
        "accent": "#856DA5",
        "accent2": "#A68BC5",
        "border": "#BBAECC",
    },

    "Graphite": {
        "bg": "#18191B",
        "panel": "#242528",
        "card": "#303236",
        "text": "#EEEEEE",
        "muted": "#999B9F",
        "accent": "#858585",
        "accent2": "#AAAAAA",
        "border": "#414348",
    },

    "Sage": {
        "bg": "#DCE4D9",
        "panel": "#EAF0E7",
        "card": "#CBD8C7",
        "text": "#384536",
        "muted": "#6E7D69",
        "accent": "#708A68",
        "accent2": "#8CA583",
        "border": "#B5C5B0",
    },

    "Rose": {
        "bg": "#E9D9DC",
        "panel": "#F2E6E8",
        "card": "#DEC7CA",
        "text": "#503A3F",
        "muted": "#896D72",
        "accent": "#A76E79",
        "accent2": "#C28A94",
        "border": "#CBAFB4",
    },

    "Blood Red": {
        "bg": "#211416",
        "panel": "#301A1D",
        "card": "#422226",
        "text": "#F3E8E8",
        "muted": "#B89A9D",
        "accent": "#80232B",
        "accent2": "#A83842",
        "border": "#5E3035",
    },
}


# ============================================================
# CONFIG
# ============================================================

def load_config():

    default = {
        "theme": "Crystal Cream",
        "opacity": 94,
        "volume": 80,
    }

    if not os.path.exists(CONFIG_FILE):
        return default

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return {
            "theme": data.get(
                "theme",
                default["theme"]
            ),
            "opacity": data.get(
                "opacity",
                default["opacity"]
            ),
            "volume": data.get(
                "volume",
                default["volume"]
            ),
        }

    except Exception:

        return default


def save_config(
    theme,
    opacity,
    volume
):

    try:

        with open(
            CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "theme": theme,
                    "opacity": opacity,
                    "volume": volume,
                },
                f,
                indent=4
            )

    except Exception:
        pass


# ============================================================
# ROUNDED FRAME
# ============================================================

class RoundedFrame(QFrame):

    def __init__(
        self,
        radius=30,
        parent=None
    ):

        super().__init__(parent)

        self.radius = radius

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        rect = self.rect().adjusted(
            1,
            1,
            -1,
            -1
        )

        path = QPainterPath()

        path.addRoundedRect(
            rect,
            self.radius,
            self.radius
        )

        painter.fillPath(
            path,
            QBrush(
                self.palette().window().color()
            )
        )

        painter.setPen(
            QPen(
                QColor(
                    255,
                    255,
                    255,
                    38
                ),
                1
            )
        )

        painter.drawPath(path)


# ============================================================
# VISUALIZER
# ============================================================

class MusicVisualizer(QWidget):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(parent)

        self.phase = 0.0
        self.progress = 0.0
        self.playing = False

        self.theme = THEMES[
            "Crystal Cream"
        ]

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(25)

        self.setMinimumHeight(185)

    def set_theme(
        self,
        theme
    ):

        self.theme = theme
        self.update()

    def set_playing(
        self,
        playing
    ):

        self.playing = playing

        self.update()

    def set_progress(
        self,
        value
    ):

        self.progress = value
        self.update()

    def animate(self):

        if self.playing:

            self.phase += 0.13

            if self.phase > math.pi * 2:

                self.phase -= math.pi * 2

            self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        w = self.width()
        h = self.height()

        cx = w / 2
        cy = h / 2

        t = self.theme

        # ----------------------------------------------------
        # SOFT BACKGROUND
        # ----------------------------------------------------

        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(
            QColor(t["bg"])
        )

        painter.drawRoundedRect(
            self.rect().adjusted(
                1,
                1,
                -1,
                -1
            ),
            25,
            25
        )

        # ----------------------------------------------------
        # OUTER RINGS
        # ----------------------------------------------------

        for i, radius in enumerate(
            (28, 50, 73)
        ):

            pulse = 0

            if self.playing:

                pulse = (
                    math.sin(
                        self.phase
                        + i * 0.8
                    )
                    + 1
                ) * 3.5

            r = radius + pulse

            alpha = 45 - i * 10

            painter.setBrush(
                Qt.BrushStyle.NoBrush
            )

            painter.setPen(
                QPen(
                    QColor(
                        t["accent"]
                    ),
                    1.5
                )
            )

            painter.drawEllipse(
                QPoint(
                    int(cx),
                    int(cy)
                ),
                int(r),
                int(r)
            )

        # ----------------------------------------------------
        # CENTRAL MUSIC DISC
        # ----------------------------------------------------

        center_radius = 25

        pulse = 0

        if self.playing:

            pulse = (
                math.sin(
                    self.phase * 1.7
                )
                + 1
            ) * 3

        painter.setBrush(
            QColor(t["accent"])
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.drawEllipse(
            QPoint(
                int(cx),
                int(cy)
            ),
            int(center_radius + pulse),
            int(center_radius + pulse)
        )

        # ----------------------------------------------------
        # INNER DISC
        # ----------------------------------------------------

        painter.setBrush(
            QColor(t["panel"])
        )

        painter.drawEllipse(
            QPoint(
                int(cx),
                int(cy)
            ),
            9,
            9
        )

        # ----------------------------------------------------
        # ORBITING DOT
        # ----------------------------------------------------

        angle = self.phase

        orbit_radius = 75

        dot_x = (
            cx
            +
            math.cos(angle)
            * orbit_radius
        )

        dot_y = (
            cy
            +
            math.sin(angle)
            * orbit_radius
        )

        painter.setBrush(
            QColor(t["accent2"])
        )

        painter.drawEllipse(
            QPoint(
                int(dot_x),
                int(dot_y)
            ),
            5,
            5
        )

        # ----------------------------------------------------
        # BEAT-MATCHED SMALL CIRCLES
        # ----------------------------------------------------

        for i in range(12):

            angle = (
                self.phase * 0.65
                +
                i
                *
                (math.pi * 2 / 12)
            )

            base_radius = 92 + (
                i % 3
            ) * 9

            if self.playing:

                bounce = (
                    math.sin(
                        self.phase * 2.0
                        +
                        i * 0.55
                    )
                    + 1
                ) * 4

            else:

                bounce = 0

            r = base_radius + bounce

            x = (
                cx
                +
                math.cos(angle)
                * r
            )

            y = (
                cy
                +
                math.sin(angle)
                * r
            )

            size = 2.5 + (
                bounce * 0.35
            )

            painter.setBrush(
                QColor(
                    t["accent"],
                )
            )

            painter.drawEllipse(
                QPoint(
                    int(x),
                    int(y)
                ),
                int(size),
                int(size)
            )


# ============================================================
# COLLAPSED BUTTON
# ============================================================

class CollapsedMusicButton(QPushButton):

    clicked_to_expand = Signal()

    def __init__(
        self,
        theme,
        parent=None
    ):

        super().__init__(parent)

        self.theme = theme

        self.drag_start = None

        self.was_dragged = False

        self.setFixedSize(
            92,
            48
        )

        self.setText(
            "GLOX"
        )

        self.setCursor(
            Qt.CursorShape.OpenHandCursor
        )

        self.apply_theme()

    def apply_theme(self):

        t = self.theme

        self.setStyleSheet(
            f"""
            QPushButton {{
                background: {t["accent"]};
                color: white;
                border: none;
                border-radius: 24px;
                font-size: 11px;
                font-weight: 800;
                letter-spacing: 1px;
            }}

            QPushButton:hover {{
                background: {t["accent2"]};
            }}
            """
        )

    def mousePressEvent(
        self,
        event
    ):

        if (
            event.button()
            ==
            Qt.MouseButton.LeftButton
        ):

            self.drag_start = (
                event.globalPosition().toPoint()
            )

            self.was_dragged = False

            self.setCursor(
                Qt.CursorShape.ClosedHandCursor
            )

            event.accept()

            return

        super().mousePressEvent(
            event
        )

    def mouseMoveEvent(
        self,
        event
    ):

        if (
            self.drag_start is not None
            and
            event.buttons()
            &
            Qt.MouseButton.LeftButton
        ):

            current = (
                event.globalPosition().toPoint()
            )

            delta = (
                current
                -
                self.drag_start
            )

            if (
                abs(delta.x()) > 3
                or
                abs(delta.y()) > 3
            ):

                self.was_dragged = True

                window = self.window()

                new_pos = (
                    window.pos()
                    +
                    delta
                )

                window.move(
                    new_pos
                )

                self.drag_start = current

            event.accept()

            return

        super().mouseMoveEvent(
            event
        )

    def mouseReleaseEvent(
        self,
        event
    ):

        self.setCursor(
            Qt.CursorShape.OpenHandCursor
        )

        if (
            event.button()
            ==
            Qt.MouseButton.LeftButton
        ):

            if not self.was_dragged:

                self.clicked_to_expand.emit()

            self.drag_start = None

            event.accept()

            return

        super().mouseReleaseEvent(
            event
        )


# ============================================================
# MAIN GLOX MUSIC
# ============================================================

class GloxMusic(QWidget):

    def __init__(self):

        super().__init__()

        self.config = load_config()

        self.theme_name = (
            self.config["theme"]
        )

        if self.theme_name not in THEMES:

            self.theme_name = (
                "Crystal Cream"
            )

        self.opacity_value = (
            self.config["opacity"]
        )

        self.volume_value = (
            self.config["volume"]
        )

        self.collapsed = False

        self.old_geometry = None

        self.drag_pos = None

        # ----------------------------------------------------
        # MEDIA
        # ----------------------------------------------------

        self.audio_output = QAudioOutput(
            self
        )

        self.player = QMediaPlayer(
            self
        )

        self.player.setAudioOutput(
            self.audio_output
        )

        self.audio_output.setVolume(
            self.volume_value / 100
        )

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.resize(
            440,
            620
        )

        self.build_ui()

        self.apply_theme()

        self.connect_player()

        self.load_music()

    # ========================================================
    # BUILD UI
    # ========================================================

    def build_ui(self):

        self.root = RoundedFrame(
            32,
            self
        )

        self.root.setGeometry(
            self.rect()
        )

        self.root_layout = QVBoxLayout(
            self.root
        )

        self.root_layout.setContentsMargins(
            22,
            18,
            22,
            20
        )

        self.root_layout.setSpacing(
            10
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QHBoxLayout()

        header.setSpacing(
            8
        )

        logo = QLabel(
            "G"
        )

        logo.setObjectName(
            "logo"
        )

        logo.setFixedSize(
            36,
            36
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        logo.setFont(
            QFont(
                "Segoe UI",
                15,
                QFont.Weight.Bold
            )
        )

        title_box = QVBoxLayout()

        title_box.setSpacing(
            0
        )

        self.title_label = QLabel(
            "GLOX MUSIC"
        )

        self.title_label.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Weight.Bold
            )
        )

        self.subtitle_label = QLabel(
            "your music  •  your space"
        )

        title_box.addWidget(
            self.title_label
        )

        title_box.addWidget(
            self.subtitle_label
        )

        header.addWidget(
            logo
        )

        header.addLayout(
            title_box
        )

        header.addStretch()

        self.minimize_button = QPushButton(
            "—"
        )

        self.minimize_button.setFixedSize(
            34,
            34
        )

        self.minimize_button.clicked.connect(
            self.collapse_widget
        )

        self.quit_button = QPushButton(
            "×"
        )

        self.quit_button.setFixedSize(
            34,
            34
        )

        self.quit_button.clicked.connect(
            QApplication.quit
        )

        header.addWidget(
            self.minimize_button
        )

        header.addWidget(
            self.quit_button
        )

        self.root_layout.addLayout(
            header
        )

        # ----------------------------------------------------
        # VISUALIZER
        # ----------------------------------------------------

        self.visualizer = MusicVisualizer(
            self.root
        )

        self.root_layout.addWidget(
            self.visualizer
        )

        # ----------------------------------------------------
        # CURRENT SONG
        # ----------------------------------------------------

        self.song_label = QLabel(
            "No music selected"
        )

        self.song_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.song_label.setFont(
            QFont(
                "Segoe UI",
                12,
                QFont.Weight.Bold
            )
        )

        self.root_layout.addWidget(
            self.song_label
        )

        self.time_label = QLabel(
            "0:00  /  0:00"
        )

        self.time_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.root_layout.addWidget(
            self.time_label
        )

        # ----------------------------------------------------
        # SEEK BAR
        # ----------------------------------------------------

        self.seek_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        self.seek_slider.setRange(
            0,
            0
        )

        self.seek_slider.sliderMoved.connect(
            self.seek_music
        )

        self.seek_slider.sliderPressed.connect(
            self.seek_pressed
        )

        self.seek_slider.sliderReleased.connect(
            self.seek_released
        )

        self.root_layout.addWidget(
            self.seek_slider
        )

        # ----------------------------------------------------
        # CONTROLS
        # ----------------------------------------------------

        controls = QHBoxLayout()

        controls.setSpacing(
            8
        )

        self.previous_button = QPushButton(
            "‹"
        )

        self.previous_button.setFixedSize(
            42,
            42
        )

        self.previous_button.clicked.connect(
            self.previous_song
        )

        self.play_button = QPushButton(
            "▶"
        )

        self.play_button.setFixedSize(
            54,
            54
        )

        self.play_button.clicked.connect(
            self.toggle_play
        )

        self.next_button = QPushButton(
            "›"
        )

        self.next_button.setFixedSize(
            42,
            42
        )

        self.next_button.clicked.connect(
            self.next_song
        )

        controls.addStretch()

        controls.addWidget(
            self.previous_button
        )

        controls.addWidget(
            self.play_button
        )

        controls.addWidget(
            self.next_button
        )

        controls.addStretch()

        self.root_layout.addLayout(
            controls
        )

        # ----------------------------------------------------
        # MUSIC LIST TITLE
        # ----------------------------------------------------

        list_header = QHBoxLayout()

        self.library_label = QLabel(
            "GMUSIC"
        )

        self.library_label.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold
            )
        )

        self.song_count_label = QLabel(
            "0 tracks"
        )

        list_header.addWidget(
            self.library_label
        )

        list_header.addStretch()

        list_header.addWidget(
            self.song_count_label
        )

        self.root_layout.addLayout(
            list_header
        )

        # ----------------------------------------------------
        # MUSIC LIST
        # ----------------------------------------------------

        self.music_list = QListWidget()

        self.music_list.setFixedHeight(
            125
        )

        self.music_list.itemClicked.connect(
            self.song_clicked
        )

        self.root_layout.addWidget(
            self.music_list
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status_label = QLabel(
            "Ready"
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.root_layout.addWidget(
            self.status_label
        )

    # ========================================================
    # PLAYER CONNECTIONS
    # ========================================================

    def connect_player(self):

        self.player.positionChanged.connect(
            self.position_changed
        )

        self.player.durationChanged.connect(
            self.duration_changed
        )

        self.player.playbackStateChanged.connect(
            self.playback_state_changed
        )

        self.player.mediaStatusChanged.connect(
            self.media_status_changed
        )

        # FIX:
        # Report actual Qt Multimedia playback errors.
        self.player.errorOccurred.connect(
            self.media_error
        )

    # ========================================================
    # LOAD MUSIC
    # ========================================================

    def load_music(self):

        self.music_list.clear()

        files = []

        try:

            for filename in os.listdir(
                GMUSIC_DIR
            ):

                if filename.lower().endswith(
                    ".mp3"
                ):

                    files.append(
                        filename
                    )

        except Exception:

            files = []

        files.sort(
            key=lambda x: x.lower()
        )

        for filename in files:

            item = QListWidgetItem(
                "♪  " + filename
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                os.path.join(
                    GMUSIC_DIR,
                    filename
                )
            )

            self.music_list.addItem(
                item
            )

        self.song_count_label.setText(
            f"{len(files)} tracks"
        )

        if not files:

            self.status_label.setText(
                "Put .mp3 files inside GMusic"
            )

        else:

            self.status_label.setText(
                "Ready"
            )

    # ========================================================
    # PLAY SONG
    # ========================================================

    def song_clicked(
        self,
        item
    ):

        path = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not path:
            return

        self.play_file(
            path
        )

    def play_file(
        self,
        path
    ):

        # ----------------------------------------------------
        # LOCAL FILE CHECK
        # ----------------------------------------------------

        if not path:

            self.status_label.setText(
                "Invalid music file"
            )

            return

        # Convert to an absolute Windows path.
        path = os.path.abspath(
            path
        )

        if not os.path.isfile(path):

            self.status_label.setText(
                "Music file not found"
            )

            return

        # ----------------------------------------------------
        # STOP CURRENT SONG
        # ----------------------------------------------------

        self.player.stop()

        # ----------------------------------------------------
        # IMPORTANT FIX
        #
        # QMediaPlayer expects a QUrl for local files.
        # Passing the Windows path directly can cause:
        #
        # FFmpeg error description:
        # No such file or directory
        # ----------------------------------------------------

        url = QUrl.fromLocalFile(
            path
        )

        self.player.setSource(
            url
        )

        # ----------------------------------------------------
        # UPDATE UI
        # ----------------------------------------------------

        self.song_label.setText(
            os.path.basename(path)
        )

        self.status_label.setText(
            "Loading..."
        )

        # ----------------------------------------------------
        # PLAY
        # ----------------------------------------------------

        self.player.play()

    # ========================================================
    # PLAY / PAUSE
    # ========================================================

    def toggle_play(self):

        if self.player.source().isEmpty():

            if self.music_list.count() > 0:

                item = (
                    self.music_list.item(0)
                )

                self.music_list.setCurrentItem(
                    item
                )

                self.song_clicked(
                    item
                )

            return

        if (
            self.player.playbackState()
            ==
            QMediaPlayer.PlaybackState.PlayingState
        ):

            self.player.pause()

        else:

            self.player.play()

    # ========================================================
    # PREVIOUS
    # ========================================================

    def previous_song(self):

        count = self.music_list.count()

        if count == 0:
            return

        current = (
            self.music_list.currentRow()
        )

        if current <= 0:

            current = count - 1

        else:

            current -= 1

        self.music_list.setCurrentRow(
            current
        )

        self.song_clicked(
            self.music_list.item(current)
        )

    # ========================================================
    # NEXT
    # ========================================================

    def next_song(self):

        count = self.music_list.count()

        if count == 0:
            return

        current = (
            self.music_list.currentRow()
        )

        if current >= count - 1:

            current = 0

        else:

            current += 1

        self.music_list.setCurrentRow(
            current
        )

        self.song_clicked(
            self.music_list.item(current)
        )

    # ========================================================
    # PLAYER POSITION
    # ========================================================

    def position_changed(
        self,
        position
    ):

        if not self.seek_slider.isSliderDown():

            self.seek_slider.setValue(
                position
            )

        self.update_time(
            position,
            self.player.duration()
        )

    def duration_changed(
        self,
        duration
    ):

        self.seek_slider.setRange(
            0,
            max(
                0,
                duration
            )
        )

        self.update_time(
            self.player.position(),
            duration
        )

    def update_time(
        self,
        position,
        duration
    ):

        def fmt(ms):

            seconds = max(
                0,
                int(ms / 1000)
            )

            minutes = (
                seconds // 60
            )

            seconds = (
                seconds % 60
            )

            return (
                f"{minutes}:"
                f"{seconds:02d}"
            )

        self.time_label.setText(
            f"{fmt(position)}  /  {fmt(duration)}"
        )

        if duration > 0:

            self.visualizer.set_progress(
                position / duration
            )

    # ========================================================
    # SEEKING
    # ========================================================

    def seek_pressed(self):

        self.was_seeking = True

    def seek_released(self):

        self.player.setPosition(
            self.seek_slider.value()
        )

        self.was_seeking = False

    def seek_music(
        self,
        position
    ):

        self.time_label.setText(
            self.format_seek_time(
                position
            )
            +
            "  /  "
            +
            self.format_seek_time(
                self.player.duration()
            )
        )

    def format_seek_time(
        self,
        ms
    ):

        seconds = max(
            0,
            int(ms / 1000)
        )

        minutes = (
            seconds // 60
        )

        seconds = (
            seconds % 60
        )

        return (
            f"{minutes}:"
            f"{seconds:02d}"
        )

    # ========================================================
    # PLAYBACK STATE
    # ========================================================

    def playback_state_changed(
        self,
        state
    ):

        playing = (
            state
            ==
            QMediaPlayer.PlaybackState.PlayingState
        )

        if playing:

            self.play_button.setText(
                "Ⅱ"
            )

            self.status_label.setText(
                "Playing"
            )

        else:

            self.play_button.setText(
                "▶"
            )

            if not self.player.source().isEmpty():

                self.status_label.setText(
                    "Paused"
                )

        self.visualizer.set_playing(
            playing
        )

    # ========================================================
    # MEDIA STATUS
    # ========================================================

    def media_status_changed(
        self,
        status
    ):

        if (
            status
            ==
            QMediaPlayer.MediaStatus.EndOfMedia
        ):

            self.next_song()

    # ========================================================
    # MEDIA ERROR
    # ========================================================

    def media_error(
        self,
        error,
        error_string
    ):

        if error == QMediaPlayer.Error.NoError:
            return

        self.status_label.setText(
            "Playback error"
        )

        self.visualizer.set_playing(
            False
        )

        print(
            "GloxMusic Media Error:",
            error,
            error_string
        )

    # ========================================================
    # THEME
    # ========================================================

    def apply_theme(self):

        t = THEMES[
            self.theme_name
        ]

        self.setWindowOpacity(
            self.opacity_value / 100
        )

        self.root.setStyleSheet(
            f"""
            QFrame {{
                background: {t["panel"]};
            }}
            """
        )

        self.visualizer.set_theme(
            t
        )

        self.title_label.setStyleSheet(
            f"color: {t['text']};"
        )

        self.subtitle_label.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 10px;
            """
        )

        self.song_label.setStyleSheet(
            f"""
            color: {t["text"]};
            """
        )

        self.time_label.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 10px;
            """
        )

        self.library_label.setStyleSheet(
            f"""
            color: {t["text"]};
            """
        )

        self.song_count_label.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 10px;
            """
        )

        self.status_label.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 10px;
            """
        )

        logo = self.root.findChild(
            QLabel,
            "logo"
        )

        logo.setStyleSheet(
            f"""
            QLabel {{
                background: {t["accent"]};
                color: white;
                border-radius: 18px;
            }}
            """
        )

        small_button_style = f"""
            QPushButton {{
                background: {t["card"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 17px;
                font-size: 15px;
            }}

            QPushButton:hover {{
                background: {t["accent"]};
                color: white;
            }}
        """

        self.minimize_button.setStyleSheet(
            small_button_style
        )

        self.quit_button.setStyleSheet(
            small_button_style
        )

        self.previous_button.setStyleSheet(
            small_button_style
        )

        self.next_button.setStyleSheet(
            small_button_style
        )

        self.play_button.setStyleSheet(
            f"""
            QPushButton {{
                background: {t["accent"]};
                color: white;
                border: none;
                border-radius: 27px;
                font-size: 17px;
                font-weight: 700;
            }}

            QPushButton:hover {{
                background: {t["accent2"]};
            }}
            """
        )

        self.seek_slider.setStyleSheet(
            f"""
            QSlider::groove:horizontal {{
                height: 5px;
                background: {t["border"]};
                border-radius: 3px;
            }}

            QSlider::sub-page:horizontal {{
                background: {t["accent"]};
                border-radius: 3px;
            }}

            QSlider::handle:horizontal {{
                width: 13px;
                height: 13px;
                margin: -4px 0;
                background: {t["accent"]};
                border-radius: 7px;
            }}
            """
        )

        self.music_list.setStyleSheet(
            f"""
            QListWidget {{
                background: {t["bg"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 17px;
                padding: 5px;
                outline: none;
            }}

            QListWidget::item {{
                padding: 8px 10px;
                border-radius: 11px;
                margin: 2px;
            }}

            QListWidget::item:hover {{
                background: {t["card"]};
            }}

            QListWidget::item:selected {{
                background: {t["accent"]};
                color: white;
            }}
            """
        )

        self.update()

    # ========================================================
    # RIGHT CLICK MENU
    # ========================================================

    def contextMenuEvent(
        self,
        event
    ):

        menu = QMenu(
            self
        )

        t = THEMES[
            self.theme_name
        ]

        menu.setStyleSheet(
            f"""
            QMenu {{
                background: {t["panel"]};
                color: #000000;
                border: 1px solid {t["border"]};
                padding: 6px;
            }}

            QMenu::item {{
                color: #000000;
                padding: 8px 18px;
                border-radius: 8px;
            }}

            QMenu::item:selected {{
                background: {t["card"]};
                color: #000000;
            }}

            QMenu::separator {{
                height: 1px;
                background: {t["border"]};
                margin: 5px 10px;
            }}
            """
        )

        # ----------------------------------------------------
        # THEME
        # ----------------------------------------------------

        theme_menu = menu.addMenu(
            "Background / Theme"
        )

        for name in THEMES:

            action = QAction(
                name,
                self
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                name == self.theme_name
            )

            action.triggered.connect(
                lambda checked=False,
                selected=name:
                self.change_theme(
                    selected
                )
            )

            theme_menu.addAction(
                action
            )

        menu.addSeparator()

        # ----------------------------------------------------
        # OPACITY
        # ----------------------------------------------------

        opacity_menu = menu.addMenu(
            "Opacity"
        )

        for opacity in (
            70,
            75,
            80,
            85,
            90,
            95,
            100
        ):

            action = QAction(
                f"{opacity}%",
                self
            )

            action.setCheckable(
                True
            )

            action.setChecked(
                opacity
                ==
                self.opacity_value
            )

            action.triggered.connect(
                lambda checked=False,
                value=opacity:
                self.change_opacity(
                    value
                )
            )

            opacity_menu.addAction(
                action
            )

        menu.addSeparator()

        # ----------------------------------------------------
        # REFRESH MUSIC
        # ----------------------------------------------------

        refresh_action = QAction(
            "Refresh GMusic",
            self
        )

        refresh_action.triggered.connect(
            self.load_music
        )

        menu.addAction(
            refresh_action
        )

        # ----------------------------------------------------
        # MINIMIZE
        # ----------------------------------------------------

        menu.addSeparator()

        minimize_action = QAction(
            "Minimize GloxMusic",
            self
        )

        minimize_action.triggered.connect(
            self.collapse_widget
        )

        menu.addAction(
            minimize_action
        )

        # ----------------------------------------------------
        # QUIT
        # ----------------------------------------------------

        quit_action = QAction(
            "Quit GloxMusic",
            self
        )

        quit_action.triggered.connect(
            QApplication.quit
        )

        menu.addAction(
            quit_action
        )

        menu.exec(
            event.globalPos()
        )

    # ========================================================
    # THEME CHANGE
    # ========================================================

    def change_theme(
        self,
        name
    ):

        if name not in THEMES:
            return

        self.theme_name = name

        self.apply_theme()

        self.save()

    # ========================================================
    # OPACITY
    # ========================================================

    def change_opacity(
        self,
        value
    ):

        self.opacity_value = value

        self.setWindowOpacity(
            value / 100
        )

        self.save()

    # ========================================================
    # SAVE
    # ========================================================

    def save(self):

        save_config(
            self.theme_name,
            self.opacity_value,
            self.volume_value
        )

    # ========================================================
    # COLLAPSE
    # ========================================================

    def collapse_widget(self):

        if self.collapsed:
            return

        self.collapsed = True

        self.old_geometry = (
            self.geometry()
        )

        start = self.geometry()

        end = QRect(
            start.x(),
            start.y(),
            92,
            48
        )

        animation = QPropertyAnimation(
            self,
            b"geometry"
        )

        animation.setDuration(
            360
        )

        animation.setEasingCurve(
            QEasingCurve.Type.OutCubic
        )

        animation.setStartValue(
            start
        )

        animation.setEndValue(
            end
        )

        animation.finished.connect(
            self.finish_collapse
        )

        self.collapse_animation = animation

        animation.start()

    def finish_collapse(self):

        self.root.hide()

        self.collapsed_button = (
            CollapsedMusicButton(
                THEMES[
                    self.theme_name
                ],
                self
            )
        )

        self.collapsed_button.setGeometry(
            0,
            0,
            92,
            48
        )

        self.collapsed_button.clicked_to_expand.connect(
            self.expand_widget
        )

        self.collapsed_button.show()

    # ========================================================
    # EXPAND
    # ========================================================

    def expand_widget(self):

        if not self.collapsed:
            return

        self.collapsed_button.hide()

        self.root.show()

        current = self.geometry()

        target = self.old_geometry

        animation = QPropertyAnimation(
            self,
            b"geometry"
        )

        animation.setDuration(
            420
        )

        animation.setEasingCurve(
            QEasingCurve.Type.OutBack
        )

        animation.setStartValue(
            current
        )

        animation.setEndValue(
            target
        )

        animation.finished.connect(
            self.expansion_finished
        )

        self.expand_animation = animation

        animation.start()

    def expansion_finished(self):

        if hasattr(
            self,
            "collapsed_button"
        ):

            self.collapsed_button.deleteLater()

        self.collapsed = False

    # ========================================================
    # DRAGGING
    # ========================================================

    def mousePressEvent(
        self,
        event
    ):

        if (
            event.button()
            ==
            Qt.MouseButton.LeftButton
        ):

            self.drag_pos = (
                event.globalPosition().toPoint()
                -
                self.frameGeometry().topLeft()
            )

            event.accept()

            return

        super().mousePressEvent(
            event
        )

    def mouseMoveEvent(
        self,
        event
    ):

        if (
            self.drag_pos is not None
            and
            event.buttons()
            &
            Qt.MouseButton.LeftButton
        ):

            target = (
                event.globalPosition().toPoint()
                -
                self.drag_pos
            )

            self.move(
                target
            )

            event.accept()

            return

        super().mouseMoveEvent(
            event
        )

    def mouseReleaseEvent(
        self,
        event
    ):

        self.drag_pos = None

        super().mouseReleaseEvent(
            event
        )

    # ========================================================
    # SHOW EVENT
    # ========================================================

    def showEvent(
        self,
        event
    ):

        super().showEvent(
            event
        )

        shadow = QGraphicsDropShadowEffect(
            self
        )

        shadow.setBlurRadius(
            45
        )

        shadow.setOffset(
            0,
            12
        )

        shadow.setColor(
            QColor(
                0,
                0,
                0,
                75
            )
        )

        self.root.setGraphicsEffect(
            shadow
        )


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        APP_NAME
    )

    app.setStyle(
        "Fusion"
    )

    widget = GloxMusic()

    screen = (
        app.primaryScreen()
    )

    if screen:

        available = (
            screen.availableGeometry()
        )

        widget.move(
            available.center()
            -
            widget.rect().center()
        )

    widget.show()

    sys.exit(
        app.exec()
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()