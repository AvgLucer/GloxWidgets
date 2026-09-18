# GloxBar — Source

GloxBar is a lightweight floating quick-access bar built with **Python + PySide6** for Windows.

This directory contains the source implementation of GloxBar, with the main application contained in `gloxbar.py`.

## Shields

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python\&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt%20for%20Python-green?logo=qt\&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?logo=windows\&logoColor=white)
![Source](https://img.shields.io/badge/Source-Python-orange?logo=python\&logoColor=white)
![UI](https://img.shields.io/badge/UI-PySide6-purple?logo=qt\&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)

</p>

---

## 📁 Source Structure

```text
src/
├── gloxbar.py
├── requirements.txt
└── README.md
```

### `gloxbar.py`

The main GloxBar application.

It contains the floating widget, configuration manager, context menu, themes, opacity controls, application launching logic, and window behavior.

---

## ✨ Features

| Feature                     | Description                                                                      |
| --------------------------- | -------------------------------------------------------------------------------- |
| ⚡ Quick Launch              | Launch frequently used applications and resources directly from the floating bar |
| 🌐 Website Launching        | Open URLs directly from configurable slots                                       |
| 📁 File & Folder Launching  | Open existing files and folders through Windows                                  |
| 🖱️ Drag Anywhere           | Move GloxBar freely around the desktop                                           |
| 📌 Always on Top            | Keeps the widget above normal windows                                            |
| 🎨 Multiple Themes          | Obsidian, Graphite, Espresso, Slate, Midnight and Carbon                         |
| 🌫️ Adjustable Opacity      | Choose between 100%, 80%, 60% and 50% opacity                                    |
| ⚙️ App Manager              | Configure the three available quick-access slots                                 |
| 🔄 Refresh                  | Reload the current configuration                                                 |
| 💾 Persistent Configuration | Saves slots, theme and opacity locally                                           |
| 🪶 Lightweight              | Designed as a small floating utility rather than a full launcher                 |

---

## 🧩 How It Works

GloxBar provides **three configurable slots**.

Each slot can point to:

* A Windows application
* A website
* A file
* A folder
* A supported shell command

When a slot is activated, GloxBar determines the target type and launches it using the appropriate Windows mechanism.

The configuration is stored locally in:

```text
gloxbar_config.json
```

This allows the user's selected apps, targets, theme and opacity settings to persist between launches.

---

## 🎨 Themes

GloxBar currently includes:

| Theme    | Description                   |
| -------- | ----------------------------- |
| Obsidian | Dark graphite-style interface |
| Graphite | Neutral dark interface        |
| Espresso | Warm dark interface           |
| Slate    | Cool dark interface           |
| Midnight | Deep dark interface           |
| Carbon   | High-contrast dark interface  |

Themes can be changed from the GloxBar right-click menu.

---

## ⚙️ Context Menu

Right-clicking GloxBar provides access to:

```text
Manage Apps
Refresh
Theme
    ├── Obsidian
    ├── Graphite
    ├── Espresso
    ├── Slate
    ├── Midnight
    └── Carbon
Opacity
    ├── 100%
    ├── 80%
    ├── 60%
    └── 50%
Exit
```

---

## 🛠️ Technology

| Technology              | Purpose                                           |
| ----------------------- | ------------------------------------------------- |
| Python                  | Core application logic                            |
| PySide6                 | GUI, windows, menus and widgets                   |
| Qt                      | Desktop UI framework through PySide6              |
| JSON                    | Local configuration storage                       |
| Windows APIs / Commands | Opening applications, files, folders and commands |

PySide6 provides the official Qt bindings for Python.

---

## 📦 Installation

From this `src` directory:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python gloxbar.py
```

For a cleaner development environment, using a Python virtual environment is recommended.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Then:

```bash
pip install -r requirements.txt
python gloxbar.py
```

---

## 🧪 Development

The source is intentionally kept simple so that GloxBar can be modified and experimented with easily.

Common areas for development include:

* Adding new themes
* Adding additional slots
* Improving configuration handling
* Adding launch target types
* Improving animations and interactions
* Extending the settings manager
* Adding additional desktop utilities

---

## 👤 Credits

**AvgLucer | Gaurav W**
**CEO & Founder at Glox Industries**

**Glox Industries**
*Building Softwares With a New Vision*

---

## ⚠️ Warning

> **FOR USER, EDUCATIONAL & TEACHING PURPOSES ONLY**
>
> GloxBar is provided for users to learn from, use, modify and experiment with.
>
> This project must **not** be used to falsely claim ownership or authorship of the original project.
>
> Do not present GloxBar or its source code as your own original project or remove/replace the original credits.

---

## 📄 Source Notice

This directory contains the source code for GloxBar.

For the packaged application and download information, refer to the main GloxBar repository documentation.

---

**Glox Industries — Building Softwares With a New Vision**
