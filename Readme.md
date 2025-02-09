# Running a Specific Task with Docker or Python

## Running with Docker

To execute a specific task using Docker, follow these steps:

```sh
cd <task-№>
docker build -t <any-name> .
docker run --rm <any-name>
```

## Running with Python

To execute a specific task using local Python instalation, follow these steps:

```sh
cd <task-№>
pip install -r requirements.txt
python ./main.py
```
