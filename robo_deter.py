import requests
import zipfile
import os
import time
from datetime import datetime, timedelta
import pandas as pd
import urllib3
import shutil
from dbfread import DBF
import urllib.request
import json
import sys
import socket


# ======================================================
# CONFIGURAÇÃO PARA GITHUB
# ======================================================


USUARIO = "COLOQUE_SEU_USUARIO_AQUI"
SENHA = "COLOQUE_SUA_SENHA_AQUI"


LOGIN_URL = "https://terrabrasilis.dpi.inpe.br/app/security/realms/terrabrasilis-realm/protocol/openid-connect/token"

DOWNLOAD_URL = "https://terrabrasilis.dpi.inpe.br/file-delivery/download/deter-amz/shape"


# Pasta local do projeto
PASTA_BASE = os.path.join(os.getcwd(), "dados_deter")


PASTA_SAIDA = os.path.join(
    PASTA_BASE,
    "DADOS_DETER"
)

PASTA_SCRIPTS = os.path.join(
    PASTA_BASE,
    "SCRIPTS"
)

PASTA_TEMP = os.path.join(
    PASTA_BASE,
    "TEMP_DOWNLOAD"
)


ARQUIVO_AGENDA = os.path.join(
    PASTA_SCRIPTS,
    "agenda_retentativa.json"
)


ARQUIVO_DATA_TEMP = os.path.join(
    PASTA_TEMP,
    "ultima_data.txt"
)


urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)



# ======================================================
# VERIFICA INTERNET
# ======================================================

def check_internet():

    print("🔍 Verificando conexão...")

    try:
        socket.create_connection(
            ("terrabrasilis.dpi.inpe.br",443),
            timeout=5
        )

        print("✅ Conexão com INPE OK")
        return True

    except:

        pass


    try:
        urllib.request.urlopen(
            "https://www.google.com",
            timeout=5
        )

        print("✅ Internet OK")
        return True


    except:

        print("❌ Sem internet")
        return False
# ======================================================
# CRIAÇÃO DE PASTAS
# ======================================================

def criar_pastas():

    os.makedirs(PASTA_SAIDA, exist_ok=True)
    os.makedirs(PASTA_TEMP, exist_ok=True)
    os.makedirs(PASTA_SCRIPTS, exist_ok=True)



# ======================================================
# VERIFICA DADOS ATUAIS
# ======================================================

def verificar_dados_final_hoje():

    hoje = datetime.now().date()

    if not os.path.exists(PASTA_SAIDA):
        return False


    arquivos = os.listdir(PASTA_SAIDA)


    if not arquivos:
        return False



    contador = 0


    for arquivo in arquivos:

        caminho = os.path.join(
            PASTA_SAIDA,
            arquivo
        )

        try:

            data = datetime.fromtimestamp(
                os.path.getmtime(caminho)
            ).date()


            if data == hoje:
                contador += 1


        except:

            pass



    if contador >= 2:

        print(
            "✅ Dados de hoje já existem"
        )

        return True



    return False




# ======================================================
# VALIDA ZIP
# ======================================================


def verificar_zip(caminho):

    try:

        with zipfile.ZipFile(caminho,"r") as z:


            arquivos = z.namelist()


            shp = any(
                x.lower().endswith(".shp")
                for x in arquivos
            )


            dbf = any(
                x.lower().endswith(".dbf")
                for x in arquivos
            )


            return shp and dbf



    except:

        return False





# ======================================================
# EXTRAÇÃO SEGURA
# ======================================================


def extrair_zip(caminho_zip):

    print(
        "📦 Extraindo arquivos..."
    )


    temp_extract = os.path.join(
        PASTA_TEMP,
        "extracao_temp"
    )


    os.makedirs(
        temp_extract,
        exist_ok=True
    )


    try:


        with zipfile.ZipFile(
            caminho_zip,
            "r"
        ) as z:


            z.extractall(
                temp_extract
            )



        arquivos = os.listdir(
            temp_extract
        )


        if not arquivos:

            return False



        # limpa saída antiga

        if os.path.exists(PASTA_SAIDA):

            shutil.rmtree(
                PASTA_SAIDA
            )


        os.makedirs(
            PASTA_SAIDA
        )


        for arquivo in arquivos:


            origem = os.path.join(
                temp_extract,
                arquivo
            )


            destino = os.path.join(
                PASTA_SAIDA,
                arquivo
            )


            shutil.move(
                origem,
                destino
            )



        shutil.rmtree(
            temp_extract,
            ignore_errors=True
        )



        converter_dbf_csv()


        return True



    except Exception as e:


        print(
            f"Erro extração: {e}"
        )


        return False






# ======================================================
# CONVERTE DBF PARA CSV
# ======================================================


def converter_dbf_csv():


    print(
        "🔄 Convertendo DBF para CSV..."
    )


    for arquivo in os.listdir(
        PASTA_SAIDA
    ):


        if arquivo.lower().endswith(".dbf"):


            caminho = os.path.join(
                PASTA_SAIDA,
                arquivo
            )


            try:


                tabela = DBF(
                    caminho,
                    encoding="utf-8"
                )


                df = pd.DataFrame(
                    iter(tabela)
                )


                saida = os.path.join(
                    PASTA_SAIDA,
                    arquivo.replace(
                        ".dbf",
                        ".csv"
                    )
                )


                df.to_csv(
                    saida,
                    index=False
                )


                print(
                    f"✅ {arquivo} convertido ({len(df)} linhas)"
                )


            except Exception as e:

                print(
                    f"Erro CSV: {e}"
                )
# ======================================================
# DOWNLOAD DOS DADOS
# ======================================================

def baixar_dados():

    tentativas = 3


    for tentativa in range(1, tentativas + 1):

        print(
            f"\n🚀 Tentativa {tentativa}/{tentativas}"
        )


        try:

            session = requests.Session()


            payload = {
                "client_id":"terrabrasilis-apps",
                "grant_type":"password",
                "username":USUARIO,
                "password":SENHA
            }



            resposta = session.post(
                LOGIN_URL,
                data=payload,
                verify=False,
                timeout=60
            )


            token = resposta.json().get(
                "access_token"
            )


            if not token:

                print(
                    "❌ Falha no login"
                )

                continue



            print(
                "✅ Login realizado"
            )



            headers = {
                "Authorization":
                f"Bearer {token}"
            }



            print(
                "📥 Baixando dados DETER..."
            )


            arquivo = session.get(
                DOWNLOAD_URL,
                headers=headers,
                stream=True,
                verify=False,
                timeout=900
            )



            if arquivo.status_code != 200:

                print(
                    "❌ Erro no download"
                )

                continue




            nome = (
                f"deter_{datetime.now().strftime('%Y%m%d')}.zip"
            )


            caminho = os.path.join(
                PASTA_TEMP,
                nome
            )



            with open(
                caminho,
                "wb"
            ) as f:


                for bloco in arquivo.iter_content(
                    chunk_size=8192
                ):

                    if bloco:

                        f.write(bloco)




            tamanho = os.path.getsize(
                caminho
            )



            print(
                f"✅ Download concluído: {tamanho/1024/1024:.1f} MB"
            )



            if not verificar_zip(caminho):

                print(
                    "❌ ZIP inválido"
                )

                continue



            sucesso = extrair_zip(
                caminho
            )



            if sucesso:

                print(
                    "🎉 Processo concluído!"
                )

                return True



        except Exception as erro:


            print(
                f"⚠️ Erro: {erro}"
            )


            time.sleep(30)



    return False





# ======================================================
# PROGRAMA PRINCIPAL
# ======================================================


def executar():


    print("="*60)

    print(
        "🤖 ROBÔ AUTOMÁTICO DETER"
    )

    print(
        datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )
    )

    print("="*60)



    criar_pastas()



    if not check_internet():

        print(
            "Sem conexão."
        )

        return



    if verificar_dados_final_hoje():

        print(
            "⏭️ Base já atualizada."
        )

        return



    baixar_dados()





if __name__ == "__main__":


    executar()
