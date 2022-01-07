### Data pipeline

### Prerequisites

```
pip3 install psycopg2-binary openpyxl
```

A database server needs to be running in addition. It is recommended to run this locally due to the remote (or our remote database) being very slow. This can be done by running the following in the ```./database``` directory.

```
sudo docker-compose up --build
```

### Run pipeline

```
./pipeline.sh
```

### Pipeline steps

##### etl

ETL takes the data from the csv files which this repo contains and processes them into the database. It matches and combines the datasets but does minimal cleansing. It's main focus is just getting everything into the database.

##### cleansing

Cleansing cleanses the actual data in the database. Cleansing reads from the database and updates the database with the cleansed data. Cleansing is not perfect in that it does remove every single possible null value. More information about how cleansing works is in the ```./pipeline/cleansing/README.md```.

##### featureEngineering

Feature engineering modifies the database and adds features based on other features.

### dataQueue

Data queue is not a part of the pipeline but is included because it would be meant to be deployed after this pipeline happens. Data queue allows a Kafka instance to be set up to consume new possible messages from consumers that could be set up. More information about how this works and running this in ```./pipeline/dataQueue/README.md```.