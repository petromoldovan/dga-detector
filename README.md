## DGA Detection Tool

DGA Detection Tool uses machine learning to detect if a domain is DGA-based.

## Core Dependencies

`python3.9`, `pipenv`

## Installation

``` sh
pipenv install
```

Train model:
``` sh
pipenv run python ./models/train.py
```

Start classification API:
``` sh
pipenv run python ./server.py
```

TESTING
``` sh
curl -X POST http://127.0.0.1:5000/detect \
    -H "Content-Type: application/json" \
    -d '{"domain": "sadasdasdewde.com"}'
```

### Unit tests
``` sh
pipenv run python -m unittest discover tests
```
