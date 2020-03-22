import db
from aiohttp.web import Response

async def add_covid(request):
  async with request.app['db'].acquire() as conn:
    data = await request.post()
    national_id = data['national_id']
    country = data['country']
    age = data['age']
    health = data['health']
    await db.add_covid(conn, national_id, country, age, health)
    return Response()

async def list_covid(request):
  async with request.app['db'].acquire() as conn:
    size = int(request.match_info['size'])
    sort = request.match_info['sort']
    offset = int(request.match_info['offset'] or 0)
    country = request.match_info['country'] or 'null'
    response = await db.list_covid(conn, size, sort, offset, country)
    return response

async def statistics_covid(request):
  async with request.app['db'].acquire() as conn:
    response = await db.statistics_covid(conn, national_id, country, age, health)
    return response
