Tomando como base o sistema Manjaro (Arch Linux) atualizado em 18/11/2015

Instalar o PIP:
	Baixar o arquivo abaixo e salvá-lo no sistema, e acesse essa pasta pelo terminal:
	- https://bootstrap.pypa.io/get-pip.py

	Instalar o Virtual PIP:
	- sudo python get-pip.py

	Instalar o Virtual Env:
	- sudo pip install virtualenv

Acessar a pasta do projeto:
- cd pasta/do/projeto/SCC0241_datamart

Criar o ambiente virtual:
- virtualenv env --python python3
(se der problema nesse ponto é porque o Python 3 não está instalado no sistema)

Ativar o ambiente virtual:
- source env/bin/activate

Instalar dependências do sistema:
- yaourt -S fontconfig     # (possivelmente este pacote já existe no sistema)
- yaourt -S wkhtmltopdf

Instalar o software da Oracle:
	Abrir o arquivo de configurações do Pacman:
	- sudo subl3 /etc/pacman.conf

	Incluir linhas no final do arquivo (tudo o que está entre os símbolos ```, mas sem incluir esses símbolos):
	```
	[oracle]
	SigLevel = Optional TrustAll
	Server = http://linux.shikadi.net/arch/$repo/$arch/
	```

	Atualizar os repositórios do Pacman:
	- sudo pacman -Sy

	Instalar o Instant Client SDK:
	- yaourt -S oracle-instantclient-sdk

Instalar pacotes do Python:
- pip install -r requirements.txt

Rodar o servidor:
- python manage.py runserver



A variável LIMIT_QUERY em settings.py na pasta labbd representa a quantidade máxima de dados a serem carregados no html. Caso seja None todos serão carregados.  
Quando todos são carregados, o html fica bem pesado.