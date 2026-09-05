# GLOX SNAP — Source

### Lightweight Screenshot Utility

This directory contains the **source code** for GLOX SNAP, a lightweight desktop screenshot utility built with **Python and PySide6**.

GLOX SNAP provides full-screen, region, and window capture with automatic clipboard copying, PNG saving, capture delays, themes, opacity controls, and a compact floating desktop interface.

---

## 📂 Source Structure

```text
GloxWidgets/
└── GloxSnap/
    └── SRC/
        ├── gloxsnap.py
        ├── requirements.txt
        └── README.md
```

| File               | Purpose                                                          |
| ------------------ | ---------------------------------------------------------------- |
| `gloxsnap.py`      | Main GLOX SNAP application source code.                          |
| `requirements.txt` | Python dependencies required to run the application from source. |
| `README.md`        | Documentation for the source version of GLOX SNAP.               |

---

## ✨ Features

| Feature                        | Description                                                          |
| ------------------------------ | -------------------------------------------------------------------- |
| 🖥️ **Full Screen Capture**    | Captures the entire primary display.                                 |
| 🎯 **Region Capture**          | Interactive rectangular region selection.                            |
| 🪟 **Window Capture**          | Captures the currently focused application window.                   |
| 📋 **Clipboard Copy**          | Automatically copies screenshots to the system clipboard.            |
| 💾 **Automatic PNG Save**      | Saves captured screenshots automatically as PNG files.               |
| 📁 **Custom Folder**           | Allows users to select a custom screenshot directory.                |
| 💿 **Save As**                 | Manually saves the latest screenshot to a chosen location.           |
| ⏱️ **Capture Delay**           | Supports 0, 3, and 5-second delays.                                  |
| 🎨 **Multiple Themes**         | Includes six built-in themes.                                        |
| 🌫️ **Opacity Control**        | Supports multiple widget opacity levels.                             |
| 🖱️ **Draggable Widget**       | Floating widget can be repositioned around the desktop.              |
| 📌 **Always on Top**           | Keeps the widget accessible above other windows.                     |
| 🖱️ **Context Menu**           | Right-click provides access to settings and utility options.         |
| 📐 **Live Dimensions**         | Displays region width × height during selection.                     |
| ⎋ **ESC Cancel**               | ESC cancels an active region selection.                              |
| ⚡ **Lightweight Architecture** | Uses a compact single-file implementation with minimal dependencies. |

---

## 🛠️ Technologies

| Technology          | Usage                                                        |
| ------------------- | ------------------------------------------------------------ |
| **Python**          | Application logic and functionality                          |
| **PySide6**         | GUI framework                                                |
| **Qt**              | Window management, events, painting, and desktop integration |
| **QPainter**        | Custom widget rendering                                      |
| **QPixmap**         | Screenshot image handling                                    |
| **QGuiApplication** | Display and screen interaction                               |
| **QFileDialog**     | File and folder selection                                    |
| **QMenu**           | Context menu functionality                                   |

---

## 📦 Requirements

The source version requires:

* **Python 3.x**
* **PySide6**

All Python dependencies are listed in:

```text
requirements.txt
```

---

## 🚀 Setup

Open a terminal inside the `SRC` directory.

Install the dependencies:

```bash
pip install -r requirements.txt
```

Then run GLOX SNAP:

```bash
python gloxsnap.py
```

---

## 🖥️ Running From Source

The application is designed as a standalone Python source file.

```text
requirements.txt
       ↓
Install dependencies
       ↓
gloxsnap.py
       ↓
GLOX SNAP
```

No external service or online account is required for the core screenshot functionality.

---

## 📸 Capture Modes

### Full Screen

Captures the entire primary display.

### Region

Select a rectangular area of the screen by dragging the mouse.

The selector displays the current:

```text
WIDTH × HEIGHT
```

Press `ESC` to cancel the selection.

### Window

Attempts to capture the currently focused application window.

---

## ⚙️ Available Settings

Right-click the GLOX SNAP widget to open the context menu.

### Capture Delay

```text
No Delay
3 Seconds
5 Seconds
```

### Themes

```text
Obsidian
Graphite
Charcoal
Espresso
Slate
Midnight
```

### Opacity

```text
100%
80%
60%
50%
```

### File Options

```text
Screenshot Folder...
Save Last Screenshot As...
```

---

## 📂 Default Screenshot Directory

Unless changed by the user, screenshots are stored in:

```text
Pictures/
└── GLOX Screenshots/
```

Files are automatically named using:

```text
GLOX_Snap_YYYYMMDD_HHMMSS.png
```

---

## 🧩 Code Design

GLOX SNAP is intentionally implemented as a compact desktop utility.

The source primarily consists of two components:

### `RegionSelector`

Responsible for:

* Screen overlay
* Mouse-based selection
* Selection rectangle
* Dimension display
* ESC cancellation
* Region coordinate calculation

### `GloxSnap`

Responsible for:

* Main widget
* Screenshot capture
* Window capture
* Clipboard handling
* Automatic saving
* Save dialogs
* Folder selection
* Themes
* Opacity
* Delay functionality
* Context menu
* Custom UI rendering
* Widget movement

This keeps the project easy to understand, modify, and experiment with.

---

## 🎨 GLOX UI Philosophy

The source follows the GLOX Widgets design philosophy:

```text
LIGHTWEIGHT
     +
MINIMAL
     +
PRACTICAL
     +
POLISHED
```

The interface uses a custom-painted PySide6 widget rather than relying entirely on standard GUI controls.

This allows the project to maintain:

* Consistent rounded geometry
* Custom colors
* Theme switching
* Compact dimensions
* Custom typography
* Frameless presentation
* GLOX visual identity

---

## 🔧 Customization

Because the project is provided as Python source code, developers can modify:

* Widget dimensions
* Themes
* Colors
* Fonts
* Capture behavior
* Screenshot naming
* Default save directory
* Delay options
* Opacity levels
* UI layout
* Context menu options

The primary UI and behavior can be customized directly inside:

```text
gloxsnap.py
```

---

## 📚 Educational Use

The source can also serve as a learning example for:

* PySide6 GUI development
* Custom `QPainter` interfaces
* Mouse event handling
* Screen capture with Qt
* Multi-monitor screen interaction
* Clipboard integration
* File dialogs
* Context menus
* Transparent overlays
* Frameless desktop widgets
* Basic desktop application architecture

---

## 🧩 GLOX Widgets

GLOX SNAP is part of the **GLOX Widgets** ecosystem — a collection of lightweight desktop utilities focused on useful functionality and polished interfaces.

The source is structured to remain accessible for developers who want to study, modify, experiment with, or build upon the project.

---

## ⚠️ Responsible Use

GLOX SNAP is intended **only for legitimate personal, educational, development, demonstration, and teaching purposes**.

Users are responsible for ensuring that their use of the software complies with applicable laws, regulations, privacy requirements, copyright restrictions, software licenses, and the rights of other individuals.

**Do not use GLOX SNAP to capture, distribute, or misuse confidential, private, copyrighted, restricted, or otherwise unauthorized content.**

Use the source and resulting application responsibly and only for purposes you are authorized to perform.

---

## 👨‍💻 Credits

### GLOX Industries

**AvgLucer | Gaurav W**
**Founder & CEO — GLOX Industries**

GLOX SNAP is designed and developed as part of the **GLOX Widgets** ecosystem.

---

<div align="center">

### GLOX SNAP — SOURCE

**Capture. Save. Done.**

**AvgLucer | Gaurav W**
**Founder & CEO — GLOX Industries**

</div>
