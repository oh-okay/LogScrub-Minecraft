# Log File Cleaner

A lightweight Python tool that scans directories for log files containing a target string and removes lines matching flagged keywords.

Useful for cleaning server logs, removing unwanted traces, or filtering out specific client/mod signatures from logs.

---

## Features

- Recursively scans directories for log files
- Detects files containing a target string
- Removes lines containing flagged keywords
- Supports dry-run mode (preview changes safely)
- Optional verbose output for removed lines
- Can scan only `.log` files or all file types

---

## Installation

Requires Python 3.7+

Clone or download the script:

```bash
git clone https://github.com/oh-okay/LogScrub-Minecraft.git
cd log-cleaner

---

# Credits to a person whom name i should not mention.
