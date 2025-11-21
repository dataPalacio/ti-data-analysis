# 📊 Dashboard de Atendimentos STI - IPRN

> Análise de dados de atendimentos de TI com foco em transparência, anonimização e insights estratégicos

[![Demo](https://img.shields.io/badge/Live-Demo-22c55e?style=for-the-badge)](https://datapalacio.github.io/ti-data-analysis/)
[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://app.powerbi.com/view?r=eyJrIjoiOGY3MWMwMmMtNjU5Zi00ZGQ0LWI3OTctNGE2YmM1MTZlYmEyIiwidCI6ImQxODBiZjJiLTU5MTQtNGRkZC1hMDUyLWZhMmY3MTdmNmY4YyJ9)

## 🎯 Sobre o Projeto

O projeto nasceu de uma necessidade estratégica: estabelecer monitoramento e visualização claros da produtividade e identificar as lacunas existentes no setor de TI.

Anteriormente, a ausência de métricas e visuais dedicados dificultava a percepção de gargalos nos atendimentos de informática. Este Dashboard preenche essa lacuna, fornecendo os insights necessários para aprimorar a gestão do serviço, otimizar recursos e direcionar o planejamento estratégico da STI - IPRN.
> **⚠️ Nota sobre Privacidade:** Este projeto utiliza dados de órgão público que foram **integralmente anonimizados** para preservar a privacidade de usuários e a confidencialidade institucional. Informações sensíveis como nomes de servidores, dados pessoais (CPF, telefone, e-mail), localização específica de departamentos e termos internos foram removidos ou generalizados antes da publicação.

1. 🔍 O Desafio (O Problema de Negócio)

> O órgão enfrentava desafios na gestão de  **Chamados de TI** , com pouca visibilidade sobre a real demanda de trabalho da equipe de suporte e a distribuição geográfica dos problemas. Buscamos responder a três questões cruciais:

1. Qual é o **Setor** com o maior volume de atendimentos e qual a prioridade real dos problemas?
2. Quais são os **Meses e Localidades** com maior concentração de demanda, impactando o custo logístico de deslocamento?
3. Qual é o **Problema Mais Comum** de cada setor de informática para subsidiar decisões de investimento e pessoal?

#### 2. 🛠️ A Solução (Meu papel de Analista)

> Utilizando **Python** para processamento de dados (incluindo anonimização e tratamento geoespacial) e o **Power BI** para visualização, desenvolvi um painel de inteligência gerencial. Minhas principais entregas foram:

* **Priorização com Pareto:** Apliquei a regra 80/20, usando um Gráfico de Pareto para filtrar chamados por setor e identificar quais recebiam $80\%$ da demanda.
* **Análise Geoespacial e Visual:** Criei um **Mapa de Calor em Gradiente** no painel (seguindo as cores da identidade visual da Instituição) para agrupar demandas por cidade, e um Gráfico de Área para mapear a evolução da demanda mensal ao longo de 2025.
* **Detalhamento Setorial:** Desmembrei o painel em páginas específicas para cada setor, aprofundando a visualização dos principais problemas.

#### 3. 🚀 As Descobertas (O Impacto Estratégico)

> A análise revelou *insights* críticos para a gestão de custos e o planejamento de recursos humanos:

* **Dependência do Nível 2 e Risco de Pessoal:** A maior parte da demanda é atendida pelo Nível 2 (presencial/remoto). Sem a presença dos  **6 estagiários** , apenas **2 terceirizados** precisariam cobrir as **3007 demandas anuais do SAU** , expondo a área a um alto risco de interrupção do serviço.
* **Foco Geográfico de Alto Custo:** O **Mapa de Calor** provou que Natal e Mossoró (e suas respectivas regiões metropolitanas) concentram a maior demanda, sugerindo a necessidade de rever a estratégia de deslocamento, que está elevando os custos de viagem e combustível.
* **Gargalo de Licitação e SLA:** O setor SAU, sozinho, concentra $62\%$ da demanda em apenas duas categorias críticas. O problema de **Solicitação de Equipamento** é um grave gargalo no SLA, pois $21\%$** dos chamados não são resolvidos** devido à morosidade do processo de licitação e compra de monitores e computadores.
* **Decisão Estratégica Sugerida:** A alta demanda por **Serviços de Impressão** levou a uma proposta de estudo de viabilidade para a contratação de serviços de **Outsourcing**, visando mitigar a dependência de manutenção e reposição de peças.

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

## 🔄 Entenda o Projeto

### Pipeline: Da Extração à Visualização

```mermaid
graph LR
    A[🔌 Extração] --> B[🧹 Tratamento]
    B --> C[🔒 Anonimização]
    C --> D[📊 Visualização]
```

#### 1. **🔌 Extração de Dados**
Coleta automatizada de tickets do sistema GLPI via **Selenium** e **Python**.
> ⚠️ *Script não publicado por conter credenciais e endpoints internos do órgão*

#### 2. **🧹 Tratamento de Dados**
Processamento com **Pandas** para limpeza, normalização e estruturação.
- Tratamento de valores nulos
- Padronização de datas e categorias
- Normalização de nomes de cidades

📁 *Implementação similar ao projeto:* [support-tickets-analytics](https://github.com/dataPalacio/support-tickets-analytics/blob/main/scripts/main.py)

#### 3. **🔒 Anonimização**
Execução do [`anonimizacao.py`](notebooks/anonimizacao.py) para proteção de dados sensíveis:
- Hash de identificadores pessoais
- Mascaramento de contatos e documentos
- Generalização de localizações
- Remoção de termos internos do órgão

#### 4. **📊 Visualização**
Integração com dados geográficos do **IBGE** e publicação no **Power BI**.
- Enriquecimento com códigos de municípios
- Modelagem dimensional (Star Schema)
- Dashboard público interativo

🔗 [Ver Dashboard ao Vivo](https://app.powerbi.com/view?r=eyJrIjoiOGY3MWMwMmMtNjU5Zi00ZGQ0LWI3OTctNGE2YmM1MTZlYmEyIiwidCI6ImQxODBiZjJiLTU5MTQtNGRkZC1hMDUyLWZhMmY3MTdmNmY4YyJ9)

---


## 📋 Estrutura dos Dados

Para garantir o funcionamento correto dos scripts de anonimização e do dashboard, o dataset de entrada (`data/all_dti_processed.csv`) deve seguir o esquema abaixo:

### Dicionário de Dados

| Coluna | Tipo | Descrição | Exemplo |
| :--- | :---: | :--- | :--- |
| `id` | `int` | Identificador único do chamado (GLPI) | `15432` |
| `data_abertura` | `datetime` | Data e hora de criação do ticket | `2025-03-10 14:30:00` |
| `status` | `string` | Estado atual do atendimento | `Solucionado` |
| `categoria` | `string` | Classificação hierárquica do problema | `Hardware > Impressora` |
| `titulo` | `string` | Assunto resumido do chamado | `Solicitação de Toner` |
| `descricao` | `string` | Relato detalhado (Alvo principal da anonimização) | `A impressora do setor X apresenta falha...` |
| `localizacao` | `string` | Cidade ou Unidade solicitante normalizada | `Natal` |
| `setor_ti` | `string` | Equipe técnica responsável (ex: SAU, Redes) | `SAU` |
| `requerente` | `string` | Nome do usuário (Será anonimizado) | `Maria Silva` → `USER_a1b2` |


### 🔎 Visualização de Amostra

Exemplo simplificado de uma linha do dataset processado:

| id | data_abertura | status | categoria | localizacao | setor_ti | requerente (hash) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `15432` | `2025-03-10` | `Fechado` | `Hardware` | `Mossoró` | `SAU` | `USER_9f8e7d` |


---

## 📊 Dashboard Power BI

### Métricas Disponíveis

- **Produtividade por Setor**: Volume de atendimentos por equipe
- **Padrões Temporais**: Análise de sazonalidade e dias de maior demanda
- **Distribuição Geográfica**: Mapa de calor por cidades do RN
- **Status de Atendimento**: Funil de chamados (abertos, em andamento, fechados)

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
- Visualização geográfica de **167 municípios** do RN e **54 atendidos** pelo setor de tecnologia

## 🛠️ Stack Técnica

| Camada                  | Tecnologia                      |
| ----------------------- | ------------------------------- |
| **Processamento** | Python, Pandas, Regex           |
| **BI**            | Power BI, DAX, Power Query      |
| **Frontend**      | HTML5, Tailwind CSS, JavaScript |
| **Deploy**        | GitHub Pages                    |

## 📝 Licença

Este projeto está sob a licença MIT. Consulte [LICENSE](LICENSE) para mais informações.

## 👤 Autor

**Gustavo Palacio** - Analista de Dados

- 🌐 Website: [datapalacio.com.br](https://datapalacio.com.br)
- 📧 Contato: [palacio.dados@gmail.com](mailto:palacio.dados@gmail.com)
- 🐙 GitHub: [@dataPalacio](https://github.com/dataPalacio)
- 💼 LinkedIn: [gfpalacio](https://www.linkedin.com/in/gfpalacio/)

---

<div align="center">

**Desenvolvido com 💚 e dados**

[🌐 Visite meu Portfolio](https://datapalacio.com.br) • [📊 Ver Demo](https://datapalacio.github.io/ti-data-analysis/)

</div>
