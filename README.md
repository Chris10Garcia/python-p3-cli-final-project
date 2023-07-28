# Phase 3 CLI Project Template: Flatiron Dog Daycare CLI Application


![Preview of CLI functioning]()<!-- need a .gif pushed to current github repo-->


## Table of Content

1. [Overview](#overview)
2. [Get Started](#get-started)
3. [Source and Credits](#source-and-credits)


## Overview

Using Python, I created a command line interface (CLI) application that performs CRUD actions (create read update delete) on a database. 

This application handles managing a "dog daycare center". Within the database, 4 tables are created that houses Dog, Breed, Toy, and Owner entities. A user can perform various CRUD actions such as creating new dog or owner records, retreiving multiple records, printing details of a single record, updating various attributes, and deleting records. 

The packages used for this project are as follows:
- The Click Python package is used to handle creating the CLI commands and tasks.
- Sqlite is utilzied as the datebase.
- The Faker Python package is used to seed data within the database.
- SQLAlchemy is utlized as the Python SQL toolkit and object relational mapper. 
- Alembic is utilized as the database migration tool.


## Get Started

- Clone this repo
- Run pipenv install
- Run pipenv shell
- cd lib/db
- run alembic upgrade head
- run python seed.py
- cd ..

To start the CLI app, next run python cli.py (ensure you're in the lib folder). From there, the help page will display and you can follow the instructions there as to perform the actions you want from the app.

Thank you for visiting my repo and checking my project out!

## Source and Credits

Modules
Faker:
https://faker.readthedocs.io/en/master/index.html 

SQLALc
<!-- link -->

Alembic
<!-- link -->

Click
<!-- link -->


Misc
dog toys
https://www.thesprucepets.com/best-dog-toys-4151137

dog breeds
https://github.com/dariusk/corpora/blob/master/data/animals/dogs.json 

