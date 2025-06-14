# Python Fast API

### Table of Contents

1. [Checklist](#checklist)
2. [Additional pip packages](#additional-pip-packages)
3. [Prerequisites](#prerequisites)
4. [Virtual Environment](#virtual-environment)
5. [Running Pytest unit tests](#running-pytest-unit-tests)
6. [Dockerise](#dockerise)
   - [Up and running?](#up-and-running)

### Checklist
<b>Features</b>
- [x] Use Python 3 and FastAPI.
- [x] Extend the API to support filtering with the following GET parameters:
  - [x] `currency` (string): Filter orders by currency (e.g. GBP, USD).
  - [x] `shipped_to` (string): Filter orders by shipping location.
  - [x] `cost` (float): Filter orders with cost >= given value.
- [x] Ensure the API can handle multiple filters at once.
- [x] Return a JSON response with the following structure:
  - [x] `results`: Number of matching orders.
  - [x] `filters`: Dictionary of filters used.
  - [x] `orders`: List of filtered orders.
- [x] Add extra useful GET parameters for filtering.
  - [x] Document and explain how to test them.
- [x] Dockerise the application.
- [x] Implement sensible logging.
- [x] Unit testing

## APIs
- [x] Support testing with curl commands such as:
  ```bash
  curl 'localhost:8000/api/orders?currency=GBP&shipped_to=Essex&cost=150'
- [x] Sort in ascending order (oldest first)
    - `curl 'localhost:8000/api/orders/sort?sort=ascend'`
- [x] Sort in descending order (newest first)
    - `curl 'localhost:8000/api/orders/sort?sort=descend'`


### Additional pip packages
- pytest
    - unit tests are essential for maintaing a secure code base, especially when python is not as type safe as a language like TypeScript.
- httpx
    - Needed for pytest...
    - RuntimeError: The starlette.testclient module requires the httpx package to be installed.

### Prerequisites
- Go into python directory
    - `cd Python`

### Virtual Environment
1) Create virtual environment `python -m venv venv`
2) Activate venv with `venv\Scripts\activate` on Command Prompt or `\venv\Scripts\Activate.ps1` on powershell
3) `pip install -r requirements.txt` - install packagaes
4) `pip list` to verify packcages
5) `deactivate` when finished


### Running Pytest unit tests
`python -m pytest`

### Dockerise

- Use docker desktop (i'm on windows, not WSL)
- Run `docker build -t fastapi-orders-app .` to create docker image
    - Note: If you encounter an error about python version not found, make sure the Python version in the Dockerfile matches an available version on Docker Hub. The Dockerfile has been updated to use Python 3.13.3-slim.
- Run the docker container with port mapping `docker run -d -p 8000:8000 fastapi-orders-app`
- Verify container is running:
    - `docker ps`
- Stop containers
    - `docker stop $(docker ps -q)`

#### Up and running?
- Try pinging the API!!
    `curl 'localhost:8000/api/orders?currency=GBP&shipped_to=Essex&cost=150'`
- Alternatively, open the browser with:
    - http://localhost:8000/api/orders?currency=GBP&shipped_to=Essex&cost=150
