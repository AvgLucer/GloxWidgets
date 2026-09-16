<div align="center">

# Glox Relay — Source

### Source Code • Dependencies • Development

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-GUI-41CD52?style=for-the-badge\&logo=qt\&logoColor=white)
![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Automation-8B5CF6?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-8B5CF6?style=for-the-badge)

</div>

---

<div style="background:#E9D5FF;padding:10px 16px;border-radius:8px;">

## 🌸 About This Folder

</div>

This `SRC` folder contains the source files required to run and understand **Glox Relay**.

```text
GloxWidgets/
└── GloxRelay/
    └── SRC/
        ├── gloxrelay.py
        ├── requirements.txt
        └── README.md
```

---

<div style="background:#D8B4FE;padding:10px 16px;border-radius:8px;">

## 📁 Files

</div>

| File               | Purpose                                         |
| ------------------ | ----------------------------------------------- |
| `gloxrelay.py`     | Main Glox Relay application source code         |
| `requirements.txt` | Python dependencies required by the application |
| `README.md`        | Documentation for the source directory          |

---

<div style="background:#C084FC;padding:10px 16px;border-radius:8px;">

## ⚙️ Requirements

</div>

Glox Relay requires:

| Package       | Purpose                         |
| ------------- | ------------------------------- |
| **PySide6**   | Desktop GUI and interface       |
| **PyAutoGUI** | Keyboard and desktop automation |

Install all dependencies with:

```bash
pip install -r requirements.txt
```

Or individually:

```bash
pip install PySide6 pyautogui
```

---

<div style="background:#A855F7;padding:10px 16px;border-radius:8px;">

## ▶️ Running From SRC

</div>

Open a terminal inside the `SRC` directory:

```bash
cd GloxWidgets/GloxRelay/SRC
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Glox Relay:

```bash
python gloxrelay.py
```

---

<div style="background:#9333EA;padding:10px 16px;border-radius:8px;">

## 🧩 Source Overview

</div>

The main source file contains the complete Glox Relay application, including:

| Component                | Description                                   |
| ------------------------ | --------------------------------------------- |
| **PySide6 UI**           | Builds the Glox Relay desktop interface       |
| **Themes**               | Provides the built-in Glox appearance presets |
| **Destinations**         | Handles supported and custom websites         |
| **Relay Engine**         | Processes the selected destinations           |
| **Clipboard Workflow**   | Copies the entered prompt for relay           |
| **PyAutoGUI Automation** | Performs paste and optional Enter actions     |
| **Configuration**        | Saves user preferences locally                |
| **Custom Websites**      | Allows users to add additional destinations   |
| **Collapse Mode**        | Provides the compact GLOX widget state        |
| **Context Menu**         | Provides quick widget controls                |

---

<div style="background:#7E22CE;padding:10px 16px;border-radius:8px;">

## 📂 Configuration

</div>

Glox Relay stores its local configuration at:

```text
~/.gloxrelay/config.json
```

Configuration may include:

* Selected destinations
* Custom websites
* Theme
* Opacity
* Destination settings

---

<div style="background:#6B21A8;padding:10px 16px;border-radius:8px;">

## 🛠️ Development

</div>

The source is intentionally kept straightforward so that it can also be studied and modified.

You can inspect `gloxrelay.py` to understand:

* PySide6 widget development
* Frameless desktop windows
* GUI event handling
* Browser automation
* Clipboard operations
* Configuration management
* Theme systems
* Custom dialogs
* Desktop widget behavior

---

<div style="background:#166534;padding:10px 16px;border-radius:8px;color:white;">

## 💚 Credits

</div>

**AvgLucer | Gaurav W**
**Founder & CEO at Glox Industries**

> Building Softwares With a New Vision.

---

<div style="background:#DC2626;padding:10px 16px;border-radius:8px;color:white;">

## 🚨 Educational & Usage Notice

</div>

This source code is provided for **user, educational, teaching, learning, experimentation, and understanding purposes**.

It is intended to help users study concepts related to Python, PySide6, desktop application development, browser automation, clipboard workflows, and GUI programming.

**Do not claim this project or its original work as your own.**

If you use, modify, study, demonstrate, or redistribute the source code, retain appropriate attribution and license information.

---

<div style="background:#E5E7EB;padding:10px 16px;border-radius:8px;">

## 📄 License

</div>

Glox Relay is released under the **MIT License**.

See the project's `LICENSE` file for the complete license text.

---

<div align="center">

### GLOX INDUSTRIES

**Building Softwares With a New Vision**

<br>

**AvgLucer | Gaurav W — Founder & CEO**

</div>
