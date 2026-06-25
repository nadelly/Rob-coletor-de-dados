🤖 Robô de Coleta Automática de Dados DETER

📌 Sobre o projeto

Este projeto consiste em uma automação desenvolvida em Python para coleta diária de dados vetoriais disponibilizados pelo sistema DETER.

O robô realiza o download automático dos arquivos disponibilizados online, processa os dados compactados e organiza os arquivos para utilização em análises ambientais e geoespaciais.

O objetivo é reduzir atividades manuais repetitivas e garantir uma rotina padronizada de atualização dos dados.

🚀 Funcionalidades

- ✅ Acesso automático ao portal de dados do DETER
- ✅ Download diário dos arquivos vetoriais disponibilizados
- ✅ Gerenciamento de arquivos compactados (.zip)
- ✅ Extração automática dos dados geoespaciais
- ✅ Organização dos arquivos em diretórios de armazenamento
- ✅ Processamento de grandes volumes de dados vetoriais (600 mil+ registros)
- ✅ Execução automatizada por rotina agendada

🔄 Fluxo da automação
Portal DETER
↓
Download automático
↓
Arquivo vetorial compactado (.zip)
↓
Extração dos arquivos
↓
Armazenamento na rede
↓
Dados prontos para análise GIS
🛠️ Tecnologias utilizadas

- Python 3
- Requests
- Automação de arquivos
- Manipulação de dados geoespaciais
- Arquivos Shapefile (.shp)
- Rotinas agendadas no sistema operacional

📂 Estrutura do projeto

robo-deter/
│
├── robo_download.py # Script principal da automação
│
├── iniciar_robo.bat # Arquivo para iniciar execução automática
│
├── dados/
│ ├── zip/ # Arquivos baixados
│ └── shp/ # Arquivos extraídos
│
├── logs/
│ └── execucao.log # Histórico das execuções
│
└── README.md

▶️ Como executar

1. Instalar dependências

bash
pip install -r requirements.txt
2. Executar manualmente
python robo_download.py
3. Execução automática

O arquivo iniciar_robo.bat permite iniciar o robô automaticamente através do Agendador de Tarefas do Windows.
