# 🔍 Dashboard Scouts - Streamlit

Dashboard interativo em Python usando Streamlit para análise de dados em Excel.

## 📋 Funcionalidades

- 📊 **Visualização de Dados**: Tabelas interativas com seus dados do Excel
- 📈 **Gráficos Dinâmicos**: Barras, pizza, linha e histogramas
- 🔍 **Busca e Filtros**: Filtre e busque dados facilmente
- 📉 **Estatísticas**: Análises descritivas automáticas
- 📥 **Export**: Download de dados filtrados em CSV
- 🔄 **Múltiplas Abas**: Suporte para arquivos Excel com várias abas

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/raavier/scouts_streamlit.git
cd scouts_streamlit
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## 💻 Como Usar

### Método 1: Upload de arquivo via interface
1. Execute o dashboard:
```bash
streamlit run app.py
```

2. Acesse no navegador (geralmente abre automaticamente em `http://localhost:8501`)

3. Use a barra lateral para fazer upload do seu arquivo Excel

### Método 2: Usar a pasta data
1. Coloque seus arquivos Excel na pasta `data/`:
```bash
cp seu_arquivo.xlsx data/
```

2. Execute o dashboard:
```bash
streamlit run app.py
```

3. Selecione o arquivo na barra lateral

## 📁 Estrutura do Projeto

```
scouts_streamlit/
├── app.py              # Aplicação principal do dashboard
├── requirements.txt    # Dependências do projeto
├── data/              # Pasta para arquivos Excel
│   └── .gitkeep
├── .gitignore
├── LICENSE
└── README.md
```

## 🔧 Tecnologias Utilizadas

- **Streamlit**: Framework para criação de dashboards
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Gráficos interativos
- **OpenPyXL**: Leitura de arquivos Excel

## 📊 Tipos de Visualizações Disponíveis

- **Gráfico de Barras**: Ideal para comparações entre categorias
- **Gráfico de Pizza**: Visualização de proporções
- **Gráfico de Linha**: Tendências ao longo do tempo ou sequências
- **Histograma**: Distribuição de valores numéricos

## 🎯 Exemplos de Uso

1. **Análise de Vendas**: Carregue sua planilha de vendas e visualize por período, produto ou região
2. **Controle de Estoque**: Monitore níveis de estoque com gráficos e filtros
3. **Relatórios Gerenciais**: Crie dashboards executivos com KPIs
4. **Análise de Dados**: Explore qualquer conjunto de dados em Excel

## 🔒 Privacidade

- Os dados são processados localmente
- Nenhum dado é enviado para servidores externos
- Arquivos da pasta `data/` não são versionados no Git (por padrão)

## 📝 Licença

Este projeto está sob a licença especificada no arquivo LICENSE.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📧 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório.