from aiohttp import web
import os
import pathlib

from covid_api.db import close_pg, init_pg
from covid_api.routes import setup_routes, setup_cors
from covid_api.helpers import load_config

def init_app(pytest=False):
  app = web.Application()

  if pytest:
    app['db_config'] = load_config('config/test-database.yaml')
    app['http_config'] = load_config('config/test-server.yaml')
  else:
    app['db_config'] = load_config('config/database.yaml')
    app['http_config'] = load_config('config/server.yaml')

  # create db connection on startup, shutdown on exit
  app.on_startup.append(init_pg)
  app.on_cleanup.append(close_pg)

  # setup views and routes
  setup_routes(app)
  setup_cors(app)

  return app


def main():
  app = init_app()

  web.run_app(app,
              host=app['http_config']['host'],
              port=app['http_config']['port'])

if __name__ == '__main__':
  main()
