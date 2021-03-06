import json
from aiohttp.web import Response, json_response
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from covid_api.helpers import load_yaml
from covid_api.validator import ValidationFailed, validate_list_input, validate_statistics_input
from covid_api import db

async def add_covid(request):
  body = await request.text()
  data = json.loads(body)

  try: # validation
    openapi = load_yaml('specifications/openapi.yaml')
    schema = openapi['definitions']['Case']
    validate(instance=data, schema=schema)
  except ValidationError as e:
    return json_response({ 'message': e.message}, status=422)

  async with request.app['db'].acquire() as conn:
    national_id = data['national_id']
    country = data['country']
    age = data['age']
    health = data['health']

    code = await db.add_covid(conn, national_id, country, age, health)
    if code == 422:
      return json_response({'message': 'The case already exists.'}, status=code)
    else:
      return json_response(status=code)

async def list_covid(request):
  data = request.query

  try: # validation
    validate_list_input(data)
  except ValidationFailed as e:
    return json_response({ 'message': e.message}, status=422)

  async with request.app['db'].acquire() as conn:
    size = int(request.query['size'])
    sort = request.query['sort']
    offset = int(request.query.get('offset',0))
    country = request.query.get('country','null')

    response = await db.list_covid(conn, size, sort, offset, country)
    return json_response(response)

async def statistics_covid(request):
  data = request.query

  try: # validation
    validate_statistics_input(data)
  except ValidationFailed as e:
    return json_response({ 'message': e.message}, status=422)

  async with request.app['db'].acquire() as conn:
    size = int(request.query['size'])
    sort = request.query['sort']
    offset = int(request.query.get('offset',0))
    response = await db.statistics_covid(conn, size, sort, offset)
    return json_response(response)
