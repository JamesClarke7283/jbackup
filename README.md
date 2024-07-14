# jbackup - James's Backup Utility

jbackup is a flexible system backup program designed with simplicity and beauty in mind. It provides both a graphical user interface (GUI) and a command-line interface (CLI) for creating and managing backups.

## Features

- Simple and intuitive GUI using CustomTkinter
- Command-line interface for automation and scripting
- Backup scheduling
- Platform-independent configuration using appdirs
- Tar and zstd compression for efficient backups
- Progress bar with ETA for backup operations
- Remote backups using rsync (supports OpenSSH and TinySSH)
- Automatic deletion of old remote backups

## Requirements

- Python 3.11 or higher

## Installation

[Add installation instructions here]

## Usage

### GUI

To start the graphical user interface:

```
jbackup-gui
```

### CLI

To use the command-line interface:

```
jbackup [options]
```

For more information on CLI options, run:

```
jbackup --help
```

## Configuration

The configuration file is stored in the user's config directory under the `jbackup` folder. The exact location depends on the operating system:

- Linux: `~/.config/jbackup/config.toml`
- macOS: `~/Library/Application Support/jbackup/config.toml`
- Windows: `C:\Users\<username>\AppData\Local\jbackup\config.toml`

## License

This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).

## Author

James David Clarke <james@jamesdavidclarke.com>