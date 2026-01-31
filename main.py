import pandas as pd
import requests
import unicodedata
import os
import re

# --- CONFIGURAÇÕES ---
CLOUDFLARE_ACCOUNT_ID = "COLOCA SEU ID AQUI"
CLOUDFLARE_TOKEN = "COLOCA SEU TOKEN AQUI"

ARQUIVO_ENTRADA = "inputs/exercicios.csv"
ARQUIVO_SAIDA = "outputs/planilha_final_completa.csv"
ARQUIVO_RELATORIO = "outputs/relatorio_nao_encontrados.txt"

def normalizar_texto(texto):
    """Limpa o nome para garantir o match, removendo sufixos como (2)."""
    if not isinstance(texto, str):
        return ""
    
    # 1. Remove aspas e aspas triplas
    texto = texto.replace('"""', '').replace('"', '').replace("'", "")
    
    # 2. Remove extensão
    texto = texto.lower().replace('.mp4', '').replace('.mov', '')
    
    # 3. SEGURANÇA: Remove sufixos de cópia como (2), (3)
    # Ex: "exercicio (2)" vira "exercicio"
    texto = re.sub(r'\(\d+\)', '', texto)
    
    # 4. Normaliza acentos
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    
    # 5. Espaços
    return " ".join(texto.split())

def buscar_videos_api():
    print("🔄 Baixando catálogo do Cloudflare (isso garante dados 100% reais)...")
    url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/stream"
    headers = {"Authorization": f"Bearer {CLOUDFLARE_TOKEN}"}
    
    mapa = {}
    url_next = url
    total = 0
    
    while url_next:
        try:
            r = requests.get(url_next, headers=headers)
            data = r.json()
            if not data.get('success'): break
            
            lista = data.get('result', [])
            if not lista: break
            
            for v in lista:
                # Tenta pegar o nome de vários lugares possíveis
                nome = v.get('meta', {}).get('name') or v.get('name') or ""
                uid = v.get('uid')
                if nome and uid:
                    chave = normalizar_texto(nome)
                    mapa[chave] = uid
            
            total += len(lista)
            print(f"   📥 Baixados até agora: {total}")
            
            if len(lista) < 10: break # Fim da lista
            break # REMOVA ESTA LINHA SE TIVER MAIS DE 1000 VÍDEOS (Cloudflare entrega 1000 por padrão)
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            break
            
    return mapa

def main():
    print("🚀 Iniciando processamento...")
    
    # Carregar Planilha
    try:
        df = pd.read_csv(ARQUIVO_ENTRADA)
    except:
        print("❌ Erro: Não achei o arquivo 'inputs/exercicios.csv'")
        return

    if 'video_id' not in df.columns: df['video_id'] = ""

    # Buscar API
    mapa = buscar_videos_api()
    print(f"✅ Catálogo Cloudflare: {len(mapa)} vídeos na memória.")

    # Cruzar
    encontrados = 0
    nao_achados = []
    
    coluna_nome = 'original_file_name' # Nome da coluna na sua planilha
    
    for i, row in df.iterrows():
        nome_orig = str(row[coluna_nome])
        chave = normalizar_texto(nome_orig)
        
        if chave in mapa:
            df.at[i, 'video_id'] = mapa[chave]
            encontrados += 1
        else:
            if nome_orig != "nan":
                nao_achados.append(nome_orig)

    # Salvar
    if not os.path.exists('outputs'): os.makedirs('outputs')
    df.to_csv(ARQUIVO_SAIDA, index=False)
    
    with open(ARQUIVO_RELATORIO, 'w', encoding='utf-8') as f:
        f.write(f"Não encontrados: {len(nao_achados)}\n")
        for item in nao_achados: f.write(f"{item}\n")

    print("\n" + "="*30)
    print(f"🏁 FINALIZADO!")
    print(f"✅ Vídeos Cruzados com Sucesso: {encontrados}")
    print(f"⚠️ Não encontrados: {len(nao_achados)}")
    print(f"📂 Verifique o arquivo: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    main()