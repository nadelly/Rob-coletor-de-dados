🤖 DETER Data Automation Pipeline

Automação em Python para coleta, processamento e atualização diária de dados vetoriais do sistema DETER (INPE/TerraBrasilis).

O robô realiza todo o fluxo de aquisição dos dados ambientais, desde a autenticação na plataforma, download do arquivo compactado, validação, extração do shapefile e conversão da tabela espacial para CSV.

O objetivo é automatizar a atualização de bases geoespaciais utilizadas em análises ambientais e sistemas de informação geográfica (SIG).

📌 Visão geral do fluxo

TerraBrasilis / INPE
|
↓
Autenticação automática
|
↓
Download diário do arquivo vetorial
|
↓
Validação do ZIP
|
↓
Extração segura do Shapefile
|
↓
Conversão DBF → CSV
|
↓
Atualização da base espacial

🚀 Funcionalidades

🔐 Autenticação
- Login automático utilizando token de acesso
- Comunicação segura com a API do TerraBrasilis

📥 Download automatizado
- Download dos arquivos vetoriais DETER
- Suporte para arquivos grandes utilizando streaming
- Salvamento automático em rede

🛡️ Validação dos dados

Antes de atualizar a base o robô verifica:

- Existência do arquivo ZIP
- Integridade do arquivo compactado
- Presença dos componentes essenciais do shapefile:
  - `.shp`
  - `.dbf`

🧹 Processamento dos dados

Após o download:

1. O arquivo é extraído em uma pasta temporária
2. Os arquivos são validados
3. Dados antigos são removidos
4. A nova versão é publicada na pasta final
5. Arquivos DBF são convertidos para CSV


🔄 Controle inteligente de atualização

O robô verifica:

- Se os dados do dia já existem
- Se o download foi concluído anteriormente
- Se existe algum arquivo temporário válido

Caso a base já esteja atualizada, evita novo download.

🔁 Sistema de retentativa

Em caso de falha:

- registra a tentativa
- aguarda intervalo programado
- realiza novas tentativas automaticamente

Intervalos configurados:


1ª tentativa → imediata
2ª tentativa → 30 minutos
3ª tentativa → 2 horas
4ª tentativa → 6 horas

🛠️ Tecnologias utilizadas

- Python 3
- Requests
- Pandas
- Zipfile
- DBFRead
- Manipulação de arquivos
- Automação Windows (.bat)
- Dados geoespaciais

📂 Estrutura do projeto

deter-data-automation/

│
├── robo_deter.py
│
├── iniciar_robo.bat
│
├── requirements.txt
│
├── temp/
│
├── dados/
│ ├── shapefile/
│ └── csv/
│
└── README.md

▶️ Execução

Execução manual:

```bash
python robo_deter.py

Execução automática:

O arquivo .bat pode ser configurado no Agendador de Tarefas do Windows para executar diariamente.

🌎 Aplicações

Este projeto pode ser utilizado em:

Monitoramento ambiental
Fiscalização territorial
Geoprocessamento
Atualização automática de bases SIG
Sistemas de apoio à decisão ambiental
👩‍💻 Autora

Nadelly Gama da Silva

Engenharia Ambiental
Python | Geoprocessamento | Dados Ambientais
