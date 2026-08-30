# 🔍 Glox Lens — Source Code

<p align="center">

  <a href="../README.md">
    <img src="https://img.shields.io/badge/Glox-Lens-brown?style=for-the-badge" alt="Glox Lens">
  </a>

  <a href="https://github.com/AvgLucer/GloxWidgets">
    <img src="https://img.shields.io/badge/Glox%20Industries-Glox%20Widgets-8B6F47?style=for-the-badge" alt="Glox Widgets">
  </a>

</p>

<p align="center">

  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">

  <img src="https://img.shields.io/badge/GUI-PySide6-41CD52?style=flat-square&logo=qt&logoColor=white" alt="PySide6">

  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=flat-square&logo=windows&logoColor=white" alt="Windows">

  <img src="https://img.shields.io/badge/Status-Released-success?style=flat-square" alt="Released">

</p>

---

# 📌 About

This directory contains the **source-side files for Glox Lens**, a desktop utility developed as part of the **Glox Widgets** ecosystem.

The `SRC` directory is intended for developers, learners, contributors, and users interested in examining the project's implementation and structure.

Glox Lens follows the broader Glox development philosophy of creating practical desktop software with a clean and recognizable interface.

---

# 📂 Source Directory

The `SRC` directory contains the source implementation and supporting documentation for Glox Lens.

```text
SRC/
│
├── gloxlens.py
├── requirements.txt
└── README.md
```

> The exact source structure may change as the project develops.

---

# 🧩 Source Information

| Property             | Details             |
| -------------------- | ------------------- |
| **Project**          | Glox Lens           |
| **Directory**        | `SRC/`              |
| **Primary Language** | Python              |
| **GUI Framework**    | PySide6             |
| **Target Platform**  | Windows             |
| **Project Family**   | Glox Widgets        |
| **Organization**     | Glox Industries     |
| **Developer**        | AvgLucer | Gaurav W |
| **Status**           | Released            |
| **Source Type**      | Desktop Application |
| **Dependency File**  | `requirements.txt`  |

---

# 🛠️ Technology Stack

## Python

Glox Lens is developed using **Python**, providing the primary programming environment for the application.

Python is responsible for the application logic, event handling, program execution, and integration between the different components of the application.

---

## PySide6

The graphical interface is built using **PySide6**, Qt's official Python bindings.

PySide6 provides the components required for creating the desktop interface, including windows, widgets, layouts, events, and other GUI functionality.

```text
Python
   │
   └── PySide6
         │
         ├── Application
         ├── Windows
         ├── Widgets
         ├── Layouts
         └── Events
```

---

# 📦 Dependencies

The project's Python dependency is maintained inside:

```text
requirements.txt
```

Current dependency:

```txt
PySide6>=6.6.0
```

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# 🚀 Running From Source

## 1. Clone the Repository

```bash
git clone https://github.com/AvgLucer/GloxWidgets.git
```

Then enter the Glox Lens source directory.

```bash
cd GloxWidgets/GloxLens/SRC
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Run Glox Lens

Run the Python source file:

```bash
python gloxlens.py
```

---

# 🔄 Development Workflow

A basic development workflow for the source version is:

```text
Clone Repository
       │
       ▼
Enter GloxLens/SRC
       │
       ▼
Create / Activate Environment
       │
       ▼
Install requirements.txt
       │
       ▼
Run gloxlens.py
       │
       ▼
Test Application
       │
       ▼
Modify Source
       │
       ▼
Test Again
       │
       ▼
Prepare Release
```

---

# 🧪 Development Environment

A virtual environment is recommended when working with the source code.

### Create Environment

```bash
python -m venv .venv
```

### Activate on Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run

```bash
python gloxlens.py
```

---

# 📋 Requirements

| Requirement | Purpose                               |
| ----------- | ------------------------------------- |
| **Python**  | Application development and execution |
| **PySide6** | Desktop GUI framework                 |
| **Windows** | Primary target platform               |
| **pip**     | Python package installation           |

---

# 🏗️ Source Architecture

At a high level, the application follows a desktop-application structure:

```text
┌──────────────────────────────┐
│          Glox Lens           │
├──────────────────────────────┤
│                              │
│       Python Application     │
│              │               │
│              ▼               │
│           PySide6            │
│              │               │
│      ┌───────┴───────┐       │
│      ▼               ▼       │
│    UI Layer      Event Logic │
│      │               │       │
│      └───────┬───────┘       │
│              ▼               │
│       Application Logic      │
│                              │
└──────────────────────────────┘
```

---

# 🎨 Glox Development Philosophy

The source code is part of the broader Glox Industries ecosystem.

The development philosophy focuses on:

* Clean interfaces
* Practical utilities
* Understandable source code
* Independent software projects
* Experimentation
* Learning
* Desktop-focused applications
* Consistent Glox branding

---

# 👨‍💻 For Developers

The `SRC` directory is primarily useful when you want to:

* Examine the source code
* Learn how the application is structured
* Modify the application
* Experiment with the interface
* Test changes
* Study PySide6 development
* Extend the project
* Build your own version
* Learn from a real desktop utility project

---

# 🧠 Learning Opportunities

Glox Lens can be used as a practical learning project for studying:

| Topic                     | Description                       |
| ------------------------- | --------------------------------- |
| **Python**                | Application programming           |
| **PySide6**               | Desktop GUI development           |
| **Qt Widgets**            | Building graphical interfaces     |
| **Event Handling**        | Responding to user interactions   |
| **Layouts**               | Organizing GUI components         |
| **Application Structure** | Organizing desktop software       |
| **Dependencies**          | Managing external packages        |
| **Virtual Environments**  | Isolating Python projects         |
| **Git**                   | Version control                   |
| **GitHub**                | Source distribution               |
| **Documentation**         | Maintaining project documentation |

---

# 🔧 Modifying the Source

When modifying Glox Lens:

1. Create a working copy or branch.
2. Install the required dependencies.
3. Make your changes.
4. Run the application.
5. Test the modified functionality.
6. Check for errors.
7. Review the source.
8. Commit your changes appropriately.

Example workflow:

```bash
git checkout -b feature/my-change
```

Make your changes, then test:

```bash
python gloxlens.py
```

---

# 🧹 Recommended Development Practices

When modifying the project, try to maintain:

* Clear variable names
* Readable functions
* Consistent indentation
* Logical organization
* Minimal unnecessary dependencies
* Useful comments where appropriate
* Proper error handling
* Consistent UI behavior

Avoid introducing dependencies that are not actually required by the application.

---

# 📦 Requirements Management

All third-party Python dependencies should be represented in:

```text
requirements.txt
```

Install them with:

```bash
pip install -r requirements.txt
```

Update the requirements file whenever a genuine runtime dependency is added or removed.

---

# 🖥️ Platform

Glox Lens is primarily intended for:

```text
Windows
```

The application uses a desktop GUI architecture and is distributed as part of the Windows-oriented Glox Widgets ecosystem.

---

# 🔗 Repository

### Glox Widgets

https://github.com/AvgLucer/GloxWidgets

### Glox Lens Documentation

[← Return to Glox Lens README](../README.md)

### Download

[⬇️ Open DOWNLOAD.md](../DOWNLOAD.md)

---

# 📊 Project Status

<img src="https://img.shields.io/badge/Project-Glox%20Lens-8B6F47?style=flat-square" alt="Project">

<img src="https://img.shields.io/badge/Release-Released-success?style=flat-square" alt="Release">

<img src="https://img.shields.io/badge/Source-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">

<img src="https://img.shields.io/badge/Framework-PySide6-41CD52?style=flat-square&logo=qt&logoColor=white" alt="PySide6">

---

# ⚠️ Educational & User Warning

> **Glox Lens is provided for educational, teaching, experimentation, development, and legitimate user purposes only.**

The source code is intended to provide an opportunity to study, learn from, experiment with, and use the project responsibly.

Users are responsible for modifications they make to the source code and for how they use any resulting software.

Use the project responsibly and only for legitimate purposes.

---

# 👨‍💻 Credits

## AvgLucer | Gaurav W

**CEO & Founder at Glox Industries**

Glox Lens is developed under the Glox Industries ecosystem.

```text
AvgLucer | Gaurav W
CEO & Founder
Glox Industries
```

---

# ⭐ Glox Lens

```text
GLOX INDUSTRIES
       │
       └── Glox Widgets
              │
              └── Glox Lens
```

**Build. Learn. Experiment. Create.**

**— AvgLucer | Gaurav W**
**CEO & Founder — Glox Industries**
