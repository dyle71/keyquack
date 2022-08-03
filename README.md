# keyquack

Annoy your colleagues.

Triggered on a comment to mine:

(German) "Kannst du in Zukunft solche Meetings wo du das Meeting leitest bitte nicht 
im Büro machen? Der kleine Raum in der Mitte wäre da besser geeignet."

This simple program makes stupid annoying sounds when you type.

Sounds are picked from https://archive.org/.
* Quack sound: https://archive.org/details/quacksoundeffect


## Prerequisite

This program uses ffplay or avplay to play sounds. Please have one of those 
installed.


## Setup

I strongly recommend to work within a [virtual environment](https://docs.python.org/3/library/venv.html).

Prepare a virtual environment like this (you may have to install `python3-venv` beforehand):
```bash
$ mkdir venv
$ python3 -m venv venv
```

Then activate the virtual environment in a shell. Example (assuming `bash`, note the dot '.'!):
```bash
$ . venv/bin/activate
```

Hence, that this alters your prompt indicating that you are now operating with the venv.

As an alternative you may switch into the development environment by simply sourcing then
`env.sh` file:

```bash
$ source ./env.sh
```

This will pull in the virtual environment and will adjust `PYTHONPATH` and `PATH` variables
accordingly.


Next install the required packages:
```bash
$ pip3 install -r requirements.txt 
```

## Building

You can create source distributions (sdist) and wheels with this command:

```bash
$ python -m build
```

A folder `dist` will be created holding the package files.  

On a remote machine, you'll need a decent python3 (>= 3.8 will do) installment and pip installed.
Then copy the package of the `dist` folder to the machine and run:
```bash
$ sudo apt-get install python3 python3-pip
...
$ pip install keyquack-*.whl
```

## Running

If you have installed the virtual environment and activated it as well as installed the
necessary packages as stated in the requirements, then 
```bash
$ keyquack
```
... and annoy your colleagues.


### More fun

* Use `--distribute` to distribute the frequency of the sound across the keyboard.
* Use `--sound muh` to switch to cows instead of ducks.
* Use `--list-only` to see what sounds are currently available.


## Notable guidelines

* How (not) to write git commit messages: https://www.codelord.net/2015/03/16/bad-commit-messages-hall-of-shame/
* How to version your software: https://semver.org/
* How to write a clever "Changes" file: https://keepachangelog.com/en/1.0.0/
* Folder Convention: https://github.com/KriaSoft/Folder-Structure-Conventions


---

(C) Copyright 2022  
Oliver Maurhart, headcode.space, https://headcode.space
