import logging
import os

# Define o diretório e o nome do arquivo de log
log_directory = 'C:/Users/IAGO/Documents/Projeto desktop/Projeto/build/Logging'
filename = 'Login_Logs.txt'
log_path = os.path.join(log_directory, filename)

# Cria o diretório se ele não existir
os.makedirs(log_directory, exist_ok=True)

# Configuração do logging
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
