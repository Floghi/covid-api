import enum
import pycountry
import aiopg.sa
from sqlalchemy import (
  MetaData, Table, Column, PrimaryKeyConstraint,
  BigInteger, Integer, String, Enum, Index
)
from psycopg2.errors import UniqueViolation

metadata = MetaData()

class Health(enum.Enum):
  infected = 1
  treated = 2
  dead = 3

# define the detected_cases table
detected_cases = Table(
  'detected_cases', metadata,

  Column('id', BigInteger, primary_key=True),
  Column('national_id', BigInteger),
  Column('country', String(64)),
  Column('age', Integer),
  Column('health', Enum(Health)),
)
Index('idx_national_id_country', detected_cases.c.national_id,
      detected_cases.c.country, unique=True)
Index('idx_country_health', detected_cases.c.country,
      detected_cases.c.health, unique=False)

allowed_countries = list(map(lambda x: x.name,list(pycountry.countries)))

def construct_db_url(config):
  DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
  return DSN.format(
    user=config['DB_USER'],
    password=config['DB_PASS'],
    database=config['DB_NAME'],
    host=config['DB_HOST'],
    port=config['DB_PORT'],
  )

async def init_pg(app):
  config = app['db_config']['user']
  db_url = construct_db_url(config)
  engine = await aiopg.sa.create_engine(db_url)
  app['db'] = engine

async def close_pg(app):
  app['db'].close()
  await app['db'].wait_closed()

# Insert a new case of COVID-19
async def add_covid(conn, national_id, country, age, health):
  """Add a new case

  :param conn: The database connection.
  :type conn: aiopg.sa.connection.SAConnection
  :param national_id: national identification number of a person
  :type national_id: int
  :param country: the country of a person
  :type country: str
  :param age: the age of a person
  :type age: int
  :param health: the state of health of a person
  :type health: str

  :rtype: None
  """
  country = country.replace("'","''")
  try:
    await conn.execute("""INSERT INTO detected_cases (national_id, country, age, health)
                            VALUES (%i, '%s', %i, '%s')"""% (national_id, country, age, health))
    return 200
  except UniqueViolation:
    return 422

# List cases of COVID-19
async def list_covid(conn, size, sort, offset=0, country="null"):
  """List existing cases

  List the last/first SIZE cases.

  :param conn: The database connection.
  :type conn: aiopg.sa.connection.SAConnection
  :param size: The number of cases to fetch.
  :type size: int
  :param sort: Sort order:  * 'asc' - Ascending, from first cases to last cases.  * 'desc' - Descending, from last cases to first cases.
  :type sort: str
  :param offset: An offset to allow pagination.
  :type offset: int
  :param country: Filter out the cases by their country (null value will ignore the filter).
  :type country: str

  :rtype: List[{ national_id: int, country: str, age: int, health: str}]
  """
  print(type(conn))
  country = country.replace("'","''")
  if country == "null":
    query = """SELECT * FROM detected_cases ORDER BY id %s LIMIT %i OFFSET %i""" % (sort, size, offset)
  else:
    query = """SELECT * FROM detected_cases WHERE country = '%s' ORDER BY id %s LIMIT %i OFFSET %i""" % (country, sort, size, offset)
  proxy = await conn.execute(query)
  records = await proxy.fetchall()

  response = list(map(lambda r: {'national_id': r[1], 'country': r[2], 'age': r[3], 'health': r[4]}, records)) # serialize
  return response

# Compute statistics of COVID-19
async def statistics_covid(conn, size, sort, offset):
  """Statistics on cases by country

  List the number of cases by country, the cases will be splitted in three state 'infected', 'treated' or 'dead'

  :param size: The number of countries to fetch.
  :type size: int
  :param sort: Sort order:  * 'asc' - Ascending, from the least affected country to the most affected country.  * 'desc' - Descending, from the most affected country to the least affected country.
  :type sort: str
  :param offset: An offset to allow pagination.
  :type offset: int

  :rtype: List[{ country: str, total: int, treated: int, infected: int, dead: int}]
  """
  query = "SELECT COUNT(*) as count,country, health FROM detected_cases GROUP BY country,health"
  proxy = await conn.execute(query)
  records = await proxy.fetchall()

  # format the response
  country_hash = {}
  for record in records:
    count = record[0]
    country = record[1]
    health = record[2]

    value = country_hash.get(country, {'country': country, 'total': 0, 'infected': 0, 'treated': 0, 'dead': 0})
    value[health] = count
    value['total'] += count
    country_hash[country] = value
  response = list(country_hash.values())
  if sort == 'asc':
    return sorted(response, key=lambda value: value['total'])[offset:(offset+size)]
  else:
    return sorted(response, key=lambda value: -value['total'])[offset:(offset+size)]
