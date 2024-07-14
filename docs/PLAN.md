# Plan for James's Backup

I want to have it without encryption first.

Also I want to use appdirs to store the backup in a platform independent, cache, directory.

I also want the program to have a CLI so it can be done on the CLI.

I want the scheduling of backups to happen using the tool. And the config file for the program after I use the GUI program uses the .config folder (use appdirs for a platform independent solution).

I want it to require python 3.11 or higher. And use the built-in tomllib module. and a module that let's us write toml files too.

The config file will be in the appdirs config folder under the folder jbackup. Which is the name of the program. James's Backup.

All source code will be in the "src" folder.

Start by writing me a pyproject.toml.

The license will be GPLv3-or-later. Author: "James David Clarke", email: "james@jamesdavidclarke.com".

The entry point to run the program will be.

src/app.py
The binary will be called jbackup-gui

The CLI will be in src/cli.py
And the binary will be called "jbackup"

We will use tar to put all the files in one file, then use zstd to compress it.

All non frontend code will be in src/core folder.

We need a convenient GUI interface to select the directories and files to backup.

We also need a progress bar for each stage, we have two stages in that progress bar.
1. We copy all the files into a .tar file.
2. We compress the files into a .zst file.

We also provide a ETA for completion for the progress bar.

We need to be able to add rsync backups, to pick a backup folder on a remote system with rsync (supporting openssh and tinyssh by doing that)
Also ability to delete remote backups older than a specific time period (in days).

## File tree
jbackup/
├── pyproject.toml
├── README.md
├── src/
│   ├── app.py
│   ├── cli.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── backup.py
│   │   ├── compress.py
│   │   └── config.py

## Philosophy
1. Free/Libre software
2. Simplicity (Simple to use)
3. Beauty (Looks really good with CustomTkinter)

