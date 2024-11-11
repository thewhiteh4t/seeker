import os
import subprocess
import urllib.request
import shutil
import seeker

def download_html(url, userconfigpath, user_agent, proxy_config=None):
    # Verificar se o wget está disponível no sistema
    wget_available = shutil.which('wget') is not None

    if os.path.exists(url):
        print(f'O caminho fornecido é um arquivo local: {url}')
        # Copiar o arquivo diretamente para o diretório de hospedagem
        try:
            save_path = os.path.join(userconfigpath, 'web_clone', 'index.html')
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            shutil.copyfile(url, save_path)
            print(f'Arquivo {url} copiado com sucesso para {save_path}')
        except Exception as e:
            print(f"Erro ao copiar o arquivo: {e}")
    else:
        if not wget_available:
            print("Wget não está disponível, utilizando urllib...")
            # Usar urllib como fallback caso o wget não esteja instalado
            try:
                request = urllib.request.Request(url, headers={'User-Agent': user_agent})
                response = urllib.request.urlopen(request)
                html_content = response.read()

                # Salvar o conteúdo HTML baixado
                save_path = os.path.join(userconfigpath, 'web_clone', 'index.html')
                os.makedirs(os.path.dirname(save_path), exist_ok=True)

                with open(save_path, 'wb') as f:
                    f.write(html_content)

                print(f'HTML salvo com sucesso em {save_path}')
            except Exception as e:
                print(f"Erro ao baixar HTML com urllib: {e}")
        else:
            print("Wget está disponível, utilizando wget para baixar o HTML...")

            # Caso o wget esteja disponível, executa com base nas configurações fornecidas
            if check_config("WGET_DEEP").lower() == "on":
                command = '%s;wget -H -N -k -p -l 2 -nd -P template/custom_og_tags --no-check-certificate -U "%s" "%s"' % (
                    proxy_config if proxy_config else '', user_agent, url)
            else:
                command = '%s;cd template/custom_og_tags;wget --no-check-certificate -O index.html -c -k -U "%s" "%s"' % (
                    proxy_config if proxy_config else '', user_agent, url)

            try:
                subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
                print("HTML baixado com sucesso usando wget.")
            except Exception as e:
                print(f"Erro ao executar wget: {e}")

# Exemplo de uso
user_agent = "Mozilla/5.0"
proxy_config = None  # Caso tenha um proxy, pode ser passado aqui
url = input("Digite a URL ou caminho para clonar: ")
port = input("Digite a porta em que vai hospedar o HTML: ")  # Corrigido para não converter diretamente para int
userconfigpath = "template/custom_og_tags"

# Baixar ou copiar o HTML
download_html(url, userconfigpath, user_agent, proxy_config)

# Hospedar o HTML usando o seeker (assumindo que seeker.py está configurado corretamente)
try:
    subprocess.Popen(f"python seeker.py -t {userconfigpath} -p {port}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
    print(f"Seeker iniciado na porta {port}")
except Exception as e:
    print(f"Erro ao iniciar o seeker: {e}")
