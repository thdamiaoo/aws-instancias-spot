FROM openjdk:11-jdk-slim

# Instala o Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie o requirements.txt para dentro do contêiner
COPY ./backend/requirements.txt .

# Instale as dependências
RUN pip3 install --no-cache-dir -r requirements.txt

# Copie o restante do código do backend
COPY ./backend/app ./app
COPY ./backend/data ./data

# Exponha a porta 5000
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python3", "-m", "app.main"]
