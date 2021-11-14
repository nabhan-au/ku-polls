# ku-polls
[![Build Status](https://app.travis-ci.com/nabhan-au/ku-polls.svg?branch=iteration3)](https://app.travis-ci.com/nabhan-au/ku-polls)
[![codecov](https://codecov.io/gh/nabhan-au/ku-polls/branch/iteration3/graph/badge.svg?token=KSO2HC5D72)](https://codecov.io/gh/nabhan-au/ku-polls)

When you need to run app you should
```
python3 manage.py migrate
python3 manage.py loaddata users polls
```

# KU-POLL

### Wiki
* [Home](https://github.com/nabhan-au/ku-polls/wiki)
* [Vision statement](https://github.com/nabhan-au/ku-polls/wiki/Vision-Statement)
* [Requirement](https://github.com/nabhan-au/ku-polls/wiki/Requirements)

## Getting Started

### Test ID
|username | password |
|---------|----------|
|tester1 | Abcdef12345 |
|tester2 | Abcdef12345 |

### Requirements
|Name  | Recommended version(s)|   
|------|-----------------------|
|Python | 3.7 or higher |
|Django | 2.2 or higher |

### Install Packages
1. Clone this project repository to your machine.

    ```
    git clone https://github.com/nabhan-au/ku-polls.git
    ```
2. Get into the directory of this repository.

    ```
    cd ku-polls
    ```
3. Create a virtual environment.

    ```
    python -m venv venv
    ```
4. Activate the virtual environment.

    - for Mac OS / Linux.   
    ```
    source venv/bin/activate
    ```
    - for Windows.   
    ```
    venv\Scripts\activate
    ```
5. Install all required packages.

    ```
    pip install -r requirements.txt
    ```
6. Create `.env` file in the same level as manage.py and write down:

    ```
    DEBUG=True
    SECRET_KEY=Your-Secret-Key
    ```
7. Run this command to migrate the database.

    ```
    python manage.py makemigrations polls
    python manage.py migrate
    ```
8. load data to database.

    ```
    python manage.py loaddata users polls
    ```
9. Start running the server by this command.
    ```
    python manage.py runserver
    ```
