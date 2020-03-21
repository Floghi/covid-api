import argparse
from sqlalchemy import create_engine, MetaData
from covid_api.helpers import load_config
from covid_api.db import construct_db_url, detected_cases

def init_db(config):
  engine = get_engine(config['admin'])

  db_name = config['user']['DB_NAME']
  db_user = config['user']['DB_USER']
  db_pass = config['user']['DB_PASS']

  with engine.connect() as conn:
    drop_db(config)

    conn.execute("CREATE USER %s WITH PASSWORD '%s'" % (db_user, db_pass))
    conn.execute("CREATE DATABASE %s" % db_name)
    conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" %
                 (db_name, db_user))

    create_tables(config)

def drop_db(config):
  engine = get_engine(config['admin'])

  db_name = config['user']['DB_NAME']
  db_user = config['user']['DB_USER']

  with engine.connect() as conn:
    # terminate all connections to be able to drop database
    conn.execute("""
      SELECT pg_terminate_backend(pg_stat_activity.pid)
      FROM pg_stat_activity
      WHERE pg_stat_activity.datname = '%s'
        AND pid <> pg_backend_pid();""" % db_name)
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)

def populate_db(config):
  # TODO
  print(user_db_config)

def create_tables(config):
  engine = get_engine(config['user'])

  meta = MetaData()
  meta.create_all(bind=engine, tables=[detected_cases])

def get_engine(config):
  db_url = construct_db_url(config)
  engine = create_engine(db_url, isolation_level='AUTOCOMMIT')
  return engine

if __name__ == '__main__':
  db_config = load_config('config/database.yaml')

  parser = argparse.ArgumentParser(description='DB related shortcuts')
  parser.add_argument("-i", "--init",
                      help="Initialize empty database and user with permissions",
                      action='store_true')
  parser.add_argument("-d", "--drop",
                      help="Drop database and user role",
                      action='store_true')
  parser.add_argument("-p", "--populate",
                      help="Populate the database with random data",
                      action='store_true')
  args = parser.parse_args()

  if args.init:
    init_db(db_config)
  elif args.drop:
    drop_db(db_config)
  elif args.populate:
    populate_db(db_config)
  else:
    parser.print_help()

