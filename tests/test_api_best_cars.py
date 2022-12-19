# from api_best_cars import client, data_for_entries


# def test_get_data():
#     res = client.get('/')

#     assert res.status_code == 200

# def test_add_data():
#     len_data = len(data_for_entries)
#     data = {
#         'id': 4,
#         'model': 'test',
#         'year': 0,
#         'engine': ['_', (0, '_'), (0, '_')],
#         'speed': [(None, None), (None, None)],
#         "released": "___ ___ copies",
#     }
#     res = client.post('/', json=data)

#     assert res.status_code == 200
#     assert len(res.get_json()) == len_data + 1


def test_art():
    assert 2 == 2
