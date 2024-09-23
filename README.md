
# Spot Instance Advisor

O **Spot Instance Advisor** é uma aplicação Flask que fornece insights sobre a redução de custo de infraestrutura utilizando instâncias Spot da AWS. A aplicação permite que os usuários consultem e analisem dados de instâncias Spot, oferecendo uma interface amigável para visualizar economias e frequências de interrupção.

## Índice

- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Funcionalidades](#funcionalidades)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes](#testes)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Tecnologias Utilizadas

- Python 3.10
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- PySpark
- Boto3
- Jest (para testes de frontend)
- Pytest (para testes de backend)

## Funcionalidades

- **Listagem das regiões**: Permite ao usuário listar as regiões AWS disponíveis.
- **Listagem de Instâncias Spot**: Permite ao usuário listar instâncias filtrando por região, tipo de instância, CPU e memória.
- **Histórico de Preços**: Coleta e exibe o histórico de preços das instâncias Spot.
- **Análise de Economia**: Compara os preços das instâncias Spot com as instâncias On-Demand, apresentando economias.
- **Frequência de Interrupção**: Fornece informações sobre a frequência de interrupção das instâncias Spot.

## Instruções para Execução

### Pré-requisitos
- Docker
- Docker Compose

### Execução da Aplicação
1. Clone o repositório:
   ```bash
   git clone https://github.com/thdamiaoo/aws-instancias-spot.git
   cd spot-instance-advisor
   ```

2. Execute a aplicação:
   ```bash
   docker-compose up --build
   ```

3. Verificar status da aplicação:
   ```bash
   docker ps -a
   ```

A aplicação estará disponível em http://localhost:5000.

### Exemplos de Uso com cURL

- Obter lista de regiões:
   ```bash
   curl -X GET http://localhost:5000/api/regioes
   ```

- Filtrar instâncias Spot:
   ```bash
   curl -X GET "http://localhost:5000/api/instancias?regiao=us-east-1&cpu=4&memoria=16&tipo_instancia=t2.micro"
   ```

- Coletar histórico de preços:
   ```bash
   curl -X GET "http://localhost:5000/coletar_historico_precos?tipo=t2.micro&regiao=us-east-1"
   ```

- Testar um endpoint que aceita dados (POST):
   ```bash
   curl -X POST http://localhost:5000/api/alguma_rota -H "Content-Type: application/json" -d '{"campo1": "valor1", "campo2": "valor2"}'
   ```

** Veja os parâmetros obrigatórios para cada caso.

## Testes

Para garantir a qualidade do código, testes foram desenvolvidos para o frontend e backend. Para executá-los:

### Testes de Backend
1. Navegue até o diretório de testes:
   ```bash
   cd backend/tests
   ```

2. Execute os testes:
   ```bash
   pytest
   ```

### Testes de Frontend
1. Navegue até o diretório de testes:
   ```bash
   cd frontend/tests
   ```

2. Execute os testes:
   ```bash
   npm test
   ```

## Contribuição

Apesar de ser um repositório específico de um teste de Engenharia de dados, contribuições são bem-vindas! 
Sinta-se à vontade para fazer um fork do repositório, fazer suas alterações e enviar um pull request. 
Para mais informações, consulte as diretrizes de contribuição.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
