## Prerequisites

- A Redis instance running on the default port
- Python 3.10 or later, with `poetry` installed

## Setup

```shell
# assuming you've cloned the project and are inside the directory
poetry install
poetry shell
python manage.py migrate
python manage.py runserver
```
