import pandas as pd
import re
import hashlib
import os
from pathlib import Path

# Configurações de Arquivo - resolvendo caminhos relativos ao arquivo deste script
BASE_DIR = Path(__file__).resolve().parent
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
    Realiza uma limpeza agressiva para dados públicos.
    """
    if pd.isna(text):
        return text

    text = str(text)

    # 0. Remover cabeçalhos de e-mail comuns (De:, Para:, Assunto:)
    # Remove linhas inteiras que parecem cabeçalhos
    text = re.sub(
        r'(?m)^(De|Para|From|To|Assunto|Subject|Enviada em|Sent):.*$', '', text)

    # 0.1 Preservar Cabeçalhos de Formulário (Whitelist)
    # Substitui por tokens temporários para não serem removidos pela limpeza de nomes
    headers_whitelist = [
        'DADOS DO FORMULÁRIO',
        'INFORMAÇÕES OBRIGATÓRIAS',
        'O QUE DESEJA SOLICITAR',
        'INFORME ONDE VOCÊ ESTÁ LOTADO',
        'TELEFONE DE CONTATO',
        'TELEFONE PARA CONTATO',
        'DESCRIÇÃO DO PROBLEMA',
        'INFORMAÇÕES ADICIONAIS',
        'LOTAÇÃO',
        'ANEXO',
        'SOLICITANTE',
        'CARGO',
        'MOTIVAÇÃO',
        'SOFTWARE/SISTEMA A SER INSTALADO',
        'NOME OU ENDEREÇO IP DA ESTAÇÃO DE TRABALHO'
    ]

    placeholders = {}
    for i, header in enumerate(headers_whitelist):
        token = f"__HEADER_{i}__"
        placeholders[token] = header
        # Case insensitive replace
        text = re.sub(r'(?i)' + re.escape(header), token, text)

    # 1. Mascarar E-mails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_REMOVIDO]', text)

    # 2. Mascarar Telefones (Formatos com ou sem DDD, com ou sem hífen)
    # Ex: (84) 99999-9999, 84 9999-9999, 99999999
    text = re.sub(
        r'(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[- ]?\d{4}\b', '[TELEFONE_REMOVIDO]', text)

    # 3. Mascarar CPF (Padrão XXX.XXX.XXX-XX)
    text = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF_REMOVIDO]', text)

    # 4. Mascarar Endereços IP
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP_REMOVIDO]', text)

    # 5. Mascarar Senhas (Heurística: procura por "senha:" seguido de valor)
    text = re.sub(
        r'(?i)(senha|password)(\s*[:=]?\s*)(\S+)', r'\1\2[SENHA_REMOVIDA]', text)

    # 6. Mascarar Matrículas e Logins
    # Ex: Mat. 123.456-7, Matrícula 123456
    text = re.sub(
        r'(?i)(matr[íi]cula|mat\.?)\s*[:=]?\s*[\d\.-]+', '[MATRICULA_REMOVIDA]', text)
    # Ex: Login: usuario.nome
    text = re.sub(
        r'(?i)(login|usu[áa]rio)\s*[:=]?\s*[\w\.]+', '[LOGIN_REMOVIDO]', text)

    # 7. Remover Siglas e Termos Internos Sensíveis (Agressivo - remove mesmo dentro de palavras)
    # Lista de termos identificados
    sensitive_terms = [
        'MPRN', 'PGJ', 'GAU', 'DINFRA', 'GMAP', 'CAOP', 'DGEP',
        'PJe', 'GLPI', 'VPN', 'Intranet', 'Checkpoint', 'Atende MP'
    ]
    for term in sensitive_terms:
        # Case insensitive replace for terms, NO word boundaries to catch suffixes/prefixes
        text = re.sub(r'(?i)' + re.escape(term), '[TERMO_INTERNO]', text)

    # 8. Mascarar URLs
    text = re.sub(r'http[s]?://\S+', '[URL_REMOVIDA]', text)

    # 9. Limpeza Agressiva de Nomes Próprios (Heurística Melhorada)
    # Regex para nomes em Title Case (Ex: João da Silva, Ana B. Costa)
    # [A-ZÀ-ÖØ-Ý] -> Letras maiúsculas incluindo acentos
    # [a-zà-öø-ý] -> Letras minúsculas incluindo acentos
    # Permite conectivos (de, da, do, e) e iniciais

    name_pattern_title = r'\b[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]+(?:\s+(?:[dD][aeo]s?|e|[A-ZÀ-ÖØ-Ý]\.?|[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]+)){1,5}\b'
    text = re.sub(name_pattern_title, '[NOME_REMOVIDO]', text)

    # Regex para nomes em ALL CAPS (Ex: JOAO DA SILVA)
    # Evita siglas curtas (min 3 letras por palavra)
    name_pattern_caps = r'\b[A-ZÀ-ÖØ-Ý]{3,}(?:\s+(?:[DE]?[AO]S?|[A-ZÀ-ÖØ-Ý]{3,})){1,5}\b'
    text = re.sub(name_pattern_caps, '[NOME_REMOVIDO]', text)

    # 10. Restaurar Cabeçalhos
    for token, header in placeholders.items():
        text = text.replace(token, header)

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
        print(
            f"Arquivo '{INPUT_FILE}' carregado com sucesso. {len(df)} registros encontrados.")
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
        df['requerente_anonymized'] = df['requerente_requerente'].apply(
            anonymize_name)
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
    df['localizacao_generalizada'] = df['localizacao'].apply(
        generalize_location)

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
    print(
        f"Sucesso! Arquivo anonimizado salvo como '{OUTPUT_FILE}' com {len(df_final.columns)} colunas.")


if __name__ == "__main__":
    main()
