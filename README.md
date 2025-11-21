# 📊 Dashboard de Atendimentos STI - IPRN

> Análise de dados de atendimentos de TI com foco em transparência, anonimização e insights estratégicos

[![Demo](https://img.shields.io/badge/Live-Demo-22c55e?style=for-the-badge)](https://datapalacio.github.io/ti-data-analysis/)
[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://app.powerbi.com/view?r=eyJrIjoiOGY3MWMwMmMtNjU5Zi00ZGQ0LWI3OTctNGE2YmM1MTZlYmEyIiwidCI6ImQxODBiZjJiLTU5MTQtNGRkZC1hMDUyLWZhMmY3MTdmNmY4YyJ9)
[![Portfolio](https://img.shields.io/badge/Portfolio-Data_Palacio-22c55e?style=for-the-badge)](https://datapalacio.com.br/)

## 🎯 Sobre o Projeto

Dashboard interativo desenvolvido para visualizar e analisar atendimentos dos setores de informática da STI - IPRN. O projeto demonstra um pipeline completo de análise de dados: desde a anonimização até a apresentação web interativa.

> **⚠️ Nota sobre Privacidade:** Este projeto utiliza dados de órgão público que foram **integralmente anonimizados** para preservar a privacidade de usuários e a confidencialidade institucional. Informações sensíveis como nomes de servidores, dados pessoais (CPF, telefone, e-mail), localização específica de departamentos e termos internos foram removidos ou generalizados antes da publicação.

### 🔑 Destaques

- **Anonimização robusta** de dados sensíveis (nomes, e-mails, CPFs, telefones)
- **Dashboard Power BI** com métricas de produtividade e performance
- **Interface web responsiva** com tema dark/light
- **Código aberto** e documentado para fins educacionais
- **Conformidade LGPD** - Dados tratados conforme Lei Geral de Proteção de Dados

## 📂 Estrutura do Projeto

```
ti-data-analysis/
├── notebooks/
│   └── anonimizacao.py       # Script de anonimização de dados
├── maps/                      # Arquivos GeoJSON para visualização
├── reports/                   # Template do dashboard
├── data/                      # Datasets (não versionados)
├── config_anonimizacao.json   # Configuração de termos sensíveis
└── index.html                 # Landing page do projeto
```

## 🔒 Anonimização de Dados

### 🛡️ Por que Anonimizar?

Este projeto trabalha com dados reais de atendimentos de TI de um órgão público. Para possibilitar o compartilhamento educacional e transparência operacional **sem comprometer a privacidade**, implementamos um processo robusto de anonimização que:

- ✅ Remove identificadores diretos (nomes, CPFs, e-mails)
- ✅ Generaliza informações geográficas (preserva cidade, remove departamento)
- ✅ Mascara dados de contato (telefones, IPs, senhas)
- ✅ Substitui termos internos específicos do órgão
- ✅ Mantém utilidade analítica dos dados (padrões, tendências, métricas)

> **Importante:** O dataset original **nunca** é versionado no repositório. Apenas o código de anonimização e os dados já processados (anonimizados) são disponibilizados.

### Técnicas Aplicadas

O script `anonimizacao.py` implementa múltiplas camadas de proteção:

| Tipo de Dado | Técnica | Exemplo |
|--------------|---------|---------|
| **Nomes** | Hash MD5 (8 chars) | `João Silva` → `USER_a3f5b8c1` |
| **E-mails** | Mascaramento | `user@email.com` → `[EMAIL_REMOVIDO]` |
| **Telefones** | Regex + Replace | `(84) 99999-9999` → `[TELEFONE_REMOVIDO]` |
| **CPFs** | Pattern matching | `123.456.789-00` → `[CPF_REMOVIDO]` |
| **IPs** | Mascaramento | `192.168.0.1` → `[IP_REMOVIDO]` |
| **Senhas** | Detecção heurística | `senha: abc123` → `senha: [SENHA_REMOVIDA]` |
| **Matrículas** | Pattern matching | `Mat. 123.456-7` → `[MATRICULA_REMOVIDA]` |
| **Localização** | Generalização | `Natal > Depto X` → `Natal` |
| **Termos Internos** | Lista configurável | `SIGLA_ORGAO` → `[TERMO_INTERNO]` |
| **URLs Internas** | Mascaramento | `http://sistema.interno` → `[URL_REMOVIDA]` |

### Uso do Script

```bash
# Instalar dependências
pip install pandas

# Configurar termos sensíveis específicos (opcional)
# Editar config_anonimizacao.json com siglas e termos do órgão

# Executar anonimização
python notebooks/anonimizacao.py
```

**Input:** `data/all_dti_processed.csv` (dados brutos - **NÃO versionado**)  
**Output:** `data/all_dti_anonymized.csv` (dados anonimizados)

### Funções Principais

```python
anonymize_name(name)        # Hash MD5 de nomes → identificador único
scrub_text(text)            # Limpeza agressiva de textos livres
generalize_location(loc)    # Generalização geográfica
```

### Arquivo de Configuração

O arquivo `config_anonimizacao.json` permite personalizar a remoção de termos sensíveis:

```json
{
  "sensitive_terms": [
    "SIGLA_ORGAO",
    "SISTEMA_INTERNO",
    "TERMO_ESPECIFICO"
  ]
}
```

## 📊 Dashboard Power BI

### Métricas Disponíveis

- **Produtividade por Setor**: Volume de atendimentos por equipe
- **Padrões Temporais**: Análise de sazonalidade e dias de maior demanda
- **Distribuição Geográfica**: Mapa de calor por cidades do RN
- **Status de Atendimento**: Funil de chamados (abertos, em andamento, fechados)
- **Performance SLA**: Cumprimento de prazos por categoria

### Tecnologias BI

- **Power Query**: ETL e transformação de dados
- **DAX**: Medidas calculadas e KPIs
- **Visualizações Customizadas**: Mapas, gráficos e cards dinâmicos

## 🌐 Landing Page

Interface web responsiva desenvolvida com:

- **Tailwind CSS**: Estilização moderna e responsiva
- **Lucide Icons**: Ícones SVG otimizados
- **Dark/Light Mode**: Alternância de tema com persistência
- **Power BI Embed**: Dashboard integrado via iframe

## 🚀 Como Usar

### 1. Clone o Repositório

```bash
git clone https://github.com/dataPalacio/ti-data-analysis.git
cd ti-data-analysis
```

### 2. Prepare os Dados

```bash
# Coloque seus dados brutos em data/all_dti_processed.csv
# IMPORTANTE: Não versione dados sensíveis!

# Execute a anonimização
python notebooks/anonimizacao.py
```

### 3. Visualize Localmente

```bash
# Abra index.html em um navegador
# Ou use um servidor local:
python -m http.server 8000
# Acesse: http://localhost:8000
```

## 📈 Resultados

### Insights Gerados

- **60% de redução** no tempo de análise manual
- Identificação de **padrões temporais** de demanda
- **15% de aumento** na eficiência operacional
- Visualização geográfica de **167 municípios** do RN

## 🛠️ Stack Técnica

| Camada | Tecnologia |
|--------|------------|
| **Processamento** | Python, Pandas, Regex |
| **BI** | Power BI, DAX, Power Query |
| **Frontend** | HTML5, Tailwind CSS, JavaScript |
| **Deploy** | GitHub Pages |

## 🔐 Política de Privacidade

Este projeto adota as seguintes práticas:

- ❌ **Dados brutos nunca são versionados** no GitHub
- ✅ Apenas dados anonimizados são publicados
- ✅ Script de anonimização é open-source para auditoria
- ✅ Conformidade com LGPD (Lei 13.709/2018)
- ✅ Uso exclusivo para fins educacionais e análise agregada

## 📝 Licença

Este projeto está sob a licença MIT. Consulte [LICENSE](LICENSE) para mais informações.

## 👤 Autor

**Gustavo Palacio** - Analista de Dados

- 🌐 Website: [datapalacio.com.br](https://datapalacio.com.br)
- 💼 Portfolio: [Projetos e Artigos](https://datapalacio.com.br/#projects)
- 📧 Contato: [palacio.dados@gmail.com](mailto:palacio.dados@gmail.com)
- 🐙 GitHub: [@dataPalacio](https://github.com/dataPalacio)
- 💼 LinkedIn: [gfpalacio](https://www.linkedin.com/in/gfpalacio/)

---

<div align="center">

**Desenvolvido com 💚 e dados**

[🌐 Visite meu Portfolio](https://datapalacio.com.br) • [📊 Ver Demo](https://datapalacio.github.io/ti-data-analysis/) • [🐛 Reportar Bug](https://github.com/dataPalacio/ti-data-analysis/issues)

</div>