import requests
import json
import time
import boto3
from requests_aws4auth import AWS4Auth

# Parâmetros do loader
neptune_endpoint = "neptune-cluster-imd.cluster-sa-east-1.neptune.amazonaws.com"  # Endpoint do Neptune
neptune_port = 8182
s3_bucket_path = "s3://infra-acervo/data-file.csv"  # Caminho do arquivo no bucket S3
format_type = "csv"  # Pode ser 'csv', 'opencypher', 'ntriples', 'nquads', 'rdfxml', ou 'turtle'
iam_role_arn = "arn:aws:iam::123456789012:role/your-neptune-s3-role"  # Substitua pelo ARN da role associada ao Neptune
aws_region = "sa-east-1"  # Região AWS do seu Neptune e S3
fail_on_error = "FALSE"
parallelism = "MEDIUM"
queue_request = "TRUE"

# Sessão boto3 para pegar credenciais da instância EC2
session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()
auth = AWS4Auth(credentials.access_key, credentials.secret_key, aws_region, 'neptune-db', session_token=credentials.token)

# Montando a URL do Neptune Loader
loader_url = f"https://{neptune_endpoint}:{neptune_port}/loader"

# Corpo da requisição em JSON
payload = {
    "source": s3_bucket_path,
    "format": format_type,
    "iamRoleArn": iam_role_arn,
    "region": aws_region,
    "failOnError": fail_on_error,
    "parallelism": parallelism,
    "queueRequest": queue_request,
}

# Cabeçalhos da requisição
headers = {
    "Content-Type": "application/json"
}

# Fazendo a requisição POST para o Neptune Loader com autenticação IAM
response = requests.post(loader_url, headers=headers, data=json.dumps(payload), auth=auth)

# Verificando o status da resposta
if response.status_code == 200:
    response_data = response.json()
    load_id = response_data.get("payload", {}).get("loadId", None)
    print(f"Load iniciado com sucesso! ID do load: {load_id}")

    # Loop para verificar o status do load a cada 30 segundos
    if load_id:
        status_url = f"https://{neptune_endpoint}:{neptune_port}/loader/{load_id}"

        while True:
            # Fazendo a requisição GET para verificar o status do load com autenticação IAM
            status_response = requests.get(status_url, auth=auth)
            if status_response.status_code == 200:
                status_data = status_response.json()
                load_status = status_data.get("payload", {}).get("status", "UNKNOWN")
                print(f"Status do Load: {load_status}")

                # Se o status for 'LOAD_COMPLETED' ou 'LOAD_FAILED', sair do loop
                if load_status in ['LOAD_COMPLETED', 'LOAD_FAILED']:
                    print("Carregamento finalizado!")
                    break
            else:
                print(f"Erro ao verificar o status. Status Code: {status_response.status_code}")
                print(f"Detalhes: {status_response.text}")

            # Espera por 30 segundos antes de verificar o status novamente
            time.sleep(30)
else:
    print(f"Erro ao iniciar o load. Status Code: {response.status_code}")
    print(f"Detalhes: {response.text}")