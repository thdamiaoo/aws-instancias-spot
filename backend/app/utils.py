import requests
from app.config import Config

def obter_informacoes_instancias(regiao):
    """
    Obtém informações sobre os tipos de instâncias disponíveis na região especificada.

    Args:
        regiao (str): A região da AWS para a qual as informações das instâncias devem ser obtidas.

    Retorna:
        dict: Um dicionário contendo informações sobre os tipos de instâncias, 
        incluindo núcleos, memória RAM, economia, rótulo de frequência de interrupção e EMR.
    """
    response = requests.get(Config.DATA_URL)
    data = response.json()
    instance_types = data['instance_types']
    ranges = data['ranges']
    spot_advisor = data['spot_advisor']

    instancias_info = {}

    if regiao in spot_advisor:
        for instance_type, info in instance_types.items():
            if instance_type in spot_advisor[regiao]['Linux']:
                s = spot_advisor[regiao]['Linux'][instance_type]['s']
                r_index = spot_advisor[regiao]['Linux'][instance_type]['r']
                frequency_label = ranges[r_index]['label']

                instancias_info[instance_type] = {
                    "cores": info['cores'],
                    "ram_gb": info['ram_gb'],
                    "savings": s,
                    "frequency_label": frequency_label,
                    "emr": info['emr']
                }

    return instancias_info
