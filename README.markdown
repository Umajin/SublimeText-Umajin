# Introduction
A Umajin Bundle for [Sublime Text 2](http://www.sublimetext.com/2)

# Features

 - **Syntax highlighting** for umajin (.u) sources.

Still to come:

 - **Umajin engine completion**, code hints and error highlighting
 - **Class discovery/completion**
 - **Sublime build system integration**, multiple build management, including running tests
 - Code snippets
 - Auto-include

# Installation

### Sublime Package Control
The bundle is available through [Package Control](http://wbond.net/sublime_packages/package_control)

### Mac OSX
    cd /Users/<username>/Library/Application\ Support/Sublime\ Text\ 2/Packages
    git clone https://github.com/AdamHarte/SublimeText-Umajin.git Umajin
### Linux
    cd ~/.config/sublime-text-2/Packages
    git clone https://github.com/AdamHarte/SublimeText-Umajin.git Umajin
### Windows
    (Using git bash http://code.google.com/p/msysgit/)
    cd /c/Users/<username>/AppData/Roaming/Sublime\ Text\ 2/Packages
    git clone https://github.com/AdamHarte/SublimeText-Umajin.git Umajin

Restart Sublime Text 2

# Usage

 - Open your project's directory (where the umajin2.exe and .u files reside) in Sublime Text.
 - Edit your classes
 - Completion is triggered either automatically by dot and colon keys, or manually by Ctrl+Space.
 - Comma keys display umajin type hints in the status bar

### Shortcuts

 - Press **Ctrl+Shift+B** to either automatically generate an hxml file if none exist, edit the build file if only one build exists or select among multiple builds (--next)
 - Press **Ctrl+Enter** to run the current/selected build
 - Press **Ctrl+I** on a qualified class name to generate the include_once statement. Safe to use if the class is already included.

# Troubleshooting

On Ubuntu, you'll probably need to install package python2.6

    sudo apt-get install python2.6


