# GLOX SNAP


<p align="center">
  <img src="assets/glox_snap.png" alt="GLOX SNAP" width="700">
</p>

### Lightweight Screenshot Utility for Windows

**GLOX SNAP** is a lightweight, fast, and minimal desktop screenshot utility built with **Python and PySide6**.

Capture your **entire screen, a selected region, or an active window**, instantly copy screenshots to your clipboard, automatically save them as PNG files, and customize the widget through themes, opacity, delays, and other options.

Designed to stay **simple, lightweight, and distraction-free**.

---

## ✨ Features

| Feature                          | Description                                                                       |
| -------------------------------- | --------------------------------------------------------------------------------- |
| 🖥️ **Full Screen Capture**      | Instantly capture the entire primary display.                                     |
| 🎯 **Region Capture**            | Select any area of the screen using an interactive selection overlay.             |
| 🪟 **Window Capture**            | Capture the currently focused application window.                                 |
| 📋 **Clipboard Copy**            | Automatically copies every captured screenshot directly to the system clipboard.  |
| 💾 **Automatic Saving**          | Screenshots are automatically saved as PNG files.                                 |
| 📁 **Custom Screenshot Folder**  | Choose a custom folder where screenshots should be stored.                        |
| 💿 **Save As**                   | Manually save the latest screenshot to any location using a standard file dialog. |
| ⏱️ **Capture Delay**             | Supports **No Delay, 3-second, and 5-second** capture delays.                     |
| 🎨 **Multiple Themes**           | Includes **Obsidian, Graphite, Charcoal, Espresso, Slate, and Midnight** themes.  |
| 🔳 **Opacity Control**           | Adjust widget opacity between **100%, 80%, 60%, and 50%**.                        |
| 🖱️ **Draggable Widget**         | Move the floating GLOX SNAP widget anywhere on the desktop.                       |
| 🖱️ **Right-Click Menu**         | Access settings and utility options through the context menu.                     |
| ⌨️ **ESC Region Cancel**         | Cancel region selection instantly using the `ESC` key.                            |
| 📐 **Live Selection Dimensions** | Displays the selected region's width and height while capturing.                  |
| 🌙 **Frameless UI**              | Clean floating interface without unnecessary operating-system window chrome.      |
| 📌 **Always on Top**             | Keeps the screenshot widget accessible above other applications.                  |
| ⚡ **Lightweight**                | Built to perform screenshot operations without unnecessary background features.   |
| 🧩 **Single-Utility Design**     | Focused specifically on quick and convenient screenshot capture.                  |

---

## 🎨 UI & Design

GLOX SNAP follows the **GLOX Widgets** design philosophy:

* Minimal desktop interface
* Rounded UI components
* Dark premium aesthetic
* Glassmorphism-inspired visual language
* Subtle shadows and depth
* Accent-based theming
* Compact floating widget
* Clean typography
* Distraction-free controls

The interface is intentionally designed to remain **small, accessible, and unobtrusive** while working on the desktop.

---

## 🛠️ Technology

GLOX SNAP is built using:

| Technology          | Purpose                                                     |
| ------------------- | ----------------------------------------------------------- |
| **Python**          | Core application logic                                      |
| **PySide6**         | Desktop GUI and rendering                                   |
| **Qt**              | Window management, painting, events, and system integration |
| **QGuiApplication** | Screen and display interaction                              |
| **QPixmap**         | Screenshot image handling                                   |
| **QFileDialog**     | Save and folder selection                                   |
| **QMenu**           | Context menu and settings                                   |
| **QPainter**        | Custom widget rendering                                     |

---

## 📦 Project Structure

```text
GloxSnap/
│
├── glox_snap.py
├── requirements.txt
├── README.md
├── DOWNLOAD.md
│
└── assets/
    └── ...
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/AvgLucer/GloxWidgets.git
```

Navigate to the GLOX SNAP directory:

```bash
cd GloxWidgets/GloxSnap
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python glox_snap.py
```

---

## 📥 Download

For the latest compiled release and downloadable version of **GLOX SNAP**, see:

👉 **[DOWNLOAD.md](DOWNLOAD.md)**

The download page contains the available packaged version and installation information.

---

## 🖱️ How to Use

### Full Screen

Click:

```text
FULL SCREEN
```

GLOX SNAP captures the entire primary display.

### Region

Click:

```text
REGION
```

Then drag across the area you want to capture.

The selected dimensions are displayed while selecting.

Press:

```text
ESC
```

to cancel the selection.

### Window

Click:

```text
WINDOW
```

GLOX SNAP attempts to capture the currently focused application window.

### Save

Click:

```text
SAVE LAST SCREENSHOT
```

to manually save the most recent capture.

---

## ⚙️ Options

Right-click anywhere on the GLOX SNAP widget to open the settings menu.

Available options include:

### Delay

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

Additional options allow you to:

* Change the screenshot folder
* Save the latest screenshot manually
* Exit the application

---

## 📸 Screenshot Workflow

GLOX SNAP follows a simple workflow:

```text
Select Capture Mode
        ↓
Capture Screen
        ↓
Copy to Clipboard
        ↓
Automatically Save PNG
        ↓
Continue Working
```

No complicated editor or unnecessary workflow is required.

---

## 🧩 Part of GLOX Widgets

**GLOX SNAP** is part of the broader **GLOX Widgets** ecosystem — a collection of lightweight desktop utilities designed to provide useful functionality through compact, polished interfaces.

The project follows the same principles used throughout the GLOX ecosystem:

> **Lightweight • Useful • Minimal • Practical**

---

## 🛡️ Disclaimer & Responsible Use

GLOX SNAP is provided **for personal, educational, development, testing, demonstration, and teaching purposes**.

Users are responsible for how they use the software and for ensuring that their usage complies with applicable laws, regulations, software licenses, privacy requirements, and the rights of other individuals.

**Do not use GLOX SNAP to capture, distribute, or misuse confidential, private, copyrighted, restricted, or otherwise unauthorized content.**

The software is intended to be used responsibly and only for legitimate purposes.

---

## 📄 License

Please refer to the repository's license and accompanying project documentation for the applicable terms of use.

---

## 👨‍💻 Credits

### GLOX Industries

**AvgLucer | Gaurav W**
**Founder & CEO — GLOX Industries**

GLOX SNAP is designed and developed as part of the **GLOX Widgets** ecosystem.

---

<div align="center">

### GLOX SNAP

**Capture. Save. Done.**

Made with Python & PySide6.

**AvgLucer | Gaurav W**
**Founder & CEO — GLOX Industries**

</div>
