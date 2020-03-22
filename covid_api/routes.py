import pathlib

import aiohttp_cors
from covid_api.controllers import add_covid, list_covid, statistics_covid

def setup_routes(app):
  app.router.add_post('/api/add', add_covid)
  app.router.add_get('/api/list', list_covid)
  app.router.add_get('/api/statistics', statistics_covid)

def setup_cors(app):
  # cors = aiohttp_cors.setup(app)
  cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
  })
  for route in list(app.router.routes()):
    cors.add(route)

