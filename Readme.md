# Running a Specific Task with Docker or Python

## Running with Docker

To execute a specific task using Docker, follow these steps:

```sh
cd <task№>
docker build -t my_task .
docker run --rm my_task
```

## Running locally

To execute a specific task directly on your pc, follow these steps:

```sh
cd <task№>
pip install -r requirements.tst
python ./main
```
