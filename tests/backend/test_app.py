# test_main.py

def test_get_regioes(client):
    response = client.get('/regioes')
    assert response.status_code == 200
    assert 'us-east-1' in response.json

def test_obter_instancias(client):
    response = client.get('/instancias_spot?regiao=us-east-1&tipo_instancia=c5.large&cpu=2&memoria=4')
    assert response.status_code == 200
    assert len(response.json['instances']) > 0

def test_coletar_historico_precos_sem_tipo(client):
    response = client.get('/coletar_historico_precos?regiao=us-east-1')
    assert response.status_code == 400
    assert 'Tipo de instância e região são obrigatórios.' in response.json['error']
