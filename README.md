# covid-api
A simple API to monitor the progress of the COVID-19 pandemic

## Tools used

* POSTGRES as database
* AIOHTTP to serve the request API

## Endpoints definition

* add a new case: a person has been detected as infected. The person will be defined by a national identification number, a country, an age, and a state of health.
* list existing cases: list the last/first X cases, filtering by country will be allowed. 
* show statistics: list the number of cases by country, the cases will be splitted in three state: 'infected', 'treated' or 'dead'.

### Formal endpoints specification

An OpenAPI Specification is included in the project.

### Database model definition

A COVID-19 case will be represented and saved in the table *detected_cases* defined by the fields:
* *id*: sequence id (integer)
* *national_id*: national identification number of a person (integer)
* *country*: country name given (string)
* *age*: age of the person (integer)
* *health*: state of health of a person (enum values 'infected', 'treated', 'dead')

We will have a first primary key *id* indexed to speedup the listing of last/first X cases.
A second primary key (*national_id*,*country*) indexed to speedup the retrieve/update/delete of a given case. 
The country column will be indexed to speedup the counting of cases by country.
