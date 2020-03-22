# covid-api
A simple API to monitor the progress of the COVID-19 pandemic

## Tools used

* POSTGRES as database
* AIOHTTP to serve the request API

## Endpoints definition

* add a new case: a person has been detected as infected. The person will be defined by a national identification number, a country, an age, and a state of health.
* list existing cases: list the last/first X cases, pagination and filtering by country will be allowed. 
* show statistics: list the number of cases by country, the cases will be splitted in three state: 'infected', 'treated' or 'dead'. Pagination will be allowed.

### Formal endpoints specification

An OpenAPI Specification is included in the project under specifications directory. Use its [link](https://raw.githubusercontent.com/Floghi/covid-api/master/specifications/openapi.yaml) in the [swagger UI tool](https://petstore.swagger.io/) to have a full documentation, specification, and test environment of the covid-api.

## Postgres database model definition

A COVID-19 case will be represented and saved in the table *detected_cases* defined by the fields:
* *id*: sequence id (integer)
* *national_id*: national identification number of a person (integer)
* *country*: country name given (string)
* *age*: age of the person (integer)
* *health*: state of health of a person (enum values 'infected', 'treated', 'dead')

We will have a first primary key *id* indexed to speedup the listing of last/first X cases.
Then an index on (*national_id*, *country*) with unique constraint to identify a person and speedup the retrieve/update/delete of a given case. 
Also an index on (*country*, *health*) to speedup the statistics computation.

## Environment and usage

* Install Python3 (tested with 3.6.9)
* Use [virtualenv](https://python-guide-pt-br.readthedocs.io/fr/latest/dev/virtualenvs.html) to isolate your application (optional)
* `git clone https://github.com/Floghi/covid-api.git`
* `pip install -r requirements.txt`

We use a postgres (10.12) database, you can install it locally on your system or use a docker image `docker run --rm -it -p 5432:5432 postgres:10`
Once installed and running you can use the *db_helpers.py* script to initialize, drop or popuate the database.

`python db_helpers.py`
```
 usage: db_helpers.py [-h] [-i] [-d] [-p]

 DB related shortcuts

 optional arguments:
  -h, --help      show this help message and exit
  -i, --init      Initialize empty database and user with permissions
  -d, --drop      Drop database and user role
  -p, --populate  Populate the database with random data
```

Once initialize you can launch the server with `python covid_api/main.py`

## Future developments

Here is a list of potential improvments:
* add a route to update the *health* of a person
* add a statistic of the *age* distribution depending on the *health* state (histogram)
* add more tests and validations of routes
