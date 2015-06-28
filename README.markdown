# Introduction
A Umajin Bundle for [Sublime Text](http://www.sublimetext.com/)

# Features

 - **Syntax highlighting** for umajin (.u) sources
 - Code snippets
 - Run project (or single file) with debug-gui

Still to come:

 - **Umajin engine completion**, code hints and error highlighting
 - **Class discovery/completion**
 - **Sublime build system integration**, multiple build management, including running tests
 - More code snippets
 - Auto-include

# Installation

### Sublime Package Control
The bundle is available through [Package Control](https://packagecontrol.io/)

### Manual installation

#### Mac OSX
    cd /Users/<username>/Library/Application\ Support/Sublime\ Text\ 2/Packages
    git clone https://github.com/AdamHarte/SublimeText-Umajin.git Umajin
#### Linux
    cd ~/.config/sublime-text-2/Packages
    git clone https://github.com/AdamHarte/SublimeText-Umajin.git Umajin
#### Windows
    (Using git bash http://code.google.com/p/msysgit/)
    cd /c/Users/<username>/AppData/Roaming/Sublime\ Text\ 2/Packages
    git clone https://github.com/AdamHarte/SublimeText-Umajin.git Umajin

Restart Sublime Text

# Usage

 - Open your project's directory (where the umajin.exe and .u files reside) in Sublime Text.
 - Edit your classes
 - Completion is triggered either automatically by dot and colon keys, or manually by Ctrl+Space.
 - Comma keys display umajin type hints in the status bar

### Shortcuts

 - Press **Alt + r** to run the current project in JIT mode
 - Press **Ctrl + Alt + r** to run the current file in JIT mode

# Troubleshooting

On Ubuntu, you'll probably need to install package python2.6

    sudo apt-get install python2.6


