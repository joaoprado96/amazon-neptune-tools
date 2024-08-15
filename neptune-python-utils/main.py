from neptune_python_utils.gremlin_utils import GremlinUtils
from neptune_python_utils.endpoints import Endpoints
import boto3

print('Exemplo 1')
# Função para criar o GremlinUtils com IAM DB Authentication e região fornecida
def create_gremlin_utils_with_iam(neptune_endpoint, neptune_port, aws_region):
    # Cria um objeto Endpoints com a região fornecida
    endpoints = Endpoints(
        neptune_endpoint=f'{neptune_endpoint}:{neptune_port}',
        region_name=aws_region
    )
    
    # Instancia o GremlinUtils usando o objeto Endpoints configurado com IAM DB Authentication
    gremlin_utils = GremlinUtils(endpoints)
    return gremlin_utils

# Parâmetros de configuração
neptune_endpoint = "your-neptune-endpoint.amazonaws.com"
neptune_port = 8182
aws_region = "us-west-2"

# Cria o GremlinUtils com IAM DB Authentication e região especificada
gremlin_utils = create_gremlin_utils_with_iam(neptune_endpoint, neptune_port, aws_region)

# Conecta ao Neptune
conn = gremlin_utils.remote_connection()
g = gremlin_utils.traversal_source(connection=conn)

# Executa a query para contar o número de nós
node_count = g.V().count().next()

# Fecha a conexão
conn.close()

# Exibe o resultado
print(f"Total de nós: {node_count}")

print('Exemplo 2')
GremlinUtils.init_statics(globals())

# Define o endpoint do cluster Neptune manualmente
endpoints = Endpoints(neptune_endpoint=neptune_endpoint)

# Cria uma instância do GremlinUtils usando o endpoint fornecido
gremlin_utils = GremlinUtils(endpoints)

# Conecta ao Neptune e cria a source de travessias (Gremlin Traversal)
conn = gremlin_utils.remote_connection()
g = gremlin_utils.traversal_source(connection=conn)

# Executa uma query para obter os primeiros 10 nós com suas propriedades
print(g.V().limit(10).valueMap().toList())

# Fecha a conexão
conn.close()

print('Exemplo 3')
GremlinUtils.init_statics(globals())

# Cria uma sessão boto3 e obtém as credenciais
session = boto3.session.Session()
credentials = session.get_credentials()

# Define o endpoint do Neptune e passa as credenciais explicitamente
endpoints = Endpoints(
    neptune_endpoint=neptune_endpoint,
    credentials=credentials)

# Cria uma instância do GremlinUtils com o endpoint e as credenciais fornecidas
gremlin_utils = GremlinUtils(endpoints)

# Conecta ao Neptune e cria a source de travessias (Gremlin Traversal)
conn = gremlin_utils.remote_connection()
g = gremlin_utils.traversal_source(connection=conn)

# Executa uma query para obter os primeiros 10 nós com suas propriedades
print(g.V().limit(10).valueMap().toList())

# Fecha a conexão
conn.close()