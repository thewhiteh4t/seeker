import os
import subprocess
import urllib.request
import seeker

def download_html(url, userconfigpath, user_agent, proxy_config=None):
    # Verificar se o wget está disponível no sistema
    wget_available = shutil.which('wget') is not None

    if not wget_available:
        print("Wget não está disponível, utilizando urllib...")
        # Usar urllib como fallback caso o wget não esteja instalado
        try:
            request = urllib.request.Request(url, headers={'User-Agent': user_agent})
            response = urllib.request.urlopen(request)
            html_content = response.read()

            # Salvar o conteúdo HTML baixado
            save_path = os.path.join(userconfigpath, 'web_clone/index.html')
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
            command = '%s;wget -H -N -k -p -l 2 -nd -P %s/web_clone/ --no-check-certificate -U "%s" "%s"' % (
                proxy_config if proxy_config else '', userconfigpath, user_agent, url)
        else:
            command = '%s;cd %s/web_clone/;wget --no-check-certificate -O index.html -c -k -U "%s" "%s"' % (
                proxy_config if proxy_config else '', userconfigpath, user_agent, url)

        try:
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).wait()
            print("HTML baixado com sucesso usando wget.")
        except Exception as e:
            print(f"Erro ao executar wget: {e}")

# Exemplo de uso
user_agent = "Mozilla/5.0"
proxy_config = None  # Caso tenha um proxy, pode ser passado aqui
url = input("Digite a URL/HOST para clonar: ")
userconfigpath = input("caminho para salvar: ")
download_html(url, userconfigpath, user_agent, proxy_config)
