# GloxVault - SOURCE

<p align="center">
  <b>GloxVault</b>
  <br>
  <i>Private. Encrypted. Yours.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows-111111?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.x-111111?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/GUI-PySide6-111111?style=for-the-badge">
  <img src="https://img.shields.io/badge/Encryption-AES--256--GCM-111111?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-111111?style=for-the-badge">
</p>

<p align="center">
  A privacy-focused desktop vault for encrypting and managing protected files using the custom <code>.glox</code> format.
</p>

---

## 🔐 About

**GloxVault** is a desktop file-protection utility developed as part of the **GloxWidgets** project by **Glox Industries**.

It allows users to add files to a local vault, encrypt them, and store them using randomized `.glox` filenames.

Protected files can then be accessed through GloxVault and extracted back into their original usable form when required.

The project is designed with portable storage in mind, making it suitable for:

* USB flash drives
* Pendrives
* External SSDs
* External HDDs
* Local drives

---

## ✨ Features

| Feature                    | Description                                                                    |
| -------------------------- | ------------------------------------------------------------------------------ |
| 🔐 AES-GCM Encryption      | Encrypts stored file data using AES-GCM authenticated encryption.              |
| 🔑 Password Protection     | Vault access is protected by a user-created password.                          |
| 🧂 Random Salt             | Generates a unique 32-byte salt for password-based key derivation.             |
| 🛡️ PBKDF2-HMAC-SHA256     | Derives a 256-bit encryption key from the vault password.                      |
| 📦 `.glox` Format          | Encrypted files are stored using the custom `.glox` extension.                 |
| 🎲 Randomized Filenames    | Encrypted files receive cryptographically random filenames.                    |
| 💾 Portable Storage        | Designed to work well from removable storage devices.                          |
| 📤 File Extraction         | Decrypt protected files back into their usable form.                           |
| 🗑️ File Deletion          | Permanently remove protected files from the vault.                             |
| 🖱️ Drag & Drop            | Drop files directly into the vault to encrypt them.                            |
| 🎨 Multiple Themes         | Includes multiple built-in visual themes.                                      |
| 🌫️ Opacity Control        | Adjust the application's window opacity.                                       |
| 🔒 Vault Locking           | Lock the vault and clear the active encryption key from the application state. |
| ⚡ Animated Interface       | Includes lightweight UI animations and interactive buttons.                    |
| 📁 Automatic Vault Storage | Creates and manages its own vault directory and index.                         |

---

## 🔒 Encryption Architecture

GloxVault uses password-based key derivation followed by authenticated encryption.

### Key Derivation

The vault password is processed using:

```text
PBKDF2-HMAC-SHA256
```

with:

```text
Iterations: 600,000
Derived Key: 32 bytes
Salt: 32 bytes
```

This produces a 256-bit encryption key.

### File Encryption

Files are encrypted using:

```text
AES-256-GCM
```

A fresh 12-byte random nonce is generated for every encryption operation.

The application also uses authenticated data:

```text
GLOXVAULT1
```

This allows AES-GCM to authenticate the encrypted payload and detect invalid or modified data.

---

## 🔄 How It Works

```text
                 User Password
                       │
                       ▼
             PBKDF2-HMAC-SHA256
                       │
                       ▼
                256-bit Key
                       │
                       ▼
                 AES-256-GCM
                       │
                       ▼
                 Encrypted Data
                       │
                       ▼
              Random .glox Filename
                       │
                       ▼
                GloxVaultData/
```

When extracting a file:

```text
.glox File
    │
    ▼
AES-256-GCM Decryption
    │
    ▼
Original File Data
    │
    ▼
User Selected Destination
```

---

## 📁 Storage Structure

GloxVault automatically creates its vault storage directory beside the executable or Python source file.

```text
GloxVault/
│
├── gloxvault.py
│
└── GloxVaultData/
    │
    ├── index.json
    ├── 7f2a...e91c.glox
    ├── 91bc...a102.glox
    └── ...
```

When compiled into an executable, the vault directory is created relative to the executable location.

### `index.json`

The index stores vault metadata such as:

* Vault version
* Password verification data
* Generated salt
* Original filenames
* Encrypted filenames
* Original file sizes

The actual file contents remain inside their encrypted `.glox` files.

---

## 📦 `.glox` Files

A protected file might look like:

```text
personal_document.pdf
```

After being added to GloxVault, it can become something similar to:

```text
a8f5e2c7d91b4e8a6c3d5f7a1b9e2c4d8f6a3b7c9e1d5f2a4b6c8d0e3f7a9b1.glox
```

The randomized filename prevents the encrypted file from directly revealing its original filename.

---

## 🚀 Usage

### 1. Start GloxVault

Run:

```bash
python gloxvault.py
```

On first launch, GloxVault will ask you to create a vault password.

The password must contain at least **6 characters**.

---

### 2. Unlock the Vault

Enter your vault password.

GloxVault verifies the password using the encrypted verification payload stored in the vault configuration.

---

### 3. Add Files

Click:

```text
＋ Add Files
```

Select the files you want to protect.

Alternatively, drag files directly into the vault window.

GloxVault will:

1. Read the file.
2. Generate a random encrypted filename.
3. Encrypt the file using AES-GCM.
4. Store the encrypted `.glox` file.
5. Add its metadata to `index.json`.

---

### 4. Extract Files

Select an encrypted file and click:

```text
↓ Extract
```

Choose the destination where the decrypted file should be saved.

Double-clicking an encrypted file also starts the extraction process.

---

### 5. Delete Files

Select a vault entry and click:

```text
⌫ Delete
```

After confirmation, the corresponding `.glox` file is removed from the vault and its metadata is removed from the index.

---

### 6. Lock the Vault

Click:

```text
🔒 Lock
```

GloxVault clears the active encryption key from the application state and returns to the login screen.

---

## 🎨 Themes

GloxVault includes multiple built-in themes:

* Obsidian
* Graphite
* Charcoal
* Espresso
* Slate
* Midnight
* Crystal Cream
* Aurora Night
* Lavender
* Glowy Sunshine
* Mono
* Blood Red

Themes can be changed from:

```text
◐ Theme
```

---

## 🌫️ Opacity

The vault interface includes an opacity slider.

The available range is:

```text
70% → 100%
```

This allows the user to adjust the transparency of the GloxVault window.

---

## 💾 Portable Storage

GloxVault can be placed on removable storage.

Example:

```text
USB Drive
│
└── GloxVault
    │
    ├── GloxVault.exe
    │
    └── GloxVaultData
        │
        ├── index.json
        ├── file1.glox
        ├── file2.glox
        └── file3.glox
```

This makes it possible to keep the application and encrypted vault together on a portable drive.

---

## 🛠️ Requirements

* Windows
* Python 3.x
* PySide6
* cryptography

Install the dependencies with:

```bash
pip install -r requirements.txt
```

Then run:

```bash
python gloxvault.py
```

---

## 📂 Project Structure

```text
GloxVault/
│
├── src/
│   └── gloxvault.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

Runtime vault data is automatically generated:

```text
GloxVaultData/
├── index.json
└── *.glox
```

---

## ⚠️ Important Security Notes

GloxVault is designed as a practical privacy-focused file vault, but users should understand its limitations.

### Keep Your Password Safe

Your vault password is not stored in plaintext.

If you forget your password, GloxVault does not provide a password recovery mechanism.

**Keep a secure record of your password.**

### Keep Backups

Always maintain backups of important files.

If the encrypted vault is lost, corrupted, or deleted and no backup exists, the original files may not be recoverable.

### Do Not Modify `.glox` Files

Encrypted `.glox` files should be managed through GloxVault.

Do not manually modify their contents or rename them unless you understand the consequences.

---

## ⚠️ Warning

> [!WARNING]
>
> **GloxVault is provided for user, educational, teaching, learning, experimentation, and understanding purposes only.**
>
> Do not claim GloxVault or its source code as your own project.
>
> Do not redistribute the project while falsely representing yourself as its original creator.
>
> Always respect the original project, its authors, and its license.
>
> **Keep backups of important files. Do not rely on GloxVault as the sole copy of important data.**

---

## 📜 License

GloxVault is released under the **MIT License**.

See the `LICENSE` file for the complete license terms.

---

## 👨‍💻 Credits

### Glox Industries

**Founder & CEO:**
**AvgLucer | Gaurav W**

GloxVault is a project developed under the **GloxWidgets** ecosystem.

> **Building Softwares With a New Vision.**

---

## 📌 Project Information

| Property       | Information         |
| -------------- | ------------------- |
| Project        | GloxVault           |
| Developer      | AvgLucer | Gaurav W |
| Organization   | Glox Industries     |
| Platform       | Windows             |
| Language       | Python              |
| GUI Framework  | PySide6             |
| Encryption     | AES-256-GCM         |
| Key Derivation | PBKDF2-HMAC-SHA256  |
| File Format    | `.glox`             |
| License        | MIT                 |

---

<p align="center">
  <b>GloxVault</b>
  <br>
  Private. Encrypted. Yours.
</p>

<p align="center">
  © 2026 Glox Industries
</p>
