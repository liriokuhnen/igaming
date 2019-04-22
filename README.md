I-gaming
========

A platform to play bet games online

### 1 - Dependencys

The dependencys to running this project is python 3.6, PIP and Virtualenv so if you already had those packages installed you can skip this session.(Virtualenv is not necessary but is extremely recommended).

##### Guide to work with python 3:

Folow those link below to install Python 3, PIP and Virtualenv

[python 3 on Linux](http://docs.python-guide.org/en/latest/starting/install3/linux/ "Install python 3 on linux")
[python 3 on Mac](http://docs.python-guide.org/en/latest/starting/install3/osx/ "Install python 3 on Mac")
[python 3 on Windows](http://docs.python-guide.org/en/latest/starting/install3/win/ "Install python 3 on Windows")

### 2 - Install requirements:

Before to install the requirements for this project you need to create and active your virtualenv.

```
virtualenv -p python3 envname
source envname/bin/activate
```

If you has luck and have the virtualenvwrapper installed just need one command

```
mkvirtualenv -p python3 envname
```

##### Install requirements

To install the requirements for this project run

```
pip3 install -r requirements.txt
```

### 3 - Running migrations

To running migrations for database

```
./manage.py migrate
./manage.py load_bonuses_config
```

### 4 - Create SuperUser

Create super user to manager bonuses delivery

```
./manage.py createsuperuser
```

### 5 - Run the project

```
./manage.py runserver
```

You can see the project at http://127.0.0.1:8000/

### 6 - Run tests

To running the tests

```
./run_tests.sh
```

If you have some problem to run this command give permission to the bash script

```
chmod +x run_tests.sh
```