import pathlib

from controllers import add_covid, list_covid, statistics_covid, options_add_covid

def setup_routes(app):
  app.router.add_post('/api/add', add_covid)
  app.router.add_options('/api/add', options_add_covid)
  app.router.add_get('/api/list', list_covid)
  app.router.add_get('/api/statistics', statistics_covid)
