import db
import json
from aiohttp.web import Response, json_response

async def options_add_covid(request):
  return json_response()

async def add_covid(request):
  async with request.app['db'].acquire() as conn:
    body = await request.text()
    data = json.loads(body)

    national_id = data['national_id']
    country = data['country']
    age = data['age']
    health = data['health']

    code = await db.add_covid(conn, national_id, country, age, health)
    return json_response(status=code)

async def list_covid(request):
  async with request.app['db'].acquire() as conn:
    size = int(request.query['size'])
    sort = request.query['sort']
    offset = int(request.query.get('offset',0))
    country = request.query.get('country','null')
    response = await db.list_covid(conn, size, sort, offset, country)

    return json_response(response)

async def statistics_covid(request):
  async with request.app['db'].acquire() as conn:
    response = await db.statistics_covid(conn, national_id, country, age, health)
    return response
