# Sky Prophet

[![Continuous Integration](https://github.com/UribeAlejandro/SkyProphet/actions/workflows/ci.yml/badge.svg)](https://github.com/UribeAlejandro/SkyProphet/actions/workflows/ci.yml)

[![Continuous Delivery](https://github.com/UribeAlejandro/SkyProphet/actions/workflows/cd.yml/badge.svg)](https://github.com/UribeAlejandro/SkyProphet/actions/workflows/cd.yml)

This project is part of the interviewing process for the position of Machine Learning Engineer. The goal of the project is to build a build, test & serve a Machine Learning model able to predict the likelihood of flight delays.

## Table of Contents


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

To run the server using docker you need to run the following command:

```bash
docker build -t skyprophet .
docker-compose up -d
```

You should be able to access the server at `http://localhost:8000`. The documentation of the API is available at `http://localhost:8000/docs`.

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


#### Tracking


#### Registry


#### Serving


## Monitoring

![Monitoring](img/SkyProphet-Monitoring.drawio.svg)
