# littleR
## Overview

This project is a bit different than most projects. Yes, it is a python package.
It also is a tool intended to be used by a requirements author to create requirements.
Think of this as "package as a service".

Not only does this project document itself in the docs folder (sphinx), but it also
describes its requirements. Those requirements are captured in the
__./littleR/templates/littleR_req__ folder using this very tool (littleR).

Also hiding in the package is a fully working web application (django). This is used as
the graphic interface for editing the requirements in littleR. Of course they can also
be edited directly in the .yaml file.

The entry point to all of this is the file **manage.py** which is an old school prompt
based text interface. It will present and allow the requirements author to select from
all the avaliable tasks. 

**manage.py** is the place to start your first project too, selecting option 2.

## Installation
- Install from pypi
    ```
    pip install littleR
    ```
    -or-
- Add littleR to your requirements.txt file in your python project

## Contribute
This project was developed on windows in a python venv. Some of the tools require a special
install on windows. The following describes how to check out the project to contribute to the 
project.

### Prerequsites
- Install Make 
- Install Python, at least python 3.12
- Change the execution policy of the powershell. [Security Issue]
    ```
    Get-ExecutionPolicy
    Set-ExecutionPolicy Unrestricted -Scope CurrentUser
    ```

### Install
- clone the repository to your machine.
- Run Make
    ```
    make
    make help
    ```