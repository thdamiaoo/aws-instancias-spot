import boto3
import requests
import datetime
from babel.dates import format_datetime
from flask import Blueprint, request, jsonify, render_template
from datetime import timedelta
from app.config import Config
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from app.utils import obter_informacoes_instancias

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """
    Renderiza a página principal do aplicativo.

    Retorna:
        str: Conteúdo HTML da página principal.
    """
    return render_template('index.html')

@main.route('/regioes', methods=['GET'])
def get_regioes():
    """
    Obtém a lista de regiões disponíveis na AWS.

    Retorna:
        jsonify: Lista de nomes das regiões ou mensagem de erro em caso de falha.
    """
    try:
        ec2 = boto3.client('ec2', region_name='us-east-1')
        regions = ec2.describe_regions()
        region_names = [region['RegionName'] for region in regions['Regions']]
        return jsonify(region_names)
    except NoCredentialsError:
        return jsonify({"error": "Credenciais da AWS não encontradas."}), 500
    except PartialCredentialsError:
        return jsonify({"error": "Credenciais da AWS incompletas."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500   

@main.route('/instancias_spot', methods=['GET'])
def obter_instancias():
    """
    Obtém as instâncias Spot com base nos parâmetros fornecidos pelo usuário.

    Retorna:
        jsonify: Lista de instâncias filtradas, total de instâncias, número da página e avisos.
    """
    try:
        response = requests.get(Config.DATA_URL)
        data = response.json()
        
        instance_types = data['instance_types']
        ranges = data['ranges']
        spot_advisor = data['spot_advisor']

        regiao = request.args.get('regiao')
        tipo_instancia = request.args.get('tipo_instancia', '')
        cpu = request.args.get('cpu', '')
        memoria = request.args.get('memoria', '')
        emr = request.args.get('emr', '').lower()
        os_filter = request.args.get('os', '').lower()
        page = int(request.args.get('page', 1))

        instance_list = []

        if regiao not in spot_advisor:
            return jsonify({"error": "Região inválida."}), 400

        for os_type in ['Linux', 'Windows']:
            if regiao in spot_advisor and os_type in spot_advisor[regiao]:
                for instance_type, info in instance_types.items():
                    if instance_type in spot_advisor[regiao][os_type]:
                        s = spot_advisor[regiao][os_type][instance_type]['s']
                        r_index = spot_advisor[regiao][os_type][instance_type]['r']
                        frequency_label = ranges[r_index]['label']

                        instance_info = {
                            "InstanceType": instance_type,
                            "vCPU": info['cores'],
                            "Memory GiB": info['ram_gb'],
                            "Savings over On-Demand": f"{s}%",
                            "Frequency of interruption": frequency_label,
                            "OS": os_type,
                            "EMR": info['emr']
                        }

                        instance_list.append(instance_info)

        # Avisar sobre filtros de 1 ou 2 caracteres
        warnings = []
        if len(tipo_instancia) < 3 and tipo_instancia:
            warnings.append("O filtro 'tipo_instancia' deve ter pelo menos 3 caracteres.")
        if len(cpu) > 0 and len(cpu) < 3:
            warnings.append("O filtro 'cpu' deve ter pelo menos 3 caracteres.")
        if len(memoria) > 0 and len(memoria) < 3:
            warnings.append("O filtro 'memoria' deve ter pelo menos 3 caracteres.")

        # Filtrar por EMR
        if emr in ['true', 'false']:
            emr_value = emr == 'true'
            instance_list = [
                inst for inst in instance_list
                if inst['EMR'] == emr_value
            ]

        # Filtrar por Sistema Operacional
        if os_filter in ['linux', 'windows']:
            instance_list = [
                inst for inst in instance_list
                if inst['OS'].lower() == os_filter
            ]

        # Filtrar por Tipo de Instância
        if len(tipo_instancia) >= 3:
            instance_list = [
                inst for inst in instance_list
                if tipo_instancia in inst['InstanceType'].lower()
            ]

        # Filtrar por CPU
        if cpu:
            cpu = int(cpu)
            instance_list = [
                inst for inst in instance_list
                if inst['vCPU'] >= cpu * 0.8 and inst['vCPU'] <= cpu * 1.2
            ]

        # Filtrar por Memória
        if memoria:
            memoria = int(memoria)
            instance_list = [
                inst for inst in instance_list
                if inst['Memory GiB'] >= memoria
            ]

        page_size = 10
        start = (page - 1) * page_size
        end = start + page_size
        paginated_list = instance_list[start:end]

        return jsonify({
            "total": len(instance_list),
            "page": page,
            "page_size": page_size,
            "instances": paginated_list,
            "warnings": warnings
        })

    except Exception as e:
        return jsonify({"error": f"Erro ao obter instâncias: {str(e)}"}), 500

@main.route('/coletar_historico_precos', methods=['GET'])
def coletar_historico_precos():
    """
    Coleta o histórico de preços de instâncias Spot com base nos parâmetros fornecidos.

    Retorna:
        jsonify: Histórico de preços filtrado, total de entradas, número da página.
    """
    tipo_instancia = request.args.get('tipo_instancia', '')
    regiao = request.args.get('regiao', '')
    os_filter = request.args.get('os', '').lower() 
    page = int(request.args.get('page', 1))

    if not tipo_instancia or not regiao:
        return jsonify({"error": "Tipo de instância e região são obrigatórios."}), 400

    try:
        instancias_info = obter_informacoes_instancias(regiao)

        ec2 = boto3.client('ec2', region_name=regiao)
        end_time = datetime.datetime.now()
        start_time = end_time - timedelta(days=30)

        response_linux = ec2.describe_spot_price_history(
            InstanceTypes=[tipo_instancia],
            ProductDescriptions=['Linux/UNIX'],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=100
        )

        response_windows = ec2.describe_spot_price_history(
            InstanceTypes=[tipo_instancia],
            ProductDescriptions=['Windows'],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=100
        )

        def processar_preco_historico(response, os_type):
            """
            Processa o histórico de preços retornado pela AWS.

            Args:
                response (dict): Resposta da AWS com dados de preços.
                os_type (str): Tipo de sistema operacional ('Linux' ou 'Windows').

            Retorna:
                list: Lista de preços históricos formatados.
            """
            preco_historico = []
            for price in response['SpotPriceHistory']:
                instance_type = price['InstanceType']
                if instance_type in instancias_info:
                    info = instancias_info[instance_type]
                    preco_historico.append({
                        "InstanceType": instance_type,
                        "SpotPrice": price['SpotPrice'],
                        "vCPU": info['cores'],
                        "Memory GiB": info['ram_gb'],
                        "Savings over On-Demand": f"{info['savings']}%",
                        "Frequency of interruption": info['frequency_label'],
                        "Update Date": format_datetime(price['Timestamp'], locale='pt_BR'),
                        "OS": os_type, 
                        "EMR": info['emr']
                    })
            return preco_historico

        preco_historico_linux = processar_preco_historico(response_linux, 'Linux')
        preco_historico_windows = processar_preco_historico(response_windows, 'Windows')

        # Filtrar pelo sistema operacional no histórico
        if os_filter in ['linux', 'windows']:
            preco_historico = [
                item for item in preco_historico_linux + preco_historico_windows
                if item['OS'].lower() == os_filter
            ]
        else:
            preco_historico = preco_historico_linux + preco_historico_windows
        
        preco_historico.sort(key=lambda x: x['Update Date'], reverse=True)
        page_size = 10
        start = (page - 1) * page_size
        end = start + page_size
        paginated_preco_historico = preco_historico[start:end]

        return jsonify({
            "total": len(preco_historico),
            "page": page,
            "page_size": page_size,
            "historico_precos": paginated_preco_historico
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
