# epics-web-viewer
This is a web application built from containerised services.

![architecture](architecture_image.png "Layout of the web app")

## Usage
To start this service, you need to do four things:
* Start the containers
* Initialise the database
* Start the PV-reader service
* Start the server

Each of these will need to be executed in an environment that has the following variables set:
```bash
export POSTGRES_DB=the_name_of_the_database
export POSTGRES_NAME=the_postgresql_username
export POSTGRES_PASSWORD=the_super_secret_postgres_password
```

### Starting the containers
```bash
docker-compose build
docker-compose up
```
One problem that might be experienced when executing this command is that there is already a postgres instance running on the host machine, and so port 5432 will not be available.  One solution is to kill the instance (if it's not being used for something critical). Another is to edit the code in the containers to use a different port.

### Initialise the database
```bash
docker-compose run pyepics python3 initialise_db.py
```

### Start the PV service
```bash
docker-compose run pyepics bash
python3 main_process.py
```

### Start the server
```bash
python routes.py
```
