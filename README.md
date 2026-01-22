# 📁 File Management Application

A modern, secure, and user-friendly desktop File Management Application built with Python and CustomTkinter.
It simplifies file and folder operations with features like secure login, auto-sorting, real-time search, file preview, undo sort, and theme customization.

## 🚀 Project Overview

The File Management Application is a comprehensive desktop solution designed to organize, manage, and navigate files efficiently. Whether you are managing downloads, project folders, or large media directories, this application provides a clean UI with powerful functionality.

Built using CustomTkinter, it offers a modern look and works seamlessly on Windows, macOS, and Linux.

## ✨ Features
### 🔐 Secure Login System

Username and password authentication

Prevents unauthorized access

Clean and modern login UI

Default credentials:

Username: admin

Password: 12345

## 📂 File Explorer Interface

Table-based file and folder display

Shows file name, type (File/Folder), and size

Real-time updates during operations

Sortable columns

Color-coded selection highlights

## 🛠 File Operations

Open files with default system applications

Rename files and folders

Move files between directories

Delete files/folders with confirmation

Navigation history with Back button

## 🔍 Search & Filter

Real-time file search

Case-insensitive filtering

Instant results while typing

Clear search with one click

Works within the current directory

## 🔄 Auto-Sort Files

Automatically organizes files by extension

Creates folders such as PDF, JPG, DOCX, etc.

Logs operations in file_log.json

Displays sorting time and file count

Ideal for Downloads and project folders

↩ Undo Sort

Restores files to their original locations

Uses file_log.json for recovery

One-click undo

Automatically removes log file after restoration

👁 File Preview Panel

Displays detailed metadata for selected files or folders:

File name and type

Size (KB and bytes)

Full file path

Created, modified, and accessed timestamps

Author and content details

## 🎨 Theme Customization

Dark Mode (default)

Light Mode

Instant theme switching

Professional color schemes

No restart required

## 💻 System Requirements

Python 3.7+

OS: Windows / macOS / Linux

Required Libraries:

customtkinter

tkinter

os

shutil

json

time

## ⚙️ Installation
1️⃣ Install Python

2️⃣ Install Dependencies
pip install customtkinter

3️⃣ Run the Application
python login.py

🧭 How to Use
Login

Run login.py

Enter credentials

Click Login

File Explorer opens

Basic Actions

Choose Folder – Browse any directory

Open – Open files or folders

Rename – Rename selected items

Move – Move files to another folder

Delete – Permanently delete files

Back – Navigate to previous folder

Refresh – Reload current directory

🗂 Project Structure
FILE MANAGEMENT APPLICATION/
│
├── login.py        # Login interface & authentication
├── Design.py       # Main file explorer application
└── README.md       # Project documentation


Runtime File:

file_log.json – Stores auto-sort history for undo functionality

⌨ Keyboard Shortcuts

Arrow Keys – Navigate file list

Enter – Open file/folder

Delete – Delete selected item (with confirmation)

⚠ Important Notes

File deletion is permanent

Always confirm before deleting important files

Auto-sort supports undo only for the latest sort

Themes reset to Dark Mode on restart

🐞 Troubleshooting

Login window is blank
➡ Update CustomTkinter:

pip install --upgrade customtkinter


Sort not working
➡ Select a folder first
➡ Ensure write permissions

Preview not loading
➡ Select a file and wait briefly

## 🔮 Future Enhancements

Multiple user accounts

Database-based authentication

File encryption

Batch operations

Favorites & shortcuts

Cloud integration

Backup and versioning

## 🧠 Technical Details

Language: Python 3.12+

GUI Framework: CustomTkinter

Architecture: Object-Oriented Programming

Data Storage: JSON (for logging)

## 📜 License

This project is provided as-is for educational and file management purposes.
Use at your own risk. Always back up important data.

## 🤝 Support

For issues, bugs, or feature requests, please open an issue or refer to the code documentation.
