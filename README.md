# Docker Beginner Exercise

A minimal project to learn the core Docker workflow: Dockerfile → Image → Container, with docker-compose orchestrating multiple containers together.

## Project Structure

```
docker-exercise-beginner/
├── Dockerfile            # Recipe to build the processor image
├── docker-compose.yml    # Orchestrates the two containers
├── process.py            # The data processing script
├── data/
│   └── input.json        # Input data (mounted into the container)
└── output/
    └── result.json       # Output written by process.py (mounted back to host)
```

## How Docker Works (the mental model)

```
Dockerfile
    ↓  docker build
  Image  (frozen blueprint, portable)
    ↓  docker run  (or docker compose up)
Container  (live process, isolated)
    ↑
  volumes  ← bridge between your local filesystem and the container
```

### 1. Dockerfile → Image

A `Dockerfile` is a recipe. Running `docker build` executes it and produces an **image** — a frozen, portable snapshot of an OS + your code + dependencies.

This project's `Dockerfile`:
- Starts from `python:3.10-slim` (an existing base image)
- Sets `/app` as the working directory inside the container
- Copies `process.py` into the image
- Sets a default environment variable
- Declares `python process.py` as the command to run on startup

### 2. Image → Container

A **container** is a live instance of an image — like launching a program from an executable. You can run many containers from one image.

Containers are **isolated** from your machine by default. Files inside a container are not visible on your host, and vice versa — unless you connect them with **volumes**.

### 3. Volumes (bridging host and container)

This project mounts two local folders into the container:

```yaml
volumes:
  - ./data:/app/data      # your local data/ is visible inside at /app/data
  - ./output:/app/output  # files written to /app/output appear in your local output/
```

This is how `process.py` can read `input.json` from your machine and write `result.json` back to it.

### 4. docker-compose.yml

`docker-compose.yml` lets you define and run **multiple containers as a system** with one command. Instead of typing long `docker run` commands, all config (volumes, env vars, dependencies) lives in one file.

This project defines two services:

**`processor`** — builds the image from the Dockerfile and runs `process.py`:
- Reads `data/input.json`, computes a summary, writes `output/result.json`

**`viewer`** — a second container that waits for `processor` to finish, then prints the result:
- Uses `depends_on: processor` to sequence the two containers

## Why No DAG File?

A DAG (Directed Acyclic Graph) is an **Airflow** concept for scheduling and orchestrating complex pipelines. You need it when you have:
- Scheduled runs (e.g. every day at 6am)
- Many dependent tasks with retry logic
- A monitoring UI for pipeline runs

This project is simpler — one script, run once, manually. The two-step sequence (`processor` → `viewer`) is handled directly by `depends_on` in docker-compose. Airflow would be a layer on top of Docker for when the workflow outgrows this.

| Complexity | Tool |
|---|---|
| One script, run manually | `docker run` or `docker compose up` |
| Multiple containers, run together | `docker-compose.yml` |
| Scheduled pipelines, retries, monitoring | Airflow + DAGs |

## Running the Project

```bash
docker compose up
```

Check the output:

```bash
cat output/result.json
```

## File Extensions

Both `docker-compose.yml` and `docker-compose.yaml` are valid — Docker accepts either. `.yml` is the more common convention.