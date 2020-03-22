import pytest

from covid_api.main import init_app
from covid_api.helpers import load_config
from db_helpers import (
  init_db,
  drop_db,
)

@pytest.fixture
async def client(loop, aiohttp_client):
  app = init_app(pytest=True)
  return await aiohttp_client(app)


@pytest.fixture(scope='module')
def db():
  db_config = load_config('config/test-database.yaml')

  init_db(db_config)
  yield
  drop_db(db_config)
