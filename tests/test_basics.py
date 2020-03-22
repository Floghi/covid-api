
async def test_add_then_list(client, db):
  case = { 'national_id': 1, 'country': 'Belgium', 'age': 54, 'health': 'infected' }
  response = await client.post('/api/add', json=case)

  assert response.status == 200

  response = await client.get('/api/list?size=1&sort=desc')
  data = await response.json()

  assert response.status == 200
  assert len(data) == 1
  assert case == data[0]
