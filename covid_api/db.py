import enum
import pycountry
from sqlalchemy import (
	MetaData, Table, Column, PrimaryKeyConstraint,
	BigInteger, Integer, String, Enum, Index
)

metadata = MetaData()

class Health(enum.Enum):
	INFECTED = 1
	TREATED = 2
	DEAD = 3

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
Index('idx_country', detected_cases.c.country, unique=False)

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

