import os

class Config:
    """
    Classe de configuração para o aplicativo.

    Atributos:
        DATA_URL (str): URL do arquivo JSON que contém os dados do Spot Advisor.
    """
    DATA_URL = 'https://spot-bid-advisor.s3.amazonaws.com/spot-advisor-data.json'
