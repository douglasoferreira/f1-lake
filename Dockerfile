FROM python:3.10-slim-bullseye

# Instala o Java (necessário para o Spark) e compiladores básicos
RUN apt-get update && apt-get install -y \
    openjdk-11-jre-headless \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configura as variáveis de ambiente para o Java funcionar com o Spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Copia primeiro apenas o requirements.txt (boa prática para cache do Docker)
COPY requirements.txt .

# Instala as dependências do Python e o Jupyter (caso queira analisar os dados localmente)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir notebook ipykernel

# Copia o restante dos arquivos do projeto (seus scripts .py e .env)
COPY . .

# Expõe as portas do Jupyter (8888) e do Spark UI (4040)
EXPOSE 8888 4040