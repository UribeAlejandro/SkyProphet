# Sky Prophet <!-- omit in toc -->

[![Continuous Integration](https://github.com/UribeAlejandro/SkyProphet/actions/workflows/ci.yml/badge.svg)](https://github.com/UribeAlejandro/SkyProphet/actions/workflows/ci.yml)

[![Continuous Delivery](https://github.com/UribeAlejandro/SkyProphet/actions/workflows/cd.yml/badge.svg)](https://github.com/UribeAlejandro/SkyProphet/actions/workflows/cd.yml)

This project is part of the interviewing process for the position of Machine Learning Engineer. The goal of the project is to build a build, test & serve a Machine Learning model able to predict the likelihood of flight delays.

## Table of Contents <!-- omit in toc -->

- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Test](#test)
- [Data](#data)
  - [Data Version Control](#data-version-control)
  - [Extract, transform, load](#extract-transform-load)
- [Model](#model)
  - [Experiments](#experiments)
    - [Tracking \& Registry](#tracking--registry)
    - [Serving](#serving)
- [Deployment](#deployment)
- [Nice Things to Have](#nice-things-to-have)
  - [Monitoring](#monitoring)
  - [Feature Store](#feature-store)
  - [BentoML](#bentoml)
  - [CI/CD](#cicd)

## Architecture

The architecture of the project is shown below:

![Architecture](img/SkyProphet-Architecture.drawio.svg)

## Installation

To install the project, you need to clone the repository and install the dependencies. To install the dependencies, you need to run the following command:

```bash
make install
```

## Usage

To run the server locally you need to run the following command:

```bash
make run-server
```

> **Note:** The following steps require a `.env` file or the environment variables (`MLFLOW_TRACKING_URI`
and `MLFLOW_EXPERIMENT_NAME`) to be set before running the commands. Otherwise, the commands will fail.

To run the server using docker you need to run the following command:

```bash
docker-compose build
docker-compose up -d
```

You should be able to access the server at `http://localhost:8000`. The documentation of the API is available at `http://localhost:8000/docs`.

The `/docs` route is shown below:

![Docs](img/FastAPI-Docs.png)

You can access the logs of the server using the following command:

```bash
docker-compose logs api
```

You should get an output similar to the following:

```bash
api-1  | INFO:     Will watch for changes in these directories: ['/']
api-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
api-1  | INFO:     Started reloader process [1] using StatReload
api-1  | INFO:     Started server process [8]
api-1  | INFO:     Waiting for application startup.
api-1  | INFO:     Starting up...
api-1  | INFO:     Application startup complete.
api-1  | INFO:     192.168.65.1:18205 - "GET /docs HTTP/1.1" 200 OK
api-1  | INFO:     192.168.65.1:18205 - "GET /openapi.json HTTP/1.1" 200 OK
```

To stop the server you need to run the following command:

```bash
docker-compose down -v
```

## Test

There are three types of tests in the project:
- `API test`: tests all the endpoints of the API.
- `Model test`: tests the model using a sample dataset.
- `Stress test`: tests the performance of the server.

You can run the tests using the following commands:

```bash
make api-test
make model-test
make stress-test
```

Once finished you can see the results of the test within the reports' folder. You will find: `reports/coverage/index.html` and `reports/stress/index.html`.

The reports can be downloaded from the `Actions` page of the repo:

![Reports](img/Reports.png)

## Data

The data is stored in the `datasets` folder. The data is stored in the following format:

```
datasets
├── test
│   └── ...
├── raw
│   └── ...
├── interim
│   └── ...
└── processed
    └── ...
```

The `raw` folder contains the raw data. The `interim` folder contains the data after it has been cleaned. The `processed` folder contains the data after it has been processed and is ready for use in a model. The `test` folder contains the data used for testing.


### Data Version Control

The data is versioned using `DVC`. The data is stored in a remote GCP bucket. It works like git, its commands are similar. For instance, the data stored in `datasets` can be added using the following command:

```bash
dvc add data/
```

Then, the data can be pushed to remote using the following command:

```bash
dvc push
```

The data can be pulled from remote using the following command:

```bash
dvc pull
```

### Extract, transform, load

The ETL process consists of the following steps:

- `extract`: Reads the file `data/raw/data.csv`.
- `transform`: Cleans the data and generates features.
- `load`: Saves the data in `data/processed/data.csv`.

## Model

### Experiments

All the experiments were tracked using `MLFlow`, the tracking server runs in a `GCP VM`, that stores the artifacts (model, confusion matrix, etc) in a `GCP bucket` and the `registry` (metrics, parameters, registered models, etc) in a `PostgreSQL` database that is hosted in `Cloud SQL`. A diagram of the architecture is shown below:

![Experiments](img/SkyProphet-Experiments.drawio.svg)

As mentioned above, were tracked using `MLFlow`. The tracking server can be started using the following command:

```bash
mlflow server --backend-store-uri $BACKEND_STORE_URI --default-artifact-root $DEFAULT_ARTIFACT_ROOT  --host 0.0.0 --port 5000
```

> Note: You should SSH the `GCP VM` to run the command.

#### Tracking & Registry

The `MLFlow` server allows the data practitioner to track the experiments and register the models. An example of the experiments is shown below:

![Experiments](img/Experiments.png)

Once, the model is trained, it can be registered in the `MLFlow` registry. An example of the registry is shown below:

![Registry](img/Registry.gif)

> **Note**: In this case, `capable-ant-951` has been selected as the best model. Because has the highest `F1-score`, `ROC AUC` & `Recall` .


#### Serving

The model is served using `FastAPI`. The model can be served using the following command:

```bash
make run-server
```

The api has the following endpoints:

- `/`: (GET) Greets the user.
- `/predict`: (POST) Predicts the likelihood of a flight delay.
- `/docs`: (GET) Shows the documentation of the API.
- `/health`: (GET) Checks the health of the server.
- `/ping`: (GET) Pings the server.

## Deployment

The deployment of the project is done using `GitHub Actions`. The deployment process consists of the following steps:

- `Continuous Integration`
  - `Build`: Install the dependencies & enforces code style.
  - `Test`: Runs the tests of the project.
- `Continuous Delivery`
  - `Staging`: Build the docker image and push it to the `Container Registry` & `Artifact Regidstry`.
  - `Deploy`: Deploys the created docker image to `GCP Cloud Run` using `Docker`.

The deployed application is shown below:

![Deployment](img/SkyProphet-Deployment.drawio.svg)

> **Note:** The model that runs in the `GCP Cloud Run` is the one that has the best performance in the `MLFlow` registry. However, it is not static. Because it is retrieved from the `MLFlow` registry, it can be updated with a new model that has better performance without the need to redeploy the application. The good news is: The model retieval is cached, so the performance of the application is not affected!

An example of a model promotion is shown below:

![Model Promotion](img/Model-Promoted.png)

> **Note**: The model with the `production` alias is the one that is retrieved by the `GCP Cloud Run`.

## Nice Things to Have

### Monitoring

The monitoring of `SkyProphet` can be done using an adversarial approach. Thus, a second model `adversarial validator` is trained to detect the drift in the data. The architecture of the monitoring system is shown below:

![Monitoring](img/SkyProphet-Monitoring.drawio.svg)

### Feature Store

The model was trained offline and once in production handles online features. It would be nice to have a `Feature Store` to handle the features in production. The workaround that has been implemented partially solves the problem by enforcing the input data to have the same features as the training data. However, it is not ideal because it can get harder to maintain the features in the future.

### BentoML

The model can be served using `BentoML`. This library allows the data practitioner to create a model server that can be deployed in different platforms. It is a grea option because it:

- Make the FastAPI endpoints automatically.
- Dockerizes the application.
- Provides the infrastructure as code to depoy the model in different platforms.


### CI/CD

The actual `CI/CD` runs in `GitHub Actions`, a demanding task such as the `stress-test` is running there, which is not ideal. Then, would be nice to have a `dev` or `test` environment to carry out all tests and deploy in this environment before deploying to `production`.
