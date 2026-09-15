# ============================================================
# GLOX AIR
# POLISHED EDITION
# ============================================================
#
# Offline Windows desktop voice assistant
#
# Features:
#   • Voice activation
#   • Wake words
#   • Dynamic app discovery
#   • Dynamic game discovery
#   • EXE / LNK launching
#   • Website shortcuts
#   • Google / YouTube / GitHub search
#   • Browser TAB closing
#   • App closing
#   • Media controls
#   • Timers
#   • Folder shortcuts
#   • Rounded UI
#   • Animated listening orb
#   • Right-click theme menu
#   • Right-click opacity menu
#   • Persistent settings
#   • Persistent app memory
#   • TTS protection
#
# ============================================================

import os
import re
import json
import time
import shutil
import difflib
import ctypes
import subprocess
import webbrowser
import datetime
import tempfile
import wave
import threading
import tkinter as tk

import sounddevice as sd
import speech_recognition as sr
import pyttsx3


# ============================================================
# PATHS
# ============================================================

HOME = os.path.expanduser("~")

MEMORY_FILE = os.path.join(
    HOME,
    ".glox_air_memory.json"
)

SETTINGS_FILE = os.path.join(
    HOME,
    ".glox_air_settings.json"
)


# ============================================================
# AUDIO
# ============================================================

SAMPLE_RATE = 16000
RECORD_SECONDS = 5


# ============================================================
# WAKE WORDS
# ============================================================

WAKE_WORDS = [
    "air",
    "hey air",
    "hello air",
    "hi air",

    "pair",
    "p air",

    "glox",
    "hey glox",
    "hello glox",

    "glocks"
]


# ============================================================
# COMMAND WORDS
# ============================================================

OPEN_WORDS = [
    "open",
    "launch",
    "start",
    "run",
    "execute",
    "show",
    "bring up"
]

CLOSE_WORDS = [
    "close",
    "exit",
    "quit",
    "terminate",
    "kill",
    "stop"
]


# ============================================================
# THEMES
# ============================================================

THEMES = {

    "Espresso": {
        "bg": "#171412",
        "panel": "#211c19",
        "panel2": "#28211d",
        "text": "#e8ddd5",
        "muted": "#8f8178",
        "accent": "#a9866d",
        "orb": "#c3a58e",
        "orb2": "#765c4d",
        "button": "#29221e",
        "border": "#45382f"
    },

    "Midnight": {
        "bg": "#0d1117",
        "panel": "#151b23",
        "panel2": "#1b222c",
        "text": "#dce4ee",
        "muted": "#77818d",
        "accent": "#8190a3",
        "orb": "#aebdce",
        "orb2": "#536171",
        "button": "#1d252f",
        "border": "#303a46"
    },

    "Jade": {
        "bg": "#101715",
        "panel": "#17201d",
        "panel2": "#1d2824",
        "text": "#dce8e2",
        "muted": "#71827a",
        "accent": "#78998a",
        "orb": "#9ab8a8",
        "orb2": "#506c60",
        "button": "#202b26",
        "border": "#31453c"
    },

    "Slate": {
        "bg": "#141618",
        "panel": "#1d2023",
        "panel2": "#24282c",
        "text": "#e0e2e4",
        "muted": "#7c8186",
        "accent": "#9299a1",
        "orb": "#b8bec5",
        "orb2": "#5f666e",
        "button": "#272b2f",
        "border": "#383d42"
    },

    "Obsidian": {
        "bg": "#0b0b0c",
        "panel": "#141416",
        "panel2": "#1a1a1d",
        "text": "#e4e4e5",
        "muted": "#707074",
        "accent": "#99999f",
        "orb": "#c2c2c8",
        "orb2": "#55555b",
        "button": "#1d1d20",
        "border": "#2b2b2f"
    }
}


# ============================================================
# WEBSITES
# ============================================================

WEBSITES = {

    "google":
        "https://google.com",

    "youtube":
        "https://youtube.com",

    "gmail":
        "https://mail.google.com",

    "github":
        "https://github.com",

    "linkedin":
        "https://linkedin.com",

    "instagram":
        "https://instagram.com",

    "facebook":
        "https://facebook.com",

    "reddit":
        "https://reddit.com",

    "discord":
        "https://discord.com",

    "spotify":
        "https://open.spotify.com",

    "netflix":
        "https://netflix.com",

    "chatgpt":
        "https://chatgpt.com",

    "gemini":
        "https://gemini.google.com",

    "claude":
        "https://claude.ai",

    "google drive":
        "https://drive.google.com",

    "google docs":
        "https://docs.google.com",

    "google sheets":
        "https://sheets.google.com",

    "google slides":
        "https://slides.google.com",

    "stackoverflow":
        "https://stackoverflow.com",

    "stack overflow":
        "https://stackoverflow.com",

    "leetcode":
        "https://leetcode.com",

    "hackerrank":
        "https://hackerrank.com",

    "devpost":
        "https://devpost.com",

    "wikipedia":
        "https://wikipedia.org",

    "canva":
        "https://canva.com",

    "notion":
        "https://notion.so",

    "outlook":
        "https://outlook.live.com",

    "zed":
        "https://zed.dev"
}


# ============================================================
# APP ALIASES
# ============================================================

APP_ALIASES = {

    "notepads": "notepad",
    "note pad": "notepad",

    "explorer": "file explorer",
    "windows explorer": "file explorer",

    "cmd": "command prompt",
    "command line": "command prompt",

    "power shell": "powershell",

    "win terminal": "terminal",
    "windows terminal": "terminal",

    "google chrome": "chrome",
    "chrome browser": "chrome",

    "mozilla": "firefox",
    "mozilla firefox": "firefox",

    "brave browser": "brave",

    "brave browser beta":
        "brave beta",

    "brave browser nightly":
        "brave nightly",

    "edge browser": "edge",
    "microsoft edge": "edge",

    "microsoft word": "word",
    "microsoft excel": "excel",

    "power point": "powerpoint",
    "microsoft powerpoint": "powerpoint",

    "ms word": "word",
    "ms excel": "excel",
    "ms powerpoint": "powerpoint",

    "microsoft office":
        "microsoft office",

    "visual studio code":
        "vs code",

    "visual studio code editor":
        "vs code",

    "vscode":
        "vs code",

    "r studio":
        "rstudio",

    "hours studio":
        "rstudio",

    "py charm":
        "pycharm",

    "intellij idea":
        "intellij",

    "android":
        "android studio",

    "notepad plus plus":
        "notepad++",

    "git hub":
        "github",

    "get hub":
        "github",

    "getup":
        "github",

    "gethub":
        "github",

    "forget hub":
        "github",

    "pg admin":
        "pgadmin",

    "pg admin 4":
        "pgadmin",

    "postgres":
        "postgresql",

    "postgres sql":
        "postgresql",

    "google gemini":
        "gemini",

    "chat gpt":
        "chatgpt",

    "c l a u d":
        "claude",

    "c l a u d e":
        "claude",

    "cloud":
        "claude",

    "clawed":
        "claude",

    "github copilot":
        "github copilot",

    "far cry four":
        "far cry 4",

    "wrc four":
        "wrc 4",

    "grand theft auto four":
        "gta 4",

    "grand theft auto five":
        "gta 5",

    "gta four":
        "gta 4",

    "gta five":
        "gta 5",

    "breath edge":
        "breathedge",

    "bed siege":
        "besiege"
}


# ============================================================
# FOLDERS
# ============================================================

SPECIAL_FOLDERS = {

    "downloads":
        os.path.join(HOME, "Downloads"),

    "documents":
        os.path.join(HOME, "Documents"),

    "pictures":
        os.path.join(HOME, "Pictures"),

    "videos":
        os.path.join(HOME, "Videos"),

    "music":
        os.path.join(HOME, "Music"),

    "desktop":
        os.path.join(HOME, "Desktop")
}


# ============================================================
# GLOX AIR
# ============================================================

class GloxAir:

    def __init__(self):

        self.running = True
        self.listening_enabled = False
        self.recording = False

        self.drag_x = 0
        self.drag_y = 0

        self.pulse = 0
        self.pulse_direction = 1

        self.app_memory = self.load_json(
            MEMORY_FILE
        )

        self.settings = self.load_json(
            SETTINGS_FILE
        )

        self.theme_name = self.settings.get(
            "theme",
            "Espresso"
        )

        self.opacity = float(
            self.settings.get(
                "opacity",
                0.96
            )
        )

        if self.theme_name not in THEMES:
            self.theme_name = "Espresso"

        # ====================================================
        # VOICE
        # ====================================================

        self.recognizer = sr.Recognizer()

        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.7

        self.engine = pyttsx3.init()

        self.engine.setProperty(
            "rate",
            175
        )

        self.engine.setProperty(
            "volume",
            1.0
        )

        # Prevent:
        # "run loop already started"
        self.tts_lock = threading.Lock()

        # ====================================================
        # WINDOW
        # ====================================================

        self.root = tk.Tk()

        self.root.title(
            "Glox Air"
        )

        self.root.geometry(
            "450x470"
        )

        self.root.overrideredirect(
            True
        )

        self.root.attributes(
            "-topmost",
            True
        )

        self.root.attributes(
            "-alpha",
            self.opacity
        )

        # Make outer window background transparent-ish
        self.root.configure(
            bg="#000000"
        )

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        self.root.geometry(
            f"450x470+{sw - 480}+{sh - 500}"
        )

        self.create_ui()

        self.apply_theme()

        self.bind_context_menu()

        self.animate()

    # ========================================================
    # JSON
    # ========================================================

    def load_json(
        self,
        path
    ):

        try:

            if os.path.exists(path):

                with open(
                    path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    return json.load(f)

        except Exception:
            pass

        return {}

    def save_json(
        self,
        path,
        data
    ):

        try:

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    data,
                    f,
                    indent=4
                )

        except Exception as e:

            print(
                "SAVE ERROR:",
                e
            )

    # ========================================================
    # UI
    # ========================================================

    def create_ui(self):

        self.canvas = tk.Canvas(
            self.root,
            width=450,
            height=470,
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Rounded main panel
        # ----------------------------------------------------

        self.main_panel = self.rounded_rect(
            self.canvas,
            8,
            8,
            442,
            462,
            radius=30
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        self.header = self.canvas.create_text(
            28,
            30,
            text="GLOX AIR",
            anchor="w",
            font=("Segoe UI", 11, "bold")
        )

        self.header_sub = self.canvas.create_text(
            28,
            49,
            text="OFFLINE DESKTOP ASSISTANT",
            anchor="w",
            font=("Segoe UI", 7)
        )

        # Close button
        self.close_button = self.rounded_rect(
            self.canvas,
            397,
            20,
            430,
            49,
            radius=14
        )

        self.close_text = self.canvas.create_text(
            413,
            34,
            text="×",
            font=("Segoe UI", 15)
        )

        self.canvas.tag_bind(
            self.close_button,
            "<Button-1>",
            lambda e: self.close()
        )

        self.canvas.tag_bind(
            self.close_text,
            "<Button-1>",
            lambda e: self.close()
        )

        # ----------------------------------------------------
        # Chat
        # ----------------------------------------------------

        self.chat_box = self.rounded_rect(
            self.canvas,
            22,
            72,
            428,
            165,
            radius=22
        )

        self.chat_label = self.canvas.create_text(
            38,
            88,
            text="AIR  •  Glox Air is ready.",
            anchor="nw",
            width=370,
            font=("Segoe UI", 9)
        )

        # ----------------------------------------------------
        # Orb
        # ----------------------------------------------------

        self.orb_outer = self.canvas.create_oval(
            145,
            175,
            305,
            335,
            width=3
        )

        self.orb_middle = self.canvas.create_oval(
            163,
            193,
            287,
            317,
            width=2
        )

        self.orb_inner = self.canvas.create_oval(
            187,
            217,
            263,
            293,
            width=2
        )

        self.orb_text = self.canvas.create_text(
            225,
            255,
            text="AIR",
            font=("Segoe UI", 21, "bold")
        )

        self.status = self.canvas.create_text(
            225,
            350,
            text="Ready",
            font=("Segoe UI", 8)
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        self.start_button = self.rounded_rect(
            self.canvas,
            90,
            380,
            205,
            420,
            radius=18
        )

        self.start_text = self.canvas.create_text(
            147,
            400,
            text="▶  START",
            font=("Segoe UI", 9, "bold")
        )

        self.stop_button = self.rounded_rect(
            self.canvas,
            245,
            380,
            360,
            420,
            radius=18
        )

        self.stop_text = self.canvas.create_text(
            302,
            400,
            text="■  STOP",
            font=("Segoe UI", 9, "bold")
        )

        self.canvas.tag_bind(
            self.start_button,
            "<Button-1>",
            lambda e: self.start_listening()
        )

        self.canvas.tag_bind(
            self.start_text,
            "<Button-1>",
            lambda e: self.start_listening()
        )

        self.canvas.tag_bind(
            self.stop_button,
            "<Button-1>",
            lambda e: self.stop_listening()
        )

        self.canvas.tag_bind(
            self.stop_text,
            "<Button-1>",
            lambda e: self.stop_listening()
        )

        # ----------------------------------------------------
        # Footer
        # ----------------------------------------------------

        self.footer = self.canvas.create_text(
            225,
            442,
            text='Say "Hey Air, open VS Code"',
            font=("Segoe UI", 7)
        )

        # ----------------------------------------------------
        # Dragging
        # ----------------------------------------------------

        self.canvas.bind(
            "<ButtonPress-1>",
            self.start_drag
        )

        self.canvas.bind(
            "<B1-Motion>",
            self.drag
        )

    # ========================================================
    # ROUNDED RECTANGLE
    # ========================================================

    def rounded_rect(
        self,
        canvas,
        x1,
        y1,
        x2,
        y2,
        radius=20,
        **kwargs
    ):

        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]

        return canvas.create_polygon(
            points,
            smooth=True,
            splinesteps=36,
            **kwargs
        )

    # ========================================================
    # THEME
    # ========================================================

    def apply_theme(self):

        theme = THEMES[
            self.theme_name
        ]

        self.root.configure(
            bg=theme["bg"]
        )

        self.canvas.configure(
            bg=theme["bg"]
        )

        # Main
        self.canvas.itemconfig(
            self.main_panel,
            fill=theme["panel"],
            outline=theme["border"]
        )

        # Chat
        self.canvas.itemconfig(
            self.chat_box,
            fill=theme["panel2"],
            outline=theme["border"]
        )

        self.canvas.itemconfig(
            self.chat_label,
            fill=theme["text"]
        )

        self.canvas.itemconfig(
            self.header,
            fill=theme["text"]
        )

        self.canvas.itemconfig(
            self.header_sub,
            fill=theme["muted"]
        )

        self.canvas.itemconfig(
            self.close_button,
            fill=theme["button"],
            outline=theme["border"]
        )

        self.canvas.itemconfig(
            self.close_text,
            fill=theme["text"]
        )

        self.canvas.itemconfig(
            self.orb_outer,
            outline=theme["orb"]
        )

        self.canvas.itemconfig(
            self.orb_middle,
            outline=theme["orb2"]
        )

        self.canvas.itemconfig(
            self.orb_inner,
            outline=theme["accent"]
        )

        self.canvas.itemconfig(
            self.orb_text,
            fill=theme["text"]
        )

        self.canvas.itemconfig(
            self.status,
            fill=theme["muted"]
        )

        self.canvas.itemconfig(
            self.start_button,
            fill=theme["button"],
            outline=theme["border"]
        )

        self.canvas.itemconfig(
            self.start_text,
            fill=theme["text"]
        )

        self.canvas.itemconfig(
            self.stop_button,
            fill=theme["button"],
            outline=theme["border"]
        )

        self.canvas.itemconfig(
            self.stop_text,
            fill=theme["text"]
        )

        self.canvas.itemconfig(
            self.footer,
            fill=theme["muted"]
        )

        self.settings[
            "theme"
        ] = self.theme_name

        self.settings[
            "opacity"
        ] = self.opacity

        self.save_json(
            SETTINGS_FILE,
            self.settings
        )

    # ========================================================
    # RIGHT CLICK MENU
    # ========================================================

    def bind_context_menu(self):

        self.root.bind(
            "<Button-3>",
            self.context_menu
        )

        self.canvas.bind(
            "<Button-3>",
            self.context_menu
        )

    def context_menu(
        self,
        event
    ):

        menu = tk.Menu(
            self.root,
            tearoff=0,
            bg="#181818",
            fg="#eeeeee",
            activebackground="#303030",
            activeforeground="white",
            bd=0
        )

        # ---------------- THEME ----------------

        theme_menu = tk.Menu(
            menu,
            tearoff=0,
            bg="#181818",
            fg="#eeeeee",
            activebackground="#303030",
            activeforeground="white",
            bd=0
        )

        for name in THEMES:

            theme_menu.add_command(
                label=(
                    "✓  " + name
                    if name == self.theme_name
                    else "    " + name
                ),
                command=lambda n=name:
                    self.set_theme(n)
            )

        menu.add_cascade(
            label="Theme",
            menu=theme_menu
        )

        # ---------------- OPACITY ----------------

        opacity_menu = tk.Menu(
            menu,
            tearoff=0,
            bg="#181818",
            fg="#eeeeee",
            activebackground="#303030",
            activeforeground="white",
            bd=0
        )

        opacity_values = [
            ("100%", 1.00),
            ("95%", 0.95),
            ("90%", 0.90),
            ("85%", 0.85),
            ("80%", 0.80),
            ("75%", 0.75)
        ]

        for label, value in opacity_values:

            opacity_menu.add_command(
                label=label,
                command=lambda v=value:
                    self.set_opacity(v)
            )

        menu.add_cascade(
            label="Opacity",
            menu=opacity_menu
        )

        menu.add_separator()

        menu.add_command(
            label="Start Listening",
            command=self.start_listening
        )

        menu.add_command(
            label="Stop Listening",
            command=self.stop_listening
        )

        menu.add_separator()

        menu.add_command(
            label="Exit Glox Air",
            command=self.close
        )

        menu.tk_popup(
            event.x_root,
            event.y_root
        )

    def set_theme(
        self,
        name
    ):

        if name not in THEMES:
            return

        self.theme_name = name

        self.apply_theme()

        self.show_message(
            "AIR",
            f"Theme changed to {name}."
        )

    def set_opacity(
        self,
        value
    ):

        self.opacity = value

        self.root.attributes(
            "-alpha",
            self.opacity
        )

        self.settings[
            "opacity"
        ] = self.opacity

        self.save_json(
            SETTINGS_FILE,
            self.settings
        )

    # ========================================================
    # DRAG
    # ========================================================

    def start_drag(
        self,
        event
    ):

        self.drag_x = event.x
        self.drag_y = event.y

    def drag(
        self,
        event
    ):

        x = (
            self.root.winfo_x()
            + event.x
            - self.drag_x
        )

        y = (
            self.root.winfo_y()
            + event.y
            - self.drag_y
        )

        self.root.geometry(
            f"+{x}+{y}"
        )

    # ========================================================
    # CHAT
    # ========================================================

    def show_message(
        self,
        speaker,
        text
    ):

        current = self.canvas.itemcget(
            self.chat_label,
            "text"
        )

        lines = current.split(
            "\n"
        )

        lines.append(
            f"{speaker}  •  {text}"
        )

        lines = lines[-5:]

        final = "\n".join(
            lines
        )

        try:

            self.root.after(
                0,
                lambda: self.canvas.itemconfig(
                    self.chat_label,
                    text=final
                )
            )

        except:
            pass

    # ========================================================
    # RESPONSE
    # ========================================================

    def respond(
        self,
        text,
        speak=True
    ):

        print(
            "AIR:",
            text
        )

        self.show_message(
            "AIR",
            text
        )

        self.status_text(
            text
        )

        if speak:

            threading.Thread(
                target=self.speak,
                args=(text,),
                daemon=True
            ).start()

    # ========================================================
    # STATUS
    # ========================================================

    def status_text(
        self,
        text
    ):

        try:

            self.root.after(
                0,
                lambda: self.canvas.itemconfig(
                    self.status,
                    text=text[:48]
                )
            )

        except:
            pass

    # ========================================================
    # TTS
    # ========================================================

    def speak(
        self,
        text
    ):

        with self.tts_lock:

            try:

                self.engine.say(
                    text
                )

                self.engine.runAndWait()

            except Exception as e:

                print(
                    "TTS ERROR:",
                    e
                )

    # ========================================================
    # ANIMATION
    # ========================================================

    def animate(self):

        if not self.running:
            return

        theme = THEMES[
            self.theme_name
        ]

        if self.recording:

            self.pulse += (
                2 * self.pulse_direction
            )

            if self.pulse >= 25:
                self.pulse_direction = -1

            if self.pulse <= 0:
                self.pulse_direction = 1

            p = self.pulse

            self.canvas.coords(
                self.orb_outer,
                145 - p,
                175 - p,
                305 + p,
                335 + p
            )

            self.canvas.itemconfig(
                self.orb_outer,
                outline=theme["accent"],
                width=4
            )

        else:

            self.canvas.coords(
                self.orb_outer,
                145,
                175,
                305,
                335
            )

            self.canvas.itemconfig(
                self.orb_outer,
                outline=theme["orb"],
                width=3
            )

        self.root.after(
            55,
            self.animate
        )

    # ========================================================
    # NORMALIZE
    # ========================================================

    def normalize(
        self,
        text
    ):

        text = text.lower().strip()

        replacements = {

            "pair": "air",
            "p air": "air",

            "getup": "github",
            "get hub": "github",
            "gethub": "github",
            "git hub": "github",
            "forget hub": "github",

            "googel": "google",

            "you tube": "youtube",

            "power point": "powerpoint",

            "r studio": "rstudio",
            "hours studio": "rstudio",

            "c l a u d":
                "claude",

            "c l a u d e":
                "claude",

            "cloud":
                "claude",

            "brave browser":
                "brave",

            "notepads":
                "notepad",

            "bed siege":
                "besiege",

            "breath edge":
                "breathedge",

            "far cry four":
                "far cry 4",

            "wrc four":
                "wrc 4",

            "gta four":
                "gta 4",

            "gta five":
                "gta 5",

            "grand theft auto four":
                "gta 4",

            "grand theft auto five":
                "gta 5"
        }

        for wrong, correct in replacements.items():

            text = text.replace(
                wrong,
                correct
            )

        return text

    # ========================================================
    # WAKE WORD
    # ========================================================

    def has_wake_word(
        self,
        text
    ):

        for wake in sorted(
            WAKE_WORDS,
            key=len,
            reverse=True
        ):

            if re.search(
                r"\b"
                + re.escape(wake)
                + r"\b",
                text
            ):

                return True

        return False

    def remove_wake(
        self,
        text
    ):

        for wake in sorted(
            WAKE_WORDS,
            key=len,
            reverse=True
        ):

            pattern = (
                r"\b"
                + re.escape(wake)
                + r"\b"
            )

            if re.search(
                pattern,
                text
            ):

                return re.sub(
                    pattern,
                    "",
                    text,
                    count=1
                ).strip()

        return text

    # ========================================================
    # RECORD
    # ========================================================

    def record(self):

        if not self.listening_enabled:
            return None

        self.recording = True

        self.status_text(
            "Listening..."
        )

        try:

            audio = sd.rec(
                int(
                    RECORD_SECONDS
                    * SAMPLE_RATE
                ),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="int16"
            )

            sd.wait()

            self.recording = False

            return audio

        except Exception as e:

            self.recording = False

            print(
                "MIC ERROR:",
                e
            )

            return None

    # ========================================================
    # LISTEN
    # ========================================================

    def listen(self):

        audio = self.record()

        if audio is None:
            return ""

        filename = tempfile.mktemp(
            suffix=".wav"
        )

        try:

            with wave.open(
                filename,
                "wb"
            ) as wf:

                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(
                    SAMPLE_RATE
                )

                wf.writeframes(
                    audio.tobytes()
                )

            with sr.AudioFile(
                filename
            ) as source:

                data = self.recognizer.record(
                    source
                )

            text = self.recognizer.recognize_google(
                data
            )

            text = self.normalize(
                text
            )

            print(
                "YOU:",
                text
            )

            self.show_message(
                "YOU",
                text
            )

            return text

        except sr.UnknownValueError:

            return ""

        except Exception as e:

            print(
                "RECOGNITION ERROR:",
                e
            )

            return ""

        finally:

            try:
                os.remove(
                    filename
                )
            except:
                pass

    # ========================================================
    # START LISTENING
    # ========================================================

    def start_listening(self):

        if self.listening_enabled:
            return

        self.listening_enabled = True

        self.respond(
            "Glox Air is ready."
        )

        threading.Thread(
            target=self.voice_loop,
            daemon=True
        ).start()

    # ========================================================
    # STOP LISTENING
    # ========================================================

    def stop_listening(self):

        self.listening_enabled = False
        self.recording = False

        try:
            sd.stop()
        except:
            pass

        self.status_text(
            "Stopped"
        )

        self.show_message(
            "AIR",
            "Voice mode stopped."
        )

    # ========================================================
    # VOICE LOOP
    # ========================================================

    def voice_loop(self):

        while (
            self.running
            and self.listening_enabled
        ):

            text = self.listen()

            if not text:
                continue

            if not self.has_wake_word(
                text
            ):

                continue

            command = self.remove_wake(
                text
            )

            if not command:

                self.respond(
                    "Yes?"
                )

                command = self.listen()

            if command:

                self.handle_command(
                    command
                )

    # ========================================================
    # FOLDER
    # ========================================================

    def open_folder(
        self,
        name
    ):

        name = name.lower().strip()

        if name in [
            "this pc",
            "my computer",
            "computer",
            "drives",
            "my files"
        ]:

            subprocess.Popen(
                [
                    "explorer.exe",
                    "shell:MyComputerFolder"
                ]
            )

            return True

        if name in SPECIAL_FOLDERS:

            path = SPECIAL_FOLDERS[name]

            if os.path.exists(path):

                os.startfile(path)

                return True

        return False

    # ========================================================
    # WEBSITE
    # ========================================================

    def open_website(
        self,
        name
    ):

        name = name.lower().strip()

        if name in WEBSITES:

            webbrowser.open(
                WEBSITES[name]
            )

            return True

        return False

    # ========================================================
    # START MENU LOCATIONS
    # ========================================================

    def get_start_menu_locations(self):

        locations = []

        program_data = os.environ.get(
            "PROGRAMDATA"
        )

        app_data = os.environ.get(
            "APPDATA"
        )

        if program_data:

            locations.append(
                os.path.join(
                    program_data,
                    "Microsoft",
                    "Windows",
                    "Start Menu",
                    "Programs"
                )
            )

        if app_data:

            locations.append(
                os.path.join(
                    app_data,
                    "Microsoft",
                    "Windows",
                    "Start Menu",
                    "Programs"
                )
            )

        return locations

    # ========================================================
    # CLEAN NAME
    # ========================================================

    def clean_name(
        self,
        name
    ):

        name = name.lower()

        name = re.sub(
            r"\.(exe|lnk)$",
            "",
            name
        )

        name = re.sub(
            r"[^a-z0-9]+",
            " ",
            name
        )

        return name.strip()

    # ========================================================
    # FUZZY SCORE
    # ========================================================

    def name_score(
        self,
        wanted,
        actual
    ):

        if wanted == actual:
            return 1.0

        if wanted in actual:
            return 0.90

        if actual in wanted:
            return 0.85

        return difflib.SequenceMatcher(
            None,
            wanted,
            actual
        ).ratio()

    # ========================================================
    # START MENU SEARCH
    # ========================================================

    def search_start_menu(
        self,
        target
    ):

        target = self.clean_name(
            target
        )

        matches = []

        for root in self.get_start_menu_locations():

            if not os.path.exists(root):
                continue

            for current, dirs, files in os.walk(root):

                for file in files:

                    if not file.lower().endswith(
                        ".lnk"
                    ):
                        continue

                    name = os.path.splitext(
                        file
                    )[0]

                    score = self.name_score(
                        target,
                        self.clean_name(name)
                    )

                    if score >= 0.50:

                        matches.append(
                            (
                                score,
                                os.path.join(
                                    current,
                                    file
                                ),
                                name
                            )
                        )

        matches.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return matches

    # ========================================================
    # DESKTOP SEARCH
    # ========================================================

    def search_desktop(
        self,
        target
    ):

        desktop = SPECIAL_FOLDERS[
            "desktop"
        ]

        if not os.path.exists(desktop):
            return []

        target = self.clean_name(
            target
        )

        matches = []

        for current, dirs, files in os.walk(
            desktop
        ):

            for file in files:

                if not (
                    file.lower().endswith(".lnk")
                    or
                    file.lower().endswith(".exe")
                ):
                    continue

                name = os.path.splitext(
                    file
                )[0]

                score = self.name_score(
                    target,
                    self.clean_name(name)
                )

                if score >= 0.45:

                    matches.append(
                        (
                            score,
                            os.path.join(
                                current,
                                file
                            ),
                            name
                        )
                    )

        matches.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return matches

    # ========================================================
    # PROGRAM FILE SEARCH
    # ========================================================

    def search_common_programs(
        self,
        target
    ):

        target = self.clean_name(
            target
        )

        roots = [

            os.environ.get(
                "PROGRAMFILES",
                ""
            ),

            os.environ.get(
                "PROGRAMFILES(X86)",
                ""
            ),

            os.environ.get(
                "LOCALAPPDATA",
                ""
            )
        ]

        matches = []

        for root in roots:

            if not root or not os.path.exists(root):
                continue

            try:

                for current, dirs, files in os.walk(
                    root
                ):

                    for file in files:

                        if not file.lower().endswith(
                            ".exe"
                        ):
                            continue

                        name = os.path.splitext(
                            file
                        )[0]

                        score = self.name_score(
                            target,
                            self.clean_name(name)
                        )

                        if score >= 0.60:

                            matches.append(
                                (
                                    score,
                                    os.path.join(
                                        current,
                                        file
                                    ),
                                    name
                                )
                            )

            except PermissionError:

                continue

        matches.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return matches[:10]

    # ========================================================
    # LAUNCH
    # ========================================================

    def launch_path(
        self,
        path
    ):

        try:

            if path.lower().endswith(
                ".lnk"
            ):

                os.startfile(path)

            else:

                subprocess.Popen(
                    [path]
                )

            return True

        except Exception as e:

            print(
                "LAUNCH ERROR:",
                e
            )

            return False

    # ========================================================
    # FIND + LAUNCH
    # ========================================================

    def find_and_launch(
        self,
        target
    ):

        target = APP_ALIASES.get(
            target,
            target
        )

        # Memory
        if target in self.app_memory:

            path = self.app_memory[target]

            if os.path.exists(path):

                if self.launch_path(path):

                    self.respond(
                        f"Opening {target}."
                    )

                    return True

        self.respond(
            f"Searching for {target}...",
            speak=False
        )

        # Start menu
        matches = self.search_start_menu(
            target
        )

        if matches:

            best = matches[0]

            if self.launch_path(
                best[1]
            ):

                self.app_memory[
                    target
                ] = best[1]

                self.save_json(
                    MEMORY_FILE,
                    self.app_memory
                )

                self.respond(
                    f"Opening {best[2]}."
                )

                return True

        # Desktop
        matches = self.search_desktop(
            target
        )

        if matches:

            best = matches[0]

            if self.launch_path(
                best[1]
            ):

                self.app_memory[
                    target
                ] = best[1]

                self.save_json(
                    MEMORY_FILE,
                    self.app_memory
                )

                self.respond(
                    f"Opening {best[2]}."
                )

                return True

        # Program Files
        matches = self.search_common_programs(
            target
        )

        if matches:

            best = matches[0]

            if self.launch_path(
                best[1]
            ):

                self.app_memory[
                    target
                ] = best[1]

                self.save_json(
                    MEMORY_FILE,
                    self.app_memory
                )

                self.respond(
                    f"Opening {best[2]}."
                )

                return True

        # PATH
        exe = target

        if not exe.endswith(
            ".exe"
        ):

            exe += ".exe"

        found = shutil.which(
            exe
        )

        if found:

            self.app_memory[
                target
            ] = found

            self.save_json(
                MEMORY_FILE,
                self.app_memory
            )

            self.launch_path(
                found
            )

            self.respond(
                f"Opening {target}."
            )

            return True

        return False

    # ========================================================
    # PROCESS FINDER
    # ========================================================

    def find_process(
        self,
        target
    ):

        target = self.clean_name(
            target
        )

        try:

            result = subprocess.run(
                ["tasklist"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

            best = None
            best_score = 0

            for line in result.stdout.splitlines():

                parts = line.split()

                if not parts:
                    continue

                process = parts[0]

                score = self.name_score(
                    target,
                    self.clean_name(process)
                )

                if score > best_score:

                    best_score = score
                    best = process

            if best_score >= 0.55:

                return best

        except Exception:
            pass

        return None

    # ========================================================
    # CLOSE APP
    # ========================================================

    def close_app(
        self,
        target
    ):

        target = APP_ALIASES.get(
            target,
            target
        )

        process = self.find_process(
            target
        )

        if not process:

            path = self.app_memory.get(
                target
            )

            if path:

                process = os.path.basename(
                    path
                )

        if process:

            try:

                subprocess.run(
                    [
                        "taskkill",
                        "/IM",
                        process,
                        "/F"
                    ],
                    capture_output=True
                )

                return True

            except:
                pass

        return False

    # ========================================================
    # BROWSER DETECTION
    # ========================================================

    def get_browser_process(
        self
    ):

        browsers = [
            "chrome.exe",
            "msedge.exe",
            "brave.exe",
            "firefox.exe"
        ]

        try:

            result = subprocess.run(
                ["tasklist"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

            running = result.stdout.lower()

            for browser in browsers:

                if browser in running:

                    return browser

        except:
            pass

        return None

    # ========================================================
    # FOCUS BROWSER
    # ========================================================

    def focus_browser(
        self,
        process
    ):

        try:

            script = f'''
            $p = Get-Process -Name "{process.replace(".exe","")}" -ErrorAction SilentlyContinue |
                 Where-Object {{ $_.MainWindowHandle -ne 0 }} |
                 Select-Object -First 1

            if ($p) {{
                Add-Type @"
                using System;
                using System.Runtime.InteropServices;

                public class Win {{
                    [DllImport("user32.dll")]
                    public static extern bool SetForegroundWindow(IntPtr hWnd);
                }}
"@

                [Win]::SetForegroundWindow($p.MainWindowHandle)
            }}
            '''

            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-Command",
                    script
                ],
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            time.sleep(0.4)

            return True

        except Exception as e:

            print(
                "BROWSER FOCUS ERROR:",
                e
            )

            return False

    # ========================================================
    # CLOSE BROWSER TAB
    # ========================================================

    def close_browser_tab(
        self,
        tab_name
    ):

        process = self.get_browser_process()

        if not process:

            return False

        # Firefox has different tab search behavior.
        # Chrome / Edge / Brave use Ctrl+Shift+A.
        if process == "firefox.exe":

            # Firefox's tab search shortcut can vary,
            # so use Ctrl+L as a safe fallback and
            # search browser history/current tabs manually
            # is not reliable.
            return False

        if not self.focus_browser(
            process
        ):

            return False

        time.sleep(0.3)

        try:

            # Chrome / Edge / Brave:
            # Ctrl + Shift + A = Search Tabs
            self.hotkey(
                "ctrl",
                "shift",
                "a"
            )

            time.sleep(0.8)

            # Type the tab name
            self.type_text(
                tab_name
            )

            time.sleep(0.8)

            # Select result
            self.press_key(
                "enter"
            )

            time.sleep(0.7)

            # Close selected tab
            self.hotkey(
                "ctrl",
                "w"
            )

            return True

        except Exception as e:

            print(
                "TAB CLOSE ERROR:",
                e
            )

            return False

    # ========================================================
    # KEYBOARD HELPERS
    # ========================================================

    def key_code(
        self,
        key
    ):

        mapping = {

            "ctrl": 0x11,
            "shift": 0x10,
            "alt": 0x12,
            "enter": 0x0D,
            "tab": 0x09,
            "esc": 0x1B,
            "a": 0x41,
            "w": 0x57
        }

        return mapping.get(
            key.lower()
        )

    def press_key(
        self,
        key
    ):

        code = self.key_code(
            key
        )

        if code is None:
            return

        ctypes.windll.user32.keybd_event(
            code,
            0,
            0,
            0
        )

        ctypes.windll.user32.keybd_event(
            code,
            0,
            2,
            0
        )

    def hotkey(
        self,
        *keys
    ):

        codes = [
            self.key_code(k)
            for k in keys
        ]

        codes = [
            c for c in codes
            if c is not None
        ]

        for code in codes:

            ctypes.windll.user32.keybd_event(
                code,
                0,
                0,
                0
            )

        for code in reversed(codes):

            ctypes.windll.user32.keybd_event(
                code,
                0,
                2,
                0
            )

    def type_text(
        self,
        text
    ):

        # Clipboard method avoids manually mapping
        # every keyboard character.

        try:

            import tkinter as _tk

            temp = _tk.Tk()
            temp.withdraw()

            temp.clipboard_clear()
            temp.clipboard_append(
                text
            )

            temp.update()

            self.hotkey(
                "ctrl",
                "v"
            )

            time.sleep(0.1)

            temp.destroy()

        except Exception as e:

            print(
                "TYPE ERROR:",
                e
            )

    # ========================================================
    # GOOGLE SEARCH
    # ========================================================

    def google_search(
        self,
        query,
        engine="google"
    ):

        encoded = query.replace(
            " ",
            "+"
        )

        if engine == "youtube":

            url = (
                "https://www.youtube.com/results?search_query="
                + encoded
            )

        elif engine == "github":

            url = (
                "https://github.com/search?q="
                + encoded
            )

        elif engine == "wikipedia":

            url = (
                "https://en.wikipedia.org/wiki/Special:Search?search="
                + encoded
            )

        else:

            url = (
                "https://www.google.com/search?q="
                + encoded
            )

        webbrowser.open(
            url
        )

    # ========================================================
    # MEDIA
    # ========================================================

    def media_key(
        self,
        action
    ):

        keys = {

            "next": 0xB0,
            "previous": 0xB1,
            "stop": 0xB2,
            "play": 0xB3,
            "pause": 0xB3,
            "mute": 0xAD
        }

        if action not in keys:
            return

        key = keys[action]

        try:

            ctypes.windll.user32.keybd_event(
                key,
                0,
                0,
                0
            )

            ctypes.windll.user32.keybd_event(
                key,
                0,
                2,
                0
            )

        except:
            pass

    # ========================================================
    # TIMER
    # ========================================================

    def timer(
        self,
        minutes
    ):

        self.respond(
            f"Timer set for {minutes} minutes."
        )

        time.sleep(
            minutes * 60
        )

        if self.running:

            self.respond(
                f"Your {minutes} minute timer is complete."
            )

    # ========================================================
    # NUMBER PARSER
    # ========================================================

    def get_number(
        self,
        text
    ):

        numbers = re.findall(
            r"\d+",
            text
        )

        if numbers:

            return int(
                numbers[0]
            )

        words = {

            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "fifteen": 15,
            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "fifty": 50,
            "sixty": 60
        }

        for word, value in words.items():

            if word in text:

                return value

        return None

    # ========================================================
    # COMMAND HANDLER
    # ========================================================

    def handle_command(
        self,
        command
    ):

        command = self.normalize(
            command
        ).strip()

        print(
            "COMMAND:",
            command
        )

        # ----------------------------------------------------
        # STOP AIR
        # ----------------------------------------------------

        if command in [
            "stop listening",
            "pause listening",
            "go to sleep",
            "cancel",
            "cancel command"
        ]:

            self.stop_listening()

            return

        # ----------------------------------------------------
        # TIME
        # ----------------------------------------------------

        if (
            "what time" in command
            or "time is it" in command
            or command == "time"
        ):

            now = datetime.datetime.now().strftime(
                "%I:%M %p"
            )

            self.respond(
                f"The time is {now}."
            )

            return

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        if (
            "what date" in command
            or "what day is it" in command
        ):

            today = datetime.datetime.now().strftime(
                "%A, %d %B %Y"
            )

            self.respond(
                f"Today is {today}."
            )

            return

        # ----------------------------------------------------
        # TIMER
        # ----------------------------------------------------

        if "timer" in command:

            number = self.get_number(
                command
            )

            if number:

                threading.Thread(
                    target=self.timer,
                    args=(number,),
                    daemon=True
                ).start()

            else:

                self.respond(
                    "Tell me how many minutes."
                )

            return

        # ----------------------------------------------------
        # CLOSE TAB
        # ----------------------------------------------------

        tab_match = re.search(
            r"^(?:close|exit|quit|kill|stop)"
            r"\s+(.+?)"
            r"\s+(?:browser\s+)?tab$",
            command
        )

        if tab_match:

            tab_name = tab_match.group(1).strip()

            self.respond(
                f"Closing the {tab_name} tab."
            )

            success = self.close_browser_tab(
                tab_name
            )

            if not success:

                self.respond(
                    f"I couldn't find the {tab_name} tab."
                )

            return

        # Also:
        # "close tab wikipedia"
        tab_match = re.search(
            r"^(?:close|exit|quit)"
            r"\s+(?:tab\s+)(.+)$",
            command
        )

        if tab_match:

            tab_name = tab_match.group(1).strip()

            self.respond(
                f"Closing the {tab_name} tab."
            )

            if not self.close_browser_tab(
                tab_name
            ):

                self.respond(
                    f"I couldn't find the {tab_name} tab."
                )

            return

        # ----------------------------------------------------
        # SEARCH YOUTUBE
        # ----------------------------------------------------

        match = re.search(
            r"(?:search|find)"
            r"\s+youtube"
            r"\s+(?:for\s+)?(.+)",
            command
        )

        if match:

            query = match.group(1)

            self.respond(
                f"Searching YouTube for {query}."
            )

            self.google_search(
                query,
                "youtube"
            )

            return

        # ----------------------------------------------------
        # SEARCH GITHUB
        # ----------------------------------------------------

        match = re.search(
            r"(?:search|find)"
            r"\s+github"
            r"\s+(?:for\s+)?(.+)",
            command
        )

        if match:

            query = match.group(1)

            self.respond(
                f"Searching GitHub for {query}."
            )

            self.google_search(
                query,
                "github"
            )

            return

        # ----------------------------------------------------
        # SEARCH GOOGLE / WEB
        # ----------------------------------------------------

        match = re.search(
            r"^(?:search|find|look up)"
            r"(?:\s+(?:google|the web))?"
            r"(?:\s+for)?\s+(.+)$",
            command
        )

        if match:

            query = match.group(1).strip()

            if query:

                self.respond(
                    f"Searching for {query}."
                )

                self.google_search(
                    query
                )

                return

        # ----------------------------------------------------
        # REDIRECT
        # ----------------------------------------------------

        match = re.search(
            r"^(?:redirect me to|take me to|"
            r"go to|bring me to)\s+(.+)$",
            command
        )

        if match:

            target = match.group(1).strip()

            if self.open_website(
                target
            ):

                self.respond(
                    f"Redirecting you to {target}."
                )

                return

            if self.find_and_launch(
                target
            ):

                return

            if (
                target.startswith("http")
                or re.match(
                    r"^[\w.-]+\.[a-z]{2,}",
                    target
                )
            ):

                url = target

                if not url.startswith(
                    "http"
                ):

                    url = "https://" + url

                webbrowser.open(url)

                self.respond(
                    f"Redirecting you to {target}."
                )

                return

            self.respond(
                f"I couldn't find {target}."
            )

            return

        # ----------------------------------------------------
        # CURRENT WINDOW
        # ----------------------------------------------------

        if command in [
            "close",
            "close this",
            "close this window",
            "close current window",
            "close window",
            "exit this"
        ]:

            self.hotkey(
                "alt",
                "f4"
            )

            return

        # ----------------------------------------------------
        # CLOSE APPLICATION
        # ----------------------------------------------------

        match = re.search(
            r"^(?:close|exit|quit|terminate|kill)"
            r"\s+(.+)$",
            command
        )

        if match:

            target = match.group(1).strip()

            if target in [
                "music",
                "song",
                "media"
            ]:

                self.media_key(
                    "stop"
                )

                self.respond(
                    "Media stopped."
                )

                return

            if self.close_app(
                target
            ):

                self.respond(
                    f"Closing {target}."
                )

            else:

                self.respond(
                    f"I couldn't find {target} running."
                )

            return

        # ----------------------------------------------------
        # STOP MEDIA
        # ----------------------------------------------------

        if command in [
            "stop music",
            "stop song",
            "stop media"
        ]:

            self.media_key(
                "stop"
            )

            self.respond(
                "Media stopped."
            )

            return

        # ----------------------------------------------------
        # PAUSE
        # ----------------------------------------------------

        if command in [
            "pause",
            "pause music"
        ]:

            self.media_key(
                "pause"
            )

            self.respond(
                "Paused."
            )

            return

        # ----------------------------------------------------
        # PLAY
        # ----------------------------------------------------

        if command in [
            "play",
            "play music",
            "resume",
            "resume music"
        ]:

            self.media_key(
                "play"
            )

            self.respond(
                "Resuming media."
            )

            return

        # ----------------------------------------------------
        # NEXT
        # ----------------------------------------------------

        if command in [
            "next song",
            "next track"
        ]:

            self.media_key(
                "next"
            )

            self.respond(
                "Next track."
            )

            return

        # ----------------------------------------------------
        # PREVIOUS
        # ----------------------------------------------------

        if command in [
            "previous song",
            "previous track"
        ]:

            self.media_key(
                "previous"
            )

            self.respond(
                "Previous track."
            )

            return

        # ----------------------------------------------------
        # MUTE
        # ----------------------------------------------------

        if command == "mute":

            self.media_key(
                "mute"
            )

            self.respond(
                "Muted."
            )

            return

        # ----------------------------------------------------
        # OPEN FOLDER
        # ----------------------------------------------------

        match = re.search(
            r"^(?:open|show)\s+"
            r"(?:my\s+)?"
            r"(downloads|documents|pictures|"
            r"videos|music|desktop|this pc|"
            r"my computer|drives|my files)$",
            command
        )

        if match:

            folder = match.group(1)

            if self.open_folder(
                folder
            ):

                self.respond(
                    f"Opening {folder}."
                )

            else:

                self.respond(
                    f"I couldn't open {folder}."
                )

            return

        # ----------------------------------------------------
        # DRIVE
        # ----------------------------------------------------

        match = re.search(
            r"^(?:open|show)"
            r"\s+([a-z])\s+drive$",
            command
        )

        if match:

            letter = match.group(1).upper()

            path = letter + ":\\"

            if os.path.exists(path):

                os.startfile(path)

                self.respond(
                    f"Opening {letter} drive."
                )

            else:

                self.respond(
                    f"{letter} drive was not found."
                )

            return

        # ----------------------------------------------------
        # OPEN ANYTHING
        # ----------------------------------------------------

        target = None

        for word in sorted(
            OPEN_WORDS,
            key=len,
            reverse=True
        ):

            if command.startswith(
                word + " "
            ):

                target = command[
                    len(word):
                ].strip()

                break

        if target:

            target = re.sub(
                r"^(my|the)\s+",
                "",
                target
            )

            target = re.sub(
                r"\s+(please|for me)$",
                "",
                target
            ).strip()

            # Website
            if self.open_website(
                target
            ):

                self.respond(
                    f"Opening {target}."
                )

                return

            # Local application
            if self.find_and_launch(
                target
            ):

                return

            # URL
            if (
                target.startswith("http")
                or re.match(
                    r"^[\w.-]+\.[a-z]{2,}",
                    target
                )
            ):

                url = target

                if not url.startswith(
                    "http"
                ):

                    url = "https://" + url

                webbrowser.open(url)

                self.respond(
                    f"Opening {target}."
                )

                return

            self.respond(
                f"I couldn't find {target}."
            )

            return

        # ----------------------------------------------------
        # DIRECT WEBSITE
        # ----------------------------------------------------

        if self.open_website(
            command
        ):

            self.respond(
                f"Opening {command}."
            )

            return

        # ----------------------------------------------------
        # UNKNOWN
        # ----------------------------------------------------

        self.respond(
            "I don't know that command yet."
        )

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):

        self.running = False
        self.listening_enabled = False
        self.recording = False

        try:
            sd.stop()
        except:
            pass

        try:
            self.engine.stop()
        except:
            pass

        self.save_json(
            MEMORY_FILE,
            self.app_memory
        )

        self.save_json(
            SETTINGS_FILE,
            self.settings
        )

        try:
            self.root.destroy()
        except:
            pass

    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        self.root.mainloop()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    air = GloxAir()

    air.run()