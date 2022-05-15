## DGA Detection Tool

TODO:

## Core Dependencies

`python3.9`, `pipenv`

## Installation

``` sh
pipenv install
```

Start classification API:
``` sh
pipenv run flask run
```

TESTING
``` sh
curl -X POST http://127.0.0.1:5000/detect \
    -H "Content-Type: application/json" \
    -d '{"domain": "sadasdasdewde.com"}'
```
