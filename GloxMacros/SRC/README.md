# GLOX Macro — Source

**GLOX Macro** is a lightweight mouse and keyboard macro recorder built with **Python, PySide6, and pynput**.

This folder contains the **source code version** of GLOX Macro for developers who want to inspect, modify, run, or build the application themselves.

---

## 📂 Source Contents

| File               | Description                                         |
| ------------------ | --------------------------------------------------- |
| `gloxmacros.py`    | Main GLOX Macro application source code             |
| `requirements.txt` | Python dependencies required to run the application |

---

## ✨ Features

| Feature                         | Description                                                    |
| ------------------------------- | -------------------------------------------------------------- |
| 🎯 **3 Macro Slots**            | Record and store up to three independent macros                |
| 🖱️ **Mouse Recording**         | Captures mouse movement, clicks, and scrolling                 |
| ⌨️ **Keyboard Recording**       | Captures keyboard press and release events                     |
| 🔁 **Macro Playback**           | Replays recorded actions while preserving their timing         |
| 💾 **Persistent Configuration** | Macro data and settings can be saved locally                   |
| 🎨 **Multiple Themes**          | Obsidian, Graphite, Espresso, Slate, Midnight, and Pearl Glass |
| 🪟 **Compact UI**               | Small, frameless, translucent desktop interface                |
| 📌 **Always on Top**            | Keeps the widget accessible above other windows                |
| 🖱️ **Drag & Move**             | Easily reposition the widget on the desktop                    |
| ⚙️ **Custom Opacity**           | Supports multiple transparency levels                          |

---

## 🛠️ Requirements

Make sure you have **Python 3.10+** installed.

Install the required dependencies using:

```bash
pip install -r requirements.txt
```

The project primarily uses:

* **Python**
* **PySide6**
* **pynput**

---

## ▶️ Running From Source

Open a terminal inside the `SRC` directory and run:

```bash
python gloxmacros.py
```

The GLOX Macro widget should launch directly from the source code.

---

## 📁 Folder Structure

```text
SRC/
│
├── gloxmacros.py
├── requirements.txt
└── README.md
```

---

## 🎮 Basic Usage

### Record a Macro

1. Launch `gloxmacros.py`.
2. Select one of the available macro slots.
3. Choose **Record Macro**.
4. Perform the mouse and keyboard actions you want to record.
5. Stop the recording.
6. The macro is stored in the selected slot.

### Replay a Macro

Simply **left-click a populated macro slot** to replay its recorded actions.

### Manage a Macro

**Right-click** a macro slot to access the available macro controls.

---

## 🎨 Themes

GLOX Macro includes several built-in themes:

| Theme       | Style       |
| ----------- | ----------- |
| Obsidian    | Dark glass  |
| Graphite    | Dark grey   |
| Espresso    | Warm dark   |
| Slate       | Cool dark   |
| Midnight    | Deep dark   |
| Pearl Glass | Light glass |

---

## ⚙️ Configuration

GLOX Macro stores its local configuration in:

```text
~/.glox_macro.json
```

This allows settings and saved macro data to persist between launches.

---

## 🧑‍💻 Development

The source is intentionally kept lightweight and organized around the core macro recording and playback system.

The main components include:

```text
MacroRecorder
    ↓
Captures mouse + keyboard events
    ↓
Stores recorded event data
    ↓
MacroPlayer
    ↓
Replays events with recorded timing
```

You are free to inspect and modify the source for your own development, learning, experimentation, or legitimate automation projects.

---

## ⚠️ Usage Warning

GLOX Macro is an automation utility and should be used responsibly.

Automated mouse and keyboard input may be restricted by certain **games, websites, applications, or online services**. Always check the rules and Terms of Service of the software or platform where you intend to use it.

Do not use GLOX Macro for cheating, unauthorized automation, abuse, security bypasses, or activities that violate third-party rules.

You are responsible for how you use and modify this source code.

---

## 📜 License

Refer to the main GLOX Macro repository for the project's licensing information.

---

<p align="center">

**GLOX Macro — Source**
*Built with Python • PySide6 • pynput*

</p>
