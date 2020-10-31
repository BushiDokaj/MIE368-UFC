# MIE368-UFC
Contains code for MIE368 project that uses analytics to understand the strengths and weaknesses of different fighting styles.


## Setting up the virtual env
You can use this website to learn about using virtualenv (https://docs.python-guide.org/dev/virtualenvs/)
We'll be using virtualenv with Python to set up the environment that will track all of the libraries we use

Commands to run from terminal:
    1. run pip install virtualenv to get virtualenv
    2. create your virtualenv using the command virtualenv ufc (your virtual environment will be called ufc)
    3. run ufc\Scripts\activate to activate the virtual env called ufc
    4. run pip install -r requirements.txt to install all of the libraries we are already using
    5. if you install any other libraries run pip freeze > requirements.txt

You need to activate the virual env to be able to access the libraries and for the code to run properly

## For Tyler and Will
In the DataStorage folder the file fighter_details_links.csv contains all of the links that you will need
to read.

When you write your code, output the data into files in this folder.
