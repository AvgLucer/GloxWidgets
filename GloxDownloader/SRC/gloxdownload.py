# ============================================================
# GloxDownloader
# Glox Industries | AvgLucer | Gaurav W
#
# Requirements:
#     pip install PySide6 yt-dlp
#
# Optional:
#     ffmpeg.exe
#     ffprobe.exe
#
# Folder:
#     GloxDownloader/
#         gloxdownloader.py
#         ffmpeg.exe
#         ffprobe.exe
#         GDownloads/
#
# Supports publicly accessible:
#     YouTube
#     YouTube Shorts
#     Instagram
#     Facebook
#     and other yt-dlp supported sites
#
# Formats:
#     MP4
#     MP3
#
# Qualities:
#     4K
#     2K
#     1080p
#     720p
#     360p
#
# ============================================================

import sys
import os
import shutil
import threading
import subprocess
import json

from pathlib import Path

from PySide6.QtCore import (
    Qt,
    Signal,
    QObject,
    QThread,
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPen,
    QBrush,
    QFont,
)

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QFrame,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QProgressBar,
    QMenu,
)

import yt_dlp


# ============================================================
# CONFIG
# ============================================================

APP_NAME = "GloxDownloader"

BASE_DIR = Path(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DOWNLOAD_DIR = BASE_DIR / "GDownloads"

CONFIG_DIR = (
    Path.home()
    / ".gloxdownloader"
)

CONFIG_FILE = (
    CONFIG_DIR
    / "config.json"
)

DOWNLOAD_DIR.mkdir(
    exist_ok=True
)

CONFIG_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# THEMES
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
    }

    if not CONFIG_FILE.exists():
        return default

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8",
        ) as f:

            data = json.load(f)

        return {
            "theme": data.get(
                "theme",
                default["theme"],
            ),
            "opacity": data.get(
                "opacity",
                default["opacity"],
            ),
        }

    except Exception:

        return default


def save_config(
    theme,
    opacity,
):

    try:

        with open(
            CONFIG_FILE,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                {
                    "theme": theme,
                    "opacity": opacity,
                },
                f,
                indent=4,
            )

    except Exception:
        pass


# ============================================================
# FFMPEG DETECTION
# ============================================================

def find_ffmpeg():

    candidates = [

        BASE_DIR / "ffmpeg.exe",

        BASE_DIR / "bin" / "ffmpeg.exe",

        Path.cwd() / "ffmpeg.exe",

    ]

    for path in candidates:

        if path.exists():

            return str(path)

    system_ffmpeg = shutil.which(
        "ffmpeg"
    )

    if system_ffmpeg:
        return system_ffmpeg

    return None


def find_ffprobe():

    candidates = [

        BASE_DIR / "ffprobe.exe",

        BASE_DIR / "bin" / "ffprobe.exe",

        Path.cwd() / "ffprobe.exe",

    ]

    for path in candidates:

        if path.exists():

            return str(path)

    system_ffprobe = shutil.which(
        "ffprobe"
    )

    if system_ffprobe:
        return system_ffprobe

    return None


# ============================================================
# ROUNDED FRAME
# ============================================================

class RoundedFrame(QFrame):

    def __init__(
        self,
        radius=30,
        parent=None,
    ):

        super().__init__(
            parent
        )

        self.radius = radius

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

    def paintEvent(
        self,
        event,
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        rect = self.rect().adjusted(
            1,
            1,
            -1,
            -1,
        )

        path = QPainterPath()

        path.addRoundedRect(
            rect,
            self.radius,
            self.radius,
        )

        painter.fillPath(
            path,
            QBrush(
                self.palette().window().color()
            ),
        )

        painter.setPen(
            QPen(
                QColor(
                    255,
                    255,
                    255,
                    35,
                ),
                1,
            )
        )

        painter.drawPath(
            path
        )


# ============================================================
# DOWNLOAD WORKER
# ============================================================

class DownloadWorker(
    QObject
):

    progress = Signal(int)
    status = Signal(str)
    finished = Signal(bool, str)

    def __init__(
        self,
        url,
        quality,
        output_format,
    ):

        super().__init__()

        self.url = url
        self.quality = quality
        self.output_format = output_format

    def progress_hook(
        self,
        data,
    ):

        if data["status"] == "downloading":

            total = (
                data.get("total_bytes")
                or
                data.get("total_bytes_estimate")
            )

            downloaded = (
                data.get(
                    "downloaded_bytes",
                    0,
                )
            )

            if total:

                percent = int(
                    downloaded
                    * 100
                    / total
                )

                percent = max(
                    0,
                    min(
                        100,
                        percent,
                    ),
                )

                self.progress.emit(
                    percent
                )

            speed = data.get(
                "speed"
            )

            if speed:

                mb = speed / (
                    1024 * 1024
                )

                self.status.emit(
                    f"Downloading • "
                    f"{mb:.1f} MB/s"
                )

            else:

                self.status.emit(
                    "Downloading..."
                )

        elif data["status"] == "finished":

            self.progress.emit(
                100
            )

            self.status.emit(
                "Processing..."
            )

    def run(self):

        try:

            ffmpeg = find_ffmpeg()

            # ------------------------------------------------
            # MP3
            # ------------------------------------------------

            if self.output_format == "MP3":

                if not ffmpeg:

                    self.finished.emit(
                        False,
                        "MP3 requires ffmpeg.exe. "
                        "Put ffmpeg.exe beside GloxDownloader.",
                    )

                    return

                ydl_format = (
                    "bestaudio/best"
                )

            # ------------------------------------------------
            # MP4
            # ------------------------------------------------

            else:

                height = {
                    "360p": 360,
                    "720p": 720,
                    "1080p": 1080,
                    "2K": 1440,
                    "4K": 2160,
                }.get(
                    self.quality,
                    1080,
                )

                # Prefer progressive MP4 first.
                # If unavailable, yt-dlp can merge
                # video + audio when FFmpeg exists.

                if ffmpeg:

                    ydl_format = (
                        f"bestvideo[height<={height}]"
                        f"[ext=mp4]+"
                        f"bestaudio[ext=m4a]/"
                        f"best[height<={height}]"
                        f"[ext=mp4]/"
                        f"best[height<={height}]"
                    )

                else:

                    ydl_format = (
                        f"best[height<={height}]"
                        f"[ext=mp4]/"
                        f"best[height<={height}]"
                    )

            options = {

                "format": ydl_format,

                "outtmpl": str(
                    DOWNLOAD_DIR
                    / "%(title)s.%(ext)s"
                ),

                "noplaylist": True,

                "quiet": True,

                "no_warnings": True,

                "progress_hooks": [
                    self.progress_hook
                ],

                "windowsfilenames": True,

            }

            # ------------------------------------------------
            # FFmpeg
            # ------------------------------------------------

            if ffmpeg:

                options[
                    "ffmpeg_location"
                ] = os.path.dirname(
                    ffmpeg
                )

            # ------------------------------------------------
            # MP3 POST PROCESSING
            # ------------------------------------------------

            if self.output_format == "MP3":

                options[
                    "postprocessors"
                ] = [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ]

            self.status.emit(
                "Preparing download..."
            )

            with yt_dlp.YoutubeDL(
                options
            ) as ydl:

                ydl.download(
                    [self.url]
                )

            self.finished.emit(
                True,
                "Download complete",
            )

        except Exception as e:

            message = str(e)

            if (
                "ffmpeg" in message.lower()
                and
                self.output_format == "MP4"
            ):

                message = (
                    "This quality needs FFmpeg "
                    "to merge video and audio."
                )

            self.finished.emit(
                False,
                message[:300],
            )


# ============================================================
# MAIN WIDGET
# ============================================================

class GloxDownloader(
    QWidget
):

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

        self.drag_pos = None

        self.thread = None
        self.worker = None

        # IMPORTANT:
        # This is a widget, not a maximizable application.
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            |
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setFixedSize(
            470,
            575,
        )

        self.build_ui()

        self.apply_theme()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        self.root = RoundedFrame(
            30,
            self,
        )

        self.root.setGeometry(
            0,
            0,
            470,
            575,
        )

        layout = QVBoxLayout(
            self.root
        )

        layout.setContentsMargins(
            24,
            20,
            24,
            22,
        )

        layout.setSpacing(
            14
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QHBoxLayout()

        logo = QLabel(
            "G"
        )

        logo.setFixedSize(
            38,
            38,
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        logo.setFont(
            QFont(
                "Segoe UI",
                16,
                QFont.Weight.Bold,
            )
        )

        logo.setObjectName(
            "logo"
        )

        title_box = QVBoxLayout()

        title_box.setSpacing(
            0
        )

        self.title = QLabel(
            "GLOX DOWNLOADER"
        )

        self.title.setFont(
            QFont(
                "Segoe UI",
                13,
                QFont.Weight.Bold,
            )
        )

        self.subtitle = QLabel(
            "download your media • your space"
        )

        title_box.addWidget(
            self.title
        )

        title_box.addWidget(
            self.subtitle
        )

        header.addWidget(
            logo
        )

        header.addLayout(
            title_box
        )

        header.addStretch()

        self.close_button = QPushButton(
            "×"
        )

        self.close_button.setFixedSize(
            36,
            36,
        )

        self.close_button.clicked.connect(
            QApplication.quit
        )

        header.addWidget(
            self.close_button
        )

        layout.addLayout(
            header
        )

        # ----------------------------------------------------
        # URL
        # ----------------------------------------------------

        self.url_label = QLabel(
            "VIDEO URL"
        )

        self.url_label.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Weight.Bold,
            )
        )

        layout.addWidget(
            self.url_label
        )

        self.url_input = QLineEdit()

        self.url_input.setPlaceholderText(
            "Paste a YouTube, Instagram, Facebook or other URL..."
        )

        self.url_input.setMinimumHeight(
            48
        )

        layout.addWidget(
            self.url_input
        )

        # ----------------------------------------------------
        # OPTIONS
        # ----------------------------------------------------

        options = QHBoxLayout()

        quality_box = QVBoxLayout()

        self.quality_label = QLabel(
            "QUALITY"
        )

        quality_box.addWidget(
            self.quality_label
        )

        self.quality_combo = QComboBox()

        self.quality_combo.addItems(
            [
                "4K",
                "2K",
                "1080p",
                "720p",
                "360p",
            ]
        )

        self.quality_combo.setCurrentText(
            "1080p"
        )

        quality_box.addWidget(
            self.quality_combo
        )

        format_box = QVBoxLayout()

        self.format_label = QLabel(
            "FORMAT"
        )

        format_box.addWidget(
            self.format_label
        )

        self.format_combo = QComboBox()

        self.format_combo.addItems(
            [
                "MP4",
                "MP3",
            ]
        )

        format_box.addWidget(
            self.format_combo
        )

        options.addLayout(
            quality_box
        )

        options.addLayout(
            format_box
        )

        layout.addLayout(
            options
        )

        # ----------------------------------------------------
        # DOWNLOAD BUTTON
        # ----------------------------------------------------

        self.download_button = QPushButton(
            "DOWNLOAD"
        )

        self.download_button.setMinimumHeight(
            52
        )

        self.download_button.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Weight.Bold,
            )
        )

        self.download_button.clicked.connect(
            self.start_download
        )

        layout.addWidget(
            self.download_button
        )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        self.progress = QProgressBar()

        self.progress.setRange(
            0,
            100,
        )

        self.progress.setValue(
            0
        )

        self.progress.setTextVisible(
            False
        )

        self.progress.setFixedHeight(
            7
        )

        layout.addWidget(
            self.progress
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        self.status = QLabel(
            "Ready"
        )

        self.status.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.status
        )

        # ----------------------------------------------------
        # INFO
        # ----------------------------------------------------

        self.info = QLabel(
            "Files are saved to  GDownloads"
        )

        self.info.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.info
        )

        layout.addStretch()

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        self.footer = QLabel(
            "GLOX INDUSTRIES  •  AvgLucer | Gaurav W"
        )

        self.footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.footer
        )

    # ========================================================
    # DOWNLOAD
    # ========================================================

    def start_download(self):

        url = (
            self.url_input.text()
            .strip()
        )

        if not url:

            self.status.setText(
                "Paste a video URL first"
            )

            return

        if (
            not url.startswith(
                "http://"
            )
            and
            not url.startswith(
                "https://"
            )
        ):

            self.status.setText(
                "Please enter a valid URL"
            )

            return

        quality = (
            self.quality_combo.currentText()
        )

        output_format = (
            self.format_combo.currentText()
        )

        self.progress.setValue(
            0
        )

        self.download_button.setEnabled(
            False
        )

        self.status.setText(
            "Starting..."
        )

        self.thread = QThread()

        self.worker = DownloadWorker(
            url,
            quality,
            output_format,
        )

        self.worker.moveToThread(
            self.thread
        )

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.progress.connect(
            self.update_progress
        )

        self.worker.status.connect(
            self.update_status
        )

        self.worker.finished.connect(
            self.download_finished
        )

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.start()

    # ========================================================
    # DOWNLOAD CALLBACKS
    # ========================================================

    def update_progress(
        self,
        value,
    ):

        self.progress.setValue(
            value
        )

    def update_status(
        self,
        text,
    ):

        self.status.setText(
            text
        )

    def download_finished(
        self,
        success,
        message,
    ):

        self.download_button.setEnabled(
            True
        )

        if success:

            self.progress.setValue(
                100
            )

            self.status.setText(
                "✓  Download complete"
            )

        else:

            self.status.setText(
                "Download failed"
            )

            self.progress.setValue(
                0
            )

            # Keep useful error in tooltip
            self.status.setToolTip(
                message
            )

            print(
                "\nGloxDownloader ERROR:"
            )

            print(
                message
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

        self.title.setStyleSheet(
            f"""
            color: {t["text"]};
            """
        )

        self.subtitle.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 10px;
            """
        )

        self.url_label.setStyleSheet(
            f"""
            color: {t["text"]};
            """
        )

        self.quality_label.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 9px;
            font-weight: 700;
            """
        )

        self.format_label.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 9px;
            font-weight: 700;
            """
        )

        self.status.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 10px;
            """
        )

        self.info.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 9px;
            """
        )

        self.footer.setStyleSheet(
            f"""
            color: {t["muted"]};
            font-size: 8px;
            """
        )

        logo = self.root.findChild(
            QLabel,
            "logo",
        )

        if logo:

            logo.setStyleSheet(
                f"""
                QLabel {{
                    background: {t["accent"]};
                    color: white;
                    border-radius: 19px;
                }}
                """
            )

        self.url_input.setStyleSheet(
            f"""
            QLineEdit {{
                background: {t["bg"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 16px;
                padding: 0 14px;
                font-size: 10px;
            }}

            QLineEdit:focus {{
                border: 1px solid {t["accent"]};
            }}
            """
        )

        combo_style = f"""
            QComboBox {{
                background: {t["bg"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 14px;
                padding: 9px 12px;
                min-height: 20px;
            }}

            QComboBox:hover {{
                border: 1px solid {t["accent"]};
            }}

            QComboBox QAbstractItemView {{
                background: {t["panel"]};
                color: {t["text"]};
                selection-background-color: {t["accent"]};
                selection-color: white;
            }}
        """

        self.quality_combo.setStyleSheet(
            combo_style
        )

        self.format_combo.setStyleSheet(
            combo_style
        )

        self.download_button.setStyleSheet(
            f"""
            QPushButton {{
                background: {t["accent"]};
                color: white;
                border: none;
                border-radius: 17px;
                font-size: 11px;
                font-weight: 800;
            }}

            QPushButton:hover {{
                background: {t["accent2"]};
            }}

            QPushButton:disabled {{
                background: {t["border"]};
                color: {t["muted"]};
            }}
            """
        )

        self.close_button.setStyleSheet(
            f"""
            QPushButton {{
                background: {t["card"]};
                color: {t["text"]};
                border: 1px solid {t["border"]};
                border-radius: 18px;
                font-size: 18px;
            }}

            QPushButton:hover {{
                background: {t["accent"]};
                color: white;
            }}
            """
        )

        self.progress.setStyleSheet(
            f"""
            QProgressBar {{
                background: {t["border"]};
                border: none;
                border-radius: 4px;
            }}

            QProgressBar::chunk {{
                background: {t["accent"]};
                border-radius: 4px;
            }}
            """
        )

    # ========================================================
    # RIGHT CLICK THEME MENU
    # ========================================================

    def contextMenuEvent(
        self,
        event,
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
            """
        )

        theme_menu = menu.addMenu(
            "Background / Theme"
        )

        for name in THEMES:

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
                selected=name:
                self.change_theme(
                    selected
                )
            )

        menu.addSeparator()

        opacity_menu = menu.addMenu(
            "Opacity"
        )

        for value in (
            70,
            75,
            80,
            85,
            90,
            95,
            100,
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
                selected=value:
                self.change_opacity(
                    selected
                )
            )

        menu.addSeparator()

        open_folder = menu.addAction(
            "Open GDownloads"
        )

        open_folder.triggered.connect(
            self.open_download_folder
        )

        menu.addSeparator()

        quit_action = menu.addAction(
            "Quit GloxDownloader"
        )

        quit_action.triggered.connect(
            QApplication.quit
        )

        menu.exec(
            event.globalPos()
        )

    # ========================================================
    # THEME CHANGE
    # ========================================================

    def change_theme(
        self,
        name,
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
        value,
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
        )

    # ========================================================
    # OPEN DOWNLOAD FOLDER
    # ========================================================

    def open_download_folder(
        self
    ):

        try:

            os.startfile(
                str(
                    DOWNLOAD_DIR
                )
            )

        except Exception:

            subprocess.Popen(
                [
                    "explorer",
                    str(
                        DOWNLOAD_DIR
                    ),
                ]
            )

    # ========================================================
    # DRAGGING
    # ========================================================

    def mousePressEvent(
        self,
        event,
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
        event,
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
        event,
    ):

        self.drag_pos = None

        super().mouseReleaseEvent(
            event
        )

    # ========================================================
    # PAINT
    # ========================================================

    def paintEvent(
        self,
        event,
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            QColor(
                0,
                0,
                0,
                45,
            )
        )

        painter.drawRoundedRect(
            self.rect().adjusted(
                3,
                5,
                -3,
                -3,
            ),
            30,
            30,
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

    widget = GloxDownloader()

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