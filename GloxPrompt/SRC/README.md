# GloxPrompt - SOURCE

<p align="center">
  <img src="https://img.shields.io/badge/GloxPrompt-FF1744?style=for-the-badge&logo=sparkles&logoColor=white">
  <img src="https://img.shields.io/badge/SOURCE-8E5CFF?style=for-the-badge&logo=github&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/PySide6-41CD52?style=for-the-badge&logo=qt&logoColor=white">
  <img src="https://img.shields.io/badge/OpenRouter-7C3AED?style=for-the-badge&logoColor=white">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Desktop%20Application-8B5CF6?style=for-the-badge">
  <img src="https://img.shields.io/badge/API%20Powered-FF6B35?style=for-the-badge">
  <img src="https://img.shields.io/badge/Multiple%20Models-00B8D4?style=for-the-badge">
  <img src="https://img.shields.io/badge/Multiple%20Themes-FF4081?style=for-the-badge">
</p>

---

## About

**GloxPrompt** is a desktop application built by **Glox Industries** that transforms simple ideas into detailed, structured and high-quality AI prompts.

Instead of manually figuring out how to structure a complicated prompt, users can describe what they want normally and let GloxPrompt refine the idea into a much more complete prompt.

This folder contains the **source code** used to build and run GloxPrompt.

---

## Features

* ✨ Natural idea-to-prompt generation
* 🤖 OpenRouter API integration
* 🧠 Multiple AI model selection
* 🎨 Multiple application themes
* 🖥️ PySide6 desktop interface
* 🔐 `.env` based API key configuration
* ⚡ Detailed prompt generation
* 📋 Easy prompt copying
* 🪟 Windows desktop support
* 🧩 Simple single-file source structure

---

## How GloxPrompt Works

```text
Your Idea
    │
    ▼
GloxPrompt Interface
    │
    ▼
Selected AI Model
    │
    ▼
OpenRouter API
    │
    ▼
Prompt Generation
    │
    ▼
Refined AI Prompt
```

The user enters an idea in normal language, selects an available model, and GloxPrompt sends the request through OpenRouter.

The generated result is then displayed directly inside the application.

---

## Source Structure

The source folder is intentionally simple:

```text
SRC/
└── gloxprompt.py
```

The main application logic, interface, API communication and prompt-generation workflow are contained inside:

```text
gloxprompt.py
```

---

## Requirements

Before running the source code, make sure Python is installed.

### Main Dependencies

```text
Python
PySide6
OpenRouter
python-dotenv
```

Install the required packages with:

```bash
pip install PySide6 openrouter python-dotenv
```

If your environment uses a different OpenRouter package configuration, install the dependencies required by the current source code.

---

## API Configuration

GloxPrompt requires an OpenRouter API key.

Create a `.env` file in the appropriate application directory and add:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Do **not** place your actual API key directly inside the Python source code.

Never commit a real API key to GitHub.

---

## Running From Source

Open a terminal inside the `SRC` folder and run:

```bash
python gloxprompt.py
```

The GloxPrompt desktop application should launch normally.

---

## Model Selection

GloxPrompt is designed to allow users to select from available AI models rather than forcing a single model.

This makes it possible to experiment with different models and compare their generated prompts.

Model availability can change depending on the models currently provided through OpenRouter.

---

## Themes

The application includes multiple visual themes so users can change the appearance of the interface.

Themes are handled directly through the desktop application and do not change the underlying prompt-generation workflow.

---

## Generation

A typical workflow is:

1. Launch GloxPrompt.
2. Enter your idea.
3. Select an available AI model.
4. Choose your preferred theme if required.
5. Generate the prompt.
6. Review the generated result.
7. Copy and use the refined prompt with your preferred AI tool.

Generation time depends on the selected model, API response time and network conditions.

---

## Development

The source is kept relatively compact so that the application can be easier to understand, experiment with and modify.

You can use the source to explore:

* PySide6 desktop application development
* API integration
* OpenRouter model usage
* Environment variable management
* AI prompt generation
* GUI event handling
* Python application structure

---

## Security

### Never commit your API key

Your `.env` file should remain private.

Add `.env` to `.gitignore`:

```gitignore
.env
```

If an API key is accidentally published, revoke it and generate a replacement key.

---

## Troubleshooting

### Application does not start

Check that Python and all required dependencies are installed:

```bash
pip install PySide6 openrouter python-dotenv
```

### API key error

Check that your `.env` file contains:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Also make sure the key is valid and active.

### Model unavailable

OpenRouter model availability can change. Select another model from the available model list.

### Slow generation

Generation speed depends on the selected model, OpenRouter availability and network conditions.

---

## Project

```text
GloxWidgets/
└── GloxPrompt/
    └── SRC/
        └── gloxprompt.py
```

This folder contains the source implementation of GloxPrompt.

The compiled Windows application and downloadable distribution are maintained separately from this source directory.

---

## Credits

**AvgLucer | Gaurav W**
**Founder & CEO at Glox Industries**

**Building Softwares With a New Vision.**

---

## Educational & Usage Notice

GloxPrompt is provided for user, teaching, understanding, learning, experimentation and educational purposes.

You are welcome to explore the source, understand how it works, experiment with it and build upon your knowledge from studying the project.

However, the project must not be falsely presented or claimed as an independently created project by someone who did not originally develop it.

If GloxPrompt or its source is used, referenced, studied or built upon for educational purposes, please provide appropriate credit to:

**AvgLucer | Gaurav W**
**Glox Industries**

---

<p align="center">
  <b>GloxPrompt</b><br>
  Building Softwares With a New Vision.
</p>
