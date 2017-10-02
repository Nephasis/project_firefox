PROJECT FIREFOX VERSION 1.3
Martyna Chojnacka

What is it?
-------------------------------------------------------------------------------

Poject_Firefox is a small web application created to enable executing
calculations at server side from every place with internet connection. Version 1.3
covers asynchronous processess and it's able to run multiple processess at once.

Installation
-------------------------------------------------------------------------------

To start using Project Firefox you need to install following applications:
- Python
- Flask
- SQLite 3
- Jinja2
- Venv (virtualenv, virtual environment)

How to run Project Firefox?
-------------------------------------------------------------------------------

Once you have installed all required applications open project directory in
console and type in $. venv/bin/activate to activate a virtual environment.

Check if there is a database file "records.db" in database folder. If not,
run file init.py in console due to create new database. You can use init.py
to recreate database in further usage.

To activate Project_Firefox run app.py from console with active venv and enter
the site by adress shown in terminal.

Now you can upload your file with approprieate format and, after calculations
are done, you can download results by clicking "Download" button associated with your
calculations.
