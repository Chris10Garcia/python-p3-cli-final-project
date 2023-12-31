# Phase 3 Project: Flatiron Dog Daycare CLI Application

![Preview of CLI functioning](https://github.com/Chris10Garcia/python-p3-cli-final-project/blob/main/lib/misc/ezgif.com-video-to-gif.gif)


## Table of Content

1. [Overview](#overview)
2. [Get Started](#get-started)
3. [Source and Credits](#source-and-credits)


## Overview

Using Python, I created a command line interface (CLI) application that performs CRUD actions (create read update delete) on a database. 

This application handles managing a "dog daycare center". Four tables contain Dog, Breed, Toy, and Owner entities. A user can perform various actions such as creating new dog or owner records, retrieving multiple records, printing details of a single record, updating various attributes, and deleting records. 

The packages used for this project are as follows:
- The Click Python package is used to handle creating the CLI commands and tasks.
- SQLite is utilized as the database.
- The Faker Python package is used to seed data into the database.
- SQLAlchemy is utilized as the Python SQL toolkit and object relational mapper. 
- Alembic is utilized as the database migration tool.


## Get Started

Please note, Pipenv is required. See [here](https://pipenv.pypa.io/en/latest/installation/) for installing pipenv. Lastly, my project uses python_version = "3.8.13".

- Clone this repo
- `cd python-p3-cli-final-project` (or `cd` into the name of the directory you gave it)
- Run `pipenv install`
- Run `pipenv shell`
- `cd lib/db`
- Run `alembic upgrade head`
- Run `python seed.py`
- `cd ..`

To start the CLI app, next run `python cli.py` (ensure you're in the lib folder and with the virtual environment running). From there, the help page will display and you can follow the instructions there as to perform the actions you want from the app.

Thank you for visiting my repo and checking my project out!


## Source and Credits

Modules
- [Faker](https://faker.readthedocs.io/en/master/index.html)

- [SQLAlchemy](https://www.sqlalchemy.org/)

- [Alembic](https://alembic.sqlalchemy.org/en/latest/)

- [Click](https://click.palletsprojects.com/en/8.1.x/)

Miscellaneous
- [Dog Toys](https://www.thesprucepets.com/best-dog-toys-4151137)

- [Dog Breeds](https://github.com/dariusk/corpora/blob/master/data/animals/dogs.json)

