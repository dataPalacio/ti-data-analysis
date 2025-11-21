import pandas as pd
import re
import hashlib
import os
from pathlib import Path

# Configurações de Arquivo - resolvendo caminhos relativos ao arquivo deste script
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / 'data' / 'all_dti_processed.csv'
OUTPUT_FILE = BASE_DIR / 'data' / 'all_dti_anonymized.csv'

def anonymize_name(name):
    """
    Substitui nomes reais por um hash (código único).
    Isso permite contagem de chamados por usuário sem revelar a identidade.
    """
    if pd.isna(name):
        return name
    # Cria um hash MD5 e pega os primeiros 8 caracteres
    hash_object = hashlib.md5(str(name).encode())
    return f"USER_{hash_object.hexdigest()[:8]}"

def scrub_text(text):
    """
    Remove dados sensíveis de textos livres (descrição e título) usando Regex.
    """
    if pd.isna(text):
        return text
    
    text = str(text)
    
    # 1. Mascarar E-mails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_REMOVIDO]', text)
    
    # 2. Mascarar Telefones (Formatos com ou sem DDD, com ou sem hífen)
    # Ex: (84) 99999-9999, 84 9999-9999, 99999999
    text = re.sub(r'(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[- ]?\d{4}\b', '[TELEFONE_REMOVIDO]', text)
    
    # 3. Mascarar CPF (Padrão XXX.XXX.XXX-XX)
    text = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF_REMOVIDO]', text)
    
    # 4. Mascarar Endereços IP
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP_REMOVIDO]', text)
    
    # 5. Mascarar Senhas (Heurística: procura por "senha:" seguido de valor)
    text = re.sub(r'(?i)(senha|password)(\s*[:=]?\s*)(\S+)', r'\1\2[SENHA_REMOVIDA]', text)
    
    return text

def generalize_location(loc):
    """
    Remove a especificidade do departamento, mantendo apenas a unidade principal.
    Ex: 'Natal > Depto X' vira apenas 'Natal'.
    """
    if pd.isna(loc):
        return loc
    # Pega apenas a primeira parte antes do separador '>'
    parts = str(loc).split('>')
    return parts[0].strip()

def main():
    print("Iniciando processo de anonimização...")
    
    # Carregar dados
    try:
        # Tenta carregar com separador padrão ;
        df = pd.read_csv(str(INPUT_FILE), sep=';')
        print(f"Arquivo '{INPUT_FILE}' carregado com sucesso. {len(df)} registros encontrados.")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{INPUT_FILE}' não encontrado.")
        print(f"Procure em: {BASE_DIR / 'data'}")
        return
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return

    # Aplicar transformações
    print("Anonimizando nomes...")
    # Verifica se as colunas existem antes de aplicar para evitar erros se o nome mudar
    if 'requerente_requerente' in df.columns:
        df['requerente_anonymized'] = df['requerente_requerente'].apply(anonymize_name)
    else:
        print("Aviso: Coluna 'requerente_requerente' não encontrada. Pulando...")
        
    if 'responsavel' in df.columns:
        df['responsavel_anonymized'] = df['responsavel'].apply(anonymize_name)
    else:
        print("Aviso: Coluna 'responsavel' não encontrada. Pulando...")

    print("Limpando textos sensíveis (pode demorar um pouco)...")
    df['descricao_sanitized'] = df['descricao'].apply(scrub_text)
    df['titulo_sanitized'] = df['titulo'].apply(scrub_text)

    print("Generalizando localizações...")
    df['localizacao_generalizada'] = df['localizacao'].apply(generalize_location)

    # Lista de colunas para manter no arquivo final
    # Atualizado para incluir colunas geradas pelo main.py (IBGE/Normalização)
    columns_to_keep = [
        'id', 
        'titulo_sanitized', 
        'data_de_abertura', 
        'status', 
        'data_de_fechamento',
        'requerente_anonymized', 
        'categoria', 
        'localizacao_generalizada',
        'descricao_sanitized', 
        'atribuido_grupo_tecnico', 
        'cidade', 
        'responsavel_anonymized', 
        'qtd_monitor',
        # Novas colunas preservadas do processamento anterior (main.py)
        'cidade_normalizada',
        'cidade_ibge',
        'codigo_ibge'
    ]

    # Filtra apenas colunas que realmente existem no DataFrame para evitar KeyErrors
    existing_columns = [col for col in columns_to_keep if col in df.columns]
    
    # Renomear para nomes mais amigáveis se necessário
    # Mapeamento De -> Para
    rename_map = {
        'titulo_sanitized': 'titulo',
        'requerente_anonymized': 'requerente_id',
        'localizacao_generalizada': 'localizacao',
        'descricao_sanitized': 'descricao',
        'responsavel_anonymized': 'responsavel_id'
    }

    df_final = df[existing_columns].rename(columns=rename_map)

    # Salvar arquivo
    df_final.to_csv(str(OUTPUT_FILE), index=False, sep=';')
    print(f"Sucesso! Arquivo anonimizado salvo como '{OUTPUT_FILE}' com {len(df_final.columns)} colunas.")

if __name__ == "__main__":
    main()