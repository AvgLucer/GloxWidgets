# ============================================================
# GLOX PROMPTS
# AI Prompt Generator Widget
#
# Requirements:
#   pip install PySide6 requests python-dotenv
#
# .env:
#   OPENROUTER_API_KEY=your_key_here
#
# ============================================================

import os
import sys
import json
import requests

from pathlib import Path

from dotenv import load_dotenv, set_key, dotenv_values

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QComboBox,
    QSlider,
    QDialog,
    QLineEdit,
    QMessageBox,
    QFrame,
    QColorDialog,
    QSizePolicy,
)


# ============================================================
# PATHS
# ============================================================
if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
else:
    APP_DIR = Path(__file__).resolve().parent

ENV_FILE = APP_DIR / ".env"
CONFIG_FILE = APP_DIR / "gloxprompts_config.json"


# ============================================================
# ENV
# ============================================================

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


# ============================================================
# THEMES
# ============================================================

THEMES = {
    "Obsidian": {
        "window": "#101114",
        "panel": "#17191e",
        "panel2": "#1d2026",
        "text": "#f1f1f1",
        "muted": "#999da7",
        "accent": "#8d96ff",
        "border": "#2a2e37",
        "input": "#111318",
    },

    "Graphite": {
        "window": "#18191b",
        "panel": "#222427",
        "panel2": "#292c30",
        "text": "#f3f3f3",
        "muted": "#a5a7aa",
        "accent": "#c2c4c7",
        "border": "#383b40",
        "input": "#191b1e",
    },

    "Charcoal": {
        "window": "#151515",
        "panel": "#202020",
        "panel2": "#292929",
        "text": "#eeeeee",
        "muted": "#a0a0a0",
        "accent": "#e0e0e0",
        "border": "#363636",
        "input": "#181818",
    },

    "Espresso": {
        "window": "#17120f",
        "panel": "#241b17",
        "panel2": "#30241e",
        "text": "#f5ebe3",
        "muted": "#b8a69a",
        "accent": "#d8a27c",
        "border": "#49362c",
        "input": "#1b1512",
    },

    "Slate": {
        "window": "#101820",
        "panel": "#18232d",
        "panel2": "#20303c",
        "text": "#edf4f8",
        "muted": "#98aab7",
        "accent": "#70b7df",
        "border": "#2c414f",
        "input": "#121b22",
    },

    "Midnight": {
        "window": "#080b14",
        "panel": "#101525",
        "panel2": "#171e32",
        "text": "#eef1ff",
        "muted": "#9299b4",
        "accent": "#7f91ff",
        "border": "#252e4a",
        "input": "#0b0f1c",
    },

    "Crystal Cream": {
        "window": "#f1eee7",
        "panel": "#faf8f3",
        "panel2": "#e9e5dc",
        "text": "#282621",
        "muted": "#777268",
        "accent": "#75624d",
        "border": "#d7d0c4",
        "input": "#ffffff",
    },

    "Aurora Night": {
        "window": "#0c1113",
        "panel": "#111b1e",
        "panel2": "#182629",
        "text": "#e9f8f4",
        "muted": "#8fa9a3",
        "accent": "#63d7bd",
        "border": "#26413d",
        "input": "#0c1416",
    },

    "Lavender": {
        "window": "#15131c",
        "panel": "#211e2c",
        "panel2": "#2b2739",
        "text": "#f2effc",
        "muted": "#aaa3bc",
        "accent": "#b39aff",
        "border": "#3b3450",
        "input": "#181620",
    },

    "Mono": {
        "window": "#111111",
        "panel": "#1b1b1b",
        "panel2": "#252525",
        "text": "#ffffff",
        "muted": "#999999",
        "accent": "#ffffff",
        "border": "#333333",
        "input": "#141414",
    },
}


# ============================================================
# PROMPT STYLES
# ============================================================

PROMPT_STYLES = {
    "General": """
Create a professional, structured prompt from the user's idea.
Preserve the user's intent while filling in reasonable missing
technical and functional details.
""",

    "Coding": """
Transform the idea into a highly detailed software-development prompt.
Focus on architecture, functionality, implementation requirements,
technology choices, edge cases, error handling, file structure,
security, performance, and expected output.
""",

    "UI / UX": """
Transform the idea into a professional UI/UX design prompt.
Focus heavily on layout, hierarchy, components, interactions,
visual language, responsiveness, accessibility, states, animations,
navigation, and user experience.
""",

    "AI Agent": """
Transform the idea into a detailed AI-agent development prompt.
Define the agent's role, objectives, tools, workflow, reasoning process,
inputs, outputs, constraints, failure handling, and expected behavior.
""",

    "Website": """
Transform the idea into a detailed website-development prompt.
Cover pages, sections, navigation, responsive behavior, visual design,
interactions, frontend architecture, backend requirements, APIs,
accessibility, SEO, performance, and deployment considerations.
""",

    "Data Science": """
Transform the idea into a detailed data-science prompt.
Cover datasets, preprocessing, exploratory analysis, feature engineering,
models, evaluation metrics, visualization, validation, reproducibility,
and expected outputs.
""",

    "Application": """
Transform the idea into a complete application-development prompt.
Cover functionality, architecture, UI, data flow, storage, settings,
security, error handling, edge cases, and deployment.
""",
}


# ============================================================
# CONFIG
# ============================================================

def load_config():
    default = {
        "theme": "Obsidian",
        "opacity": 100,
        "background": "",
    }

    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            default.update(data)

    except Exception:
        pass

    return default


def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass


# ============================================================
# OPENROUTER WORKER
# ============================================================

class APIWorker(QThread):

    finished = Signal(object)
    error = Signal(str)

    def __init__(self, url, headers=None, params=None, json_data=None):
        super().__init__()

        self.url = url
        self.headers = headers or {}
        self.params = params
        self.json_data = json_data

    def run(self):
        try:

            response = requests.get(
                self.url,
                headers=self.headers,
                params=self.params,
                timeout=30,
            ) if self.json_data is None else requests.post(
                self.url,
                headers=self.headers,
                json=self.json_data,
                timeout=120,
            )

            if not response.ok:
                try:
                    data = response.json()
                    message = data.get("error", {}).get(
                        "message",
                        response.text
                    )
                except Exception:
                    message = response.text

                raise Exception(
                    f"HTTP {response.status_code}: {message}"
                )

            self.finished.emit(response.json())

        except Exception as e:
            self.error.emit(str(e))


# ============================================================
# API KEY DIALOG
# ============================================================

class APIKeyDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("OpenRouter API Key")
        self.setModal(True)
        self.setFixedWidth(500)

        self.setStyleSheet("""
            QDialog {
                background: #17191e;
                color: white;
            }

            QLabel {
                color: #eeeeee;
            }

            QLineEdit {
                background: #111318;
                color: white;
                border: 1px solid #343943;
                border-radius: 10px;
                padding: 11px;
            }

            QPushButton {
                background: #252a34;
                color: white;
                border: none;
                border-radius: 9px;
                padding: 10px 16px;
            }

            QPushButton:hover {
                background: #303642;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        title = QLabel("OpenRouter API Key")
        title.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))

        subtitle = QLabel(
            "Enter your OpenRouter API key.\n"
            "It will be stored in the local .env file."
        )
        subtitle.setWordWrap(True)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("sk-or-v1-...")
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)

        existing = os.getenv("OPENROUTER_API_KEY", "")

        if existing:
            self.key_input.setText(existing)

        buttons = QHBoxLayout()

        save = QPushButton("Save Key")
        remove = QPushButton("Remove Key")
        cancel = QPushButton("Cancel")

        save.clicked.connect(self.save_key)
        remove.clicked.connect(self.remove_key)
        cancel.clicked.connect(self.reject)

        buttons.addWidget(remove)
        buttons.addStretch()
        buttons.addWidget(cancel)
        buttons.addWidget(save)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.key_input)
        layout.addLayout(buttons)

    def save_key(self):

        key = self.key_input.text().strip()

        if not key:
            QMessageBox.warning(
                self,
                "Missing Key",
                "Please enter an OpenRouter API key."
            )
            return

        try:

            if not ENV_FILE.exists():
                ENV_FILE.touch()

            set_key(
                str(ENV_FILE),
                "OPENROUTER_API_KEY",
                key
            )

            os.environ["OPENROUTER_API_KEY"] = key

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Could not save the API key:\n\n{e}"
            )

    def remove_key(self):

        try:

            if ENV_FILE.exists():

                values = dotenv_values(ENV_FILE)

                lines = []

                with open(
                    ENV_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:
                    lines = f.readlines()

                with open(
                    ENV_FILE,
                    "w",
                    encoding="utf-8"
                ) as f:

                    for line in lines:

                        if not line.strip().startswith(
                            "OPENROUTER_API_KEY="
                        ):
                            f.write(line)

            os.environ.pop(
                "OPENROUTER_API_KEY",
                None
            )

            self.accept()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Error",
                f"Could not remove the API key:\n\n{e}"
            )


# ============================================================
# MAIN WINDOW
# ============================================================

class GloxPrompt(QWidget):

    def __init__(self):

        super().__init__()

        self.config = load_config()
        self.worker = None

        self.current_theme = self.config.get(
            "theme",
            "Obsidian"
        )

        self.opacity_value = self.config.get(
            "opacity",
            100
        )

        self.custom_background = self.config.get(
            "background",
            ""
        )

        self.setWindowTitle("GloxPrompt")

        self.setMinimumSize(900, 700)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Window
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.drag_position = None

        self.build_ui()
        self.apply_theme()
        self.update_api_status()

        self.load_models()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        self.root = QFrame()
        self.root.setObjectName("Root")

        root_layout = QVBoxLayout(self.root)
        root_layout.setContentsMargins(
            20, 16, 20, 20
        )
        root_layout.setSpacing(12)

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = QHBoxLayout()

        logo = QLabel("GloxPrompt")
        logo.setObjectName("Logo")
        logo.setFont(
            QFont(
                "Segoe UI",
                17,
                QFont.Weight.Bold
            )
        )

        subtitle = QLabel(
            "Turn rough ideas into professional prompts"
        )
        subtitle.setObjectName("Subtitle")

        header.addWidget(logo)
        header.addSpacing(8)
        header.addWidget(subtitle)
        header.addStretch()

        settings_btn = QPushButton("⚙")
        settings_btn.setFixedSize(36, 36)
        settings_btn.clicked.connect(
            self.open_settings
        )

        minimize_btn = QPushButton("—")
        minimize_btn.setFixedSize(36, 36)
        minimize_btn.clicked.connect(
            self.showMinimized
        )

        close_btn = QPushButton("×")
        close_btn.setFixedSize(36, 36)
        close_btn.clicked.connect(
            self.close
        )

        header.addWidget(settings_btn)
        header.addWidget(minimize_btn)
        header.addWidget(close_btn)

        root_layout.addLayout(header)

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        status_row = QHBoxLayout()

        self.api_status = QLabel()
        self.api_status.setObjectName("Status")

        status_row.addWidget(self.api_status)
        status_row.addStretch()

        root_layout.addLayout(status_row)

        # ----------------------------------------------------
        # INPUT LABEL
        # ----------------------------------------------------

        input_label = QLabel("YOUR IDEA")
        input_label.setObjectName("SectionTitle")

        root_layout.addWidget(input_label)

        # ----------------------------------------------------
        # INPUT
        # ----------------------------------------------------

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText(
            "Explain your idea naturally...\n\n"
            "You don't need to structure it. Just describe "
            "what you want to build, what it should do, "
            "how it should look, technologies you prefer, "
            "or anything else you have in mind."
        )

        self.input_box.setMinimumHeight(180)

        root_layout.addWidget(
            self.input_box,
            1
        )

        # ----------------------------------------------------
        # CONTROLS
        # ----------------------------------------------------

        controls = QHBoxLayout()

        style_label = QLabel("Style")
        style_label.setObjectName("ControlLabel")

        self.style_combo = QComboBox()
        self.style_combo.addItems(
            PROMPT_STYLES.keys()
        )
        self.style_combo.setMinimumWidth(150)

        model_label = QLabel("Model")
        model_label.setObjectName("ControlLabel")

        self.model_combo = QComboBox()
        self.model_combo.setMinimumWidth(270)

        controls.addWidget(style_label)
        controls.addWidget(self.style_combo)

        controls.addSpacing(15)

        controls.addWidget(model_label)
        controls.addWidget(self.model_combo)

        controls.addStretch()

        root_layout.addLayout(controls)

        # ----------------------------------------------------
        # GENERATE
        # ----------------------------------------------------

        self.generate_btn = QPushButton(
            "✦  GENERATE PROMPT"
        )

        self.generate_btn.setObjectName(
            "GenerateButton"
        )

        self.generate_btn.setMinimumHeight(46)

        self.generate_btn.clicked.connect(
            self.generate_prompt
        )

        root_layout.addWidget(
            self.generate_btn
        )

        # ----------------------------------------------------
        # OUTPUT LABEL
        # ----------------------------------------------------

        output_header = QHBoxLayout()

        output_label = QLabel(
            "GENERATED PROMPT"
        )

        output_label.setObjectName(
            "SectionTitle"
        )

        output_header.addWidget(
            output_label
        )

        output_header.addStretch()

        copy_btn = QPushButton(
            "Copy"
        )

        clear_btn = QPushButton(
            "Clear"
        )

        copy_btn.clicked.connect(
            self.copy_prompt
        )

        clear_btn.clicked.connect(
            self.clear_prompt
        )

        output_header.addWidget(copy_btn)
        output_header.addWidget(clear_btn)

        root_layout.addLayout(
            output_header
        )

        # ----------------------------------------------------
        # OUTPUT
        # ----------------------------------------------------

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        self.output_box.setPlaceholderText(
            "Your structured professional prompt "
            "will appear here..."
        )

        root_layout.addWidget(
            self.output_box,
            2
        )

        # ----------------------------------------------------
        # FOOTER
        # ----------------------------------------------------

        footer = QLabel(
            "GloxPrompt  •  OpenRouter powered"
        )

        footer.setObjectName(
            "Footer"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        root_layout.addWidget(
            footer
        )

        # ----------------------------------------------------
        # MAIN WINDOW LAYOUT
        # ----------------------------------------------------

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self.root)

    # ========================================================
    # THEME
    # ========================================================

    def apply_theme(self):

        theme = THEMES.get(
            self.current_theme,
            THEMES["Obsidian"]
        )

        if self.custom_background:
            window_color = self.custom_background
        else:
            window_color = theme["window"]

        self.setStyleSheet(f"""

            QWidget {{
                font-family: "Segoe UI";
            }}

            QFrame#Root {{
                background: {window_color};
                border: 1px solid {theme["border"]};
                border-radius: 20px;
            }}

            QLabel {{
                color: {theme["text"]};
            }}

            QLabel#Logo {{
                color: {theme["text"]};
            }}

            QLabel#Subtitle {{
                color: {theme["muted"]};
                font-size: 11px;
            }}

            QLabel#SectionTitle {{
                color: {theme["muted"]};
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
            }}

            QLabel#ControlLabel {{
                color: {theme["muted"]};
                font-size: 11px;
            }}

            QLabel#Status {{
                color: {theme["accent"]};
                font-size: 11px;
            }}

            QLabel#Footer {{
                color: {theme["muted"]};
                font-size: 9px;
            }}

            QTextEdit {{
                background: {theme["input"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 13px;
                padding: 12px;
                font-size: 12px;
                selection-background-color: {theme["accent"]};
            }}

            QComboBox {{
                background: {theme["panel"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 9px;
                padding: 8px 12px;
            }}

            QComboBox:hover {{
                border: 1px solid {theme["accent"]};
            }}

            QComboBox QAbstractItemView {{
                background: {theme["panel"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                selection-background-color: {theme["accent"]};
            }}

            QPushButton {{
                background: {theme["panel"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 9px;
                padding: 8px 13px;
            }}

            QPushButton:hover {{
                background: {theme["panel2"]};
            }}

            QPushButton#GenerateButton {{
                background: {theme["accent"]};
                color: {theme["window"]};
                border: none;
                border-radius: 11px;
                font-weight: bold;
                font-size: 12px;
            }}

            QPushButton#GenerateButton:hover {{
                opacity: 0.9;
            }}

            QScrollBar:vertical {{
                background: transparent;
                width: 7px;
            }}

            QScrollBar::handle:vertical {{
                background: {theme["border"]};
                border-radius: 4px;
            }}
        """)

        self.setWindowOpacity(
            self.opacity_value / 100
        )

    # ========================================================
    # API STATUS
    # ========================================================

    def update_api_status(self):

        key = os.getenv(
            "OPENROUTER_API_KEY",
            ""
        ).strip()

        if key:

            self.api_status.setText(
                "● OpenRouter API connected"
            )

        else:

            self.api_status.setText(
                "○ No OpenRouter API key"
            )

    # ========================================================
    # FETCH MODELS
    # ========================================================

    def load_models(self):

        self.model_combo.clear()

        self.model_combo.addItem(
            "Loading free models..."
        )

        headers = {}

        key = os.getenv(
            "OPENROUTER_API_KEY",
            ""
        ).strip()

        if key:
            headers["Authorization"] = f"Bearer {key}"

        self.worker = APIWorker(
            "https://openrouter.ai/api/v1/models",
            headers=headers
        )

        self.worker.finished.connect(
            self.models_loaded
        )

        self.worker.error.connect(
            self.models_error
        )

        self.worker.start()

    def models_loaded(self, data):

        self.model_combo.clear()

        models = data.get(
            "data",
            []
        )

        free_models = []

        for model in models:

            model_id = model.get(
                "id",
                ""
            )

            pricing = model.get(
                "pricing",
                {}
            )

            prompt_price = str(
                pricing.get("prompt", "")
            )

            completion_price = str(
                pricing.get("completion", "")
            )

            is_free = (
                prompt_price in ("0", "0.0", "0.000000")
                and
                completion_price in ("0", "0.0", "0.000000")
            )

            # OpenRouter often uses :free
            if ":free" in model_id:
                is_free = True

            if is_free:

                name = model.get(
                    "name",
                    model_id
                )

                free_models.append(
                    (
                        name,
                        model_id
                    )
                )

        free_models.sort(
            key=lambda x: x[0].lower()
        )

        if not free_models:

            self.model_combo.addItem(
                "No free models found"
            )

            return

        for name, model_id in free_models:

            self.model_combo.addItem(
                name,
                model_id
            )

        # Prefer Nemotron if available
        for i in range(
            self.model_combo.count()
        ):

            model_id = self.model_combo.itemData(i)

            if model_id and (
                "nemotron" in model_id.lower()
            ):

                self.model_combo.setCurrentIndex(i)
                break

    def models_error(self, message):

        self.model_combo.clear()

        self.model_combo.addItem(
            "Could not load models"
        )

        # Don't block the entire application if
        # the model endpoint temporarily fails.

        self.api_status.setText(
            "● API available • model list unavailable"
        )

    # ========================================================
    # GENERATE PROMPT
    # ========================================================

    def generate_prompt(self):

        idea = self.input_box.toPlainText().strip()

        if not idea:

            QMessageBox.warning(
                self,
                "Empty Idea",
                "Describe your idea first."
            )

            return

        api_key = os.getenv(
            "OPENROUTER_API_KEY",
            ""
        ).strip()

        if not api_key:

            result = QMessageBox.question(
                self,
                "API Key Required",
                "You need an OpenRouter API key "
                "to generate prompts.\n\n"
                "Open API settings now?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No
            )

            if result == QMessageBox.StandardButton.Yes:
                self.open_api_dialog()

            return

        model_id = self.model_combo.currentData()

        if not model_id:

            QMessageBox.warning(
                self,
                "No Model",
                "Please select a valid OpenRouter model."
            )

            return

        style = self.style_combo.currentText()

        style_instruction = PROMPT_STYLES.get(
            style,
            PROMPT_STYLES["General"]
        )

        system_prompt = f"""
You are GloxPrompt, an expert prompt engineer.

Your job is to transform a user's rough, natural-language
idea into a highly professional, structured prompt that
another AI can directly understand and execute.

The user may describe their idea casually, incompletely,
or with poor grammar. Do NOT criticize their writing.

Preserve their original intent.

Improve:
- clarity
- structure
- specificity
- technical precision
- requirements
- constraints
- expected behavior
- edge cases
- output expectations

Do not invent major features that fundamentally change
the user's idea.

You may intelligently infer reasonable implementation
details when necessary.

{style_instruction}

Return ONLY the finished prompt.

Use a clean Markdown structure.

For software-related ideas, prefer sections such as:

# ROLE
# OBJECTIVE
# CONTEXT
# CORE REQUIREMENTS
# FUNCTIONAL REQUIREMENTS
# UI / UX REQUIREMENTS
# TECHNICAL REQUIREMENTS
# DATA / API REQUIREMENTS
# ERROR HANDLING
# SECURITY
# PERFORMANCE
# CONSTRAINTS
# EXPECTED OUTPUT
# ACCEPTANCE CRITERIA

Only include sections that are relevant.

Make the final prompt detailed, professional,
actionable, and ready to paste into another AI.
"""

        user_prompt = f"""
Here is the user's raw idea:

---BEGIN IDEA---

{idea}

---END IDEA---

Transform this into the final professional prompt.
"""

        payload = {
            "model": model_id,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "temperature": 0.35,
        }

        self.generate_btn.setEnabled(False)
        self.generate_btn.setText(
            "✦  GENERATING..."
        )

        self.output_box.setPlainText(
            "Generating your professional prompt..."
        )

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/AvgLucer",
            "X-Title": "GloxPrompt",
        }

        self.worker = APIWorker(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json_data=payload
        )

        self.worker.finished.connect(
            self.prompt_generated
        )

        self.worker.error.connect(
            self.generation_error
        )

        self.worker.start()

    def prompt_generated(self, data):

        try:

            choices = data.get(
                "choices",
                []
            )

            if not choices:
                raise Exception(
                    "The model returned no response."
                )

            message = choices[0].get(
                "message",
                {}
            )

            content = message.get(
                "content",
                ""
            )

            if not content:
                raise Exception(
                    "The model returned an empty prompt."
                )

            self.output_box.setPlainText(
                content.strip()
            )

        except Exception as e:

            self.output_box.clear()

            QMessageBox.critical(
                self,
                "Generation Error",
                str(e)
            )

        finally:

            self.generate_btn.setEnabled(True)
            self.generate_btn.setText(
                "✦  GENERATE PROMPT"
            )

    def generation_error(self, message):

        self.output_box.clear()

        self.generate_btn.setEnabled(True)

        self.generate_btn.setText(
            "✦  GENERATE PROMPT"
        )

        QMessageBox.critical(
            self,
            "OpenRouter Error",
            message
        )

    # ========================================================
    # CLIPBOARD
    # ========================================================

    def copy_prompt(self):

        text = self.output_box.toPlainText().strip()

        if not text:
            return

        QApplication.clipboard().setText(
            text
        )

        self.api_status.setText(
            "● Prompt copied to clipboard"
        )

    def clear_prompt(self):

        self.input_box.clear()
        self.output_box.clear()

    # ========================================================
    # SETTINGS
    # ========================================================

    def open_settings(self):

        dialog = QDialog(self)

        dialog.setWindowTitle(
            "GloxPrompt Settings"
        )

        dialog.setFixedWidth(450)

        theme = THEMES.get(
            self.current_theme,
            THEMES["Obsidian"]
        )

        dialog.setStyleSheet(f"""

            QDialog {{
                background: {theme["window"]};
            }}

            QLabel {{
                color: {theme["text"]};
            }}

            QComboBox {{
                background: {theme["panel"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 8px;
                padding: 8px;
            }}

            QPushButton {{
                background: {theme["panel"]};
                color: {theme["text"]};
                border: 1px solid {theme["border"]};
                border-radius: 8px;
                padding: 9px 13px;
            }}
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(
            22, 22, 22, 22
        )

        title = QLabel(
            "GloxPrompt Settings"
        )

        title.setFont(
            QFont(
                "Segoe UI",
                15,
                QFont.Weight.Bold
            )
        )

        layout.addWidget(title)

        # ----------------------------------------------------
        # API
        # ----------------------------------------------------

        api_btn = QPushButton(
            "OpenRouter API Key"
        )

        api_btn.clicked.connect(
            lambda: (
                dialog.close(),
                self.open_api_dialog()
            )
        )

        layout.addWidget(api_btn)

        # ----------------------------------------------------
        # THEME
        # ----------------------------------------------------

        layout.addWidget(
            QLabel("Theme")
        )

        theme_combo = QComboBox()

        theme_combo.addItems(
            THEMES.keys()
        )

        theme_combo.setCurrentText(
            self.current_theme
        )

        layout.addWidget(
            theme_combo
        )

        # ----------------------------------------------------
        # OPACITY
        # ----------------------------------------------------

        opacity_label = QLabel(
            f"Opacity: {self.opacity_value}%"
        )

        layout.addWidget(
            opacity_label
        )

        opacity_slider = QSlider(
            Qt.Orientation.Horizontal
        )

        opacity_slider.setRange(
            45,
            100
        )

        opacity_slider.setValue(
            self.opacity_value
        )

        opacity_slider.valueChanged.connect(
            lambda value: opacity_label.setText(
                f"Opacity: {value}%"
            )
        )

        layout.addWidget(
            opacity_slider
        )

        # ----------------------------------------------------
        # BACKGROUND
        # ----------------------------------------------------

        bg_btn = QPushButton(
            "Choose Background Color"
        )

        def choose_background():

            color = QColorDialog.getColor(
                QColor(
                    self.custom_background
                    if self.custom_background
                    else theme["window"]
                ),
                dialog,
                "Choose Background"
            )

            if color.isValid():

                self.custom_background = (
                    color.name()
                )

                self.apply_theme()

        bg_btn.clicked.connect(
            choose_background
        )

        layout.addWidget(
            bg_btn
        )

        reset_bg = QPushButton(
            "Reset Background"
        )

        def reset_background():

            self.custom_background = ""

            self.apply_theme()

        reset_bg.clicked.connect(
            reset_background
        )

        layout.addWidget(
            reset_bg
        )

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        layout.addStretch()

        buttons = QHBoxLayout()

        cancel = QPushButton(
            "Cancel"
        )

        save = QPushButton(
            "Save"
        )

        cancel.clicked.connect(
            dialog.reject
        )

        def save_settings():

            self.current_theme = (
                theme_combo.currentText()
            )

            self.opacity_value = (
                opacity_slider.value()
            )

            self.config["theme"] = (
                self.current_theme
            )

            self.config["opacity"] = (
                self.opacity_value
            )

            self.config["background"] = (
                self.custom_background
            )

            save_config(
                self.config
            )

            self.apply_theme()

            dialog.accept()

        save.clicked.connect(
            save_settings
        )

        buttons.addStretch()
        buttons.addWidget(cancel)
        buttons.addWidget(save)

        layout.addLayout(
            buttons
        )

        dialog.exec()

        self.update_api_status()

        self.load_models()

    def open_api_dialog(self):

        dialog = APIKeyDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:

            load_dotenv(
                ENV_FILE,
                override=True
            )

            self.update_api_status()
            self.load_models()

    # ========================================================
    # WINDOW DRAGGING
    # ========================================================

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if (
            event.buttons()
            & Qt.MouseButton.LeftButton
            and self.drag_position
        ):

            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

    def mouseReleaseEvent(self, event):

        self.drag_position = None

    # ========================================================
    # CLOSE
    # ========================================================

    def closeEvent(self, event):

        self.config["theme"] = (
            self.current_theme
        )

        self.config["opacity"] = (
            self.opacity_value
        )

        self.config["background"] = (
            self.custom_background
        )

        save_config(
            self.config
        )

        event.accept()


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(sys.argv)

    app.setApplicationName(
        "GloxPrompt"
    )

    app.setStyle(
        "Fusion"
    )

    window = GloxPrompt()

    window.resize(
        1000,
        780
    )

    # Center
    screen = app.primaryScreen()

    if screen:

        geometry = screen.availableGeometry()

        window.move(
            geometry.center()
            - window.rect().center()
        )

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()