import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Configuração da página
st.set_page_config(
    page_title="Dashboard Scouts",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🔍 Dashboard Scouts")
st.markdown("---")

# Sidebar para upload e seleção de arquivos
st.sidebar.header("📂 Carregar Dados")

# Opção 1: Upload de arquivo
uploaded_file = st.sidebar.file_uploader(
    "Fazer upload de arquivo Excel",
    type=['xlsx', 'xls'],
    help="Selecione um arquivo Excel para visualizar"
)

# Opção 2: Selecionar da pasta data
data_folder = Path("data")
if data_folder.exists():
    excel_files = list(data_folder.glob("*.xlsx")) + list(data_folder.glob("*.xls"))
    if excel_files:
        file_names = ["Selecione..."] + [f.name for f in excel_files]
        selected_file = st.sidebar.selectbox(
            "Ou selecione da pasta 'data'",
            file_names
        )
    else:
        selected_file = None
        st.sidebar.info("Nenhum arquivo Excel encontrado na pasta 'data'")
else:
    selected_file = None

# Função para carregar dados
@st.cache_data
def load_data(file_path):
    """Carrega dados do Excel"""
    try:
        # Tentar ler todas as abas
        excel_file = pd.ExcelFile(file_path)
        return excel_file, excel_file.sheet_names
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return None, None

# Determinar qual arquivo usar
df = None
sheet_names = []

if uploaded_file is not None:
    excel_file, sheet_names = load_data(uploaded_file)
    source = "upload"
elif selected_file and selected_file != "Selecione...":
    file_path = data_folder / selected_file
    excel_file, sheet_names = load_data(file_path)
    source = "local"
else:
    excel_file = None

# Se há arquivo carregado
if excel_file is not None:
    # Selecionar aba
    if len(sheet_names) > 1:
        selected_sheet = st.sidebar.selectbox(
            "Selecione a aba",
            sheet_names
        )
    else:
        selected_sheet = sheet_names[0]

    # Carregar dados da aba selecionada
    df = pd.read_excel(excel_file, sheet_name=selected_sheet)

    st.sidebar.success(f"✅ Arquivo carregado com sucesso!")
    st.sidebar.info(f"📊 {len(df)} linhas × {len(df.columns)} colunas")

    # Opções de filtro
    st.sidebar.markdown("---")
    st.sidebar.header("🔧 Filtros")

    # Filtros dinâmicos para colunas categóricas
    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

    filters = {}
    if categorical_columns:
        for col in categorical_columns[:5]:  # Limitar a 5 colunas para não poluir
            unique_values = df[col].dropna().unique()
            if len(unique_values) <= 20:  # Só mostrar se tiver até 20 valores únicos
                selected_values = st.sidebar.multiselect(
                    f"Filtrar por {col}",
                    options=sorted(unique_values.astype(str)),
                    default=None
                )
                if selected_values:
                    filters[col] = selected_values

    # Aplicar filtros
    filtered_df = df.copy()
    for col, values in filters.items():
        filtered_df = filtered_df[filtered_df[col].astype(str).isin(values)]

    # Conteúdo principal
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "📈 Gráficos", "🔍 Explorar Dados", "📉 Estatísticas"])

    with tab1:
        st.header("📊 Visão Geral dos Dados")

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Registros", len(filtered_df))
        with col2:
            st.metric("Colunas", len(filtered_df.columns))
        with col3:
            st.metric("Valores Nulos", filtered_df.isnull().sum().sum())
        with col4:
            numeric_cols = filtered_df.select_dtypes(include=['number']).columns
            st.metric("Colunas Numéricas", len(numeric_cols))

        st.markdown("---")

        # Preview dos dados
        st.subheader("👀 Preview dos Dados")
        st.dataframe(filtered_df.head(100), use_container_width=True)

        # Download dos dados filtrados
        st.download_button(
            label="📥 Download dados filtrados (CSV)",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='dados_filtrados.csv',
            mime='text/csv',
        )

    with tab2:
        st.header("📈 Visualizações")

        # Selecionar colunas para gráficos
        numeric_columns = filtered_df.select_dtypes(include=['number']).columns.tolist()

        if numeric_columns:
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Gráfico de Barras")
                if categorical_columns:
                    x_col = st.selectbox("Eixo X (Categoria)", categorical_columns, key="bar_x")
                    if numeric_columns:
                        y_col = st.selectbox("Eixo Y (Valor)", numeric_columns, key="bar_y")

                        # Agregar dados
                        agg_data = filtered_df.groupby(x_col)[y_col].sum().reset_index()
                        fig = px.bar(agg_data, x=x_col, y=y_col,
                                    title=f"{y_col} por {x_col}")
                        st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Gráfico de Pizza")
                if categorical_columns:
                    pie_col = st.selectbox("Selecione a coluna", categorical_columns, key="pie_col")
                    value_counts = filtered_df[pie_col].value_counts().head(10)
                    fig = px.pie(values=value_counts.values, names=value_counts.index,
                                title=f"Distribuição de {pie_col}")
                    st.plotly_chart(fig, use_container_width=True)

            # Gráfico de linha
            st.subheader("Gráfico de Linha")
            if len(numeric_columns) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    line_x = st.selectbox("Eixo X", filtered_df.columns.tolist(), key="line_x")
                with col2:
                    line_y = st.selectbox("Eixo Y", numeric_columns, key="line_y")

                fig = px.line(filtered_df.sort_values(line_x), x=line_x, y=line_y,
                            title=f"{line_y} por {line_x}")
                st.plotly_chart(fig, use_container_width=True)

            # Histograma
            st.subheader("Histograma")
            hist_col = st.selectbox("Selecione a coluna numérica", numeric_columns, key="hist")
            fig = px.histogram(filtered_df, x=hist_col,
                             title=f"Distribuição de {hist_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhuma coluna numérica encontrada para criar gráficos.")

    with tab3:
        st.header("🔍 Explorar Dados")

        # Busca
        st.subheader("Buscar nos dados")
        search_term = st.text_input("Digite o termo de busca")

        if search_term:
            mask = filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)
            ).any(axis=1)
            search_results = filtered_df[mask]
            st.write(f"Encontrados {len(search_results)} resultados")
            st.dataframe(search_results, use_container_width=True)

        # Visualizar colunas específicas
        st.subheader("Selecionar colunas para visualizar")
        selected_columns = st.multiselect(
            "Escolha as colunas",
            filtered_df.columns.tolist(),
            default=filtered_df.columns.tolist()[:5]
        )

        if selected_columns:
            st.dataframe(filtered_df[selected_columns], use_container_width=True)

    with tab4:
        st.header("📉 Estatísticas Descritivas")

        # Estatísticas gerais
        st.subheader("Estatísticas das Colunas Numéricas")
        if numeric_columns:
            st.dataframe(filtered_df[numeric_columns].describe(), use_container_width=True)
        else:
            st.warning("Nenhuma coluna numérica encontrada.")

        # Informações sobre valores nulos
        st.subheader("Valores Nulos por Coluna")
        null_counts = filtered_df.isnull().sum()
        null_df = pd.DataFrame({
            'Coluna': null_counts.index,
            'Valores Nulos': null_counts.values,
            'Percentual': (null_counts.values / len(filtered_df) * 100).round(2)
        })
        null_df = null_df[null_df['Valores Nulos'] > 0].sort_values('Valores Nulos', ascending=False)

        if len(null_df) > 0:
            st.dataframe(null_df, use_container_width=True)

            # Gráfico de valores nulos
            fig = px.bar(null_df, x='Coluna', y='Valores Nulos',
                        title="Valores Nulos por Coluna")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ Nenhum valor nulo encontrado!")

        # Informações de tipos de dados
        st.subheader("Tipos de Dados")
        type_df = pd.DataFrame({
            'Coluna': filtered_df.columns,
            'Tipo': filtered_df.dtypes.values
        })
        st.dataframe(type_df, use_container_width=True)

else:
    # Página inicial quando não há arquivo carregado
    st.info("👈 Por favor, carregue um arquivo Excel usando a barra lateral")

    st.markdown("""
    ## 📋 Como usar este dashboard:

    1. **Upload de arquivo**: Use a barra lateral para fazer upload de um arquivo Excel
    2. **Ou**: Coloque seus arquivos Excel na pasta `data/` e selecione na barra lateral
    3. **Explore**: Use as diferentes abas para visualizar e analisar seus dados

    ### 🎯 Funcionalidades disponíveis:

    - 📊 Visualização de dados em tabelas interativas
    - 📈 Gráficos dinâmicos (barras, pizza, linha, histograma)
    - 🔍 Busca e filtros nos dados
    - 📉 Estatísticas descritivas
    - 📥 Download de dados filtrados

    ### 💡 Dicas:

    - Suporta arquivos `.xlsx` e `.xls`
    - Funciona com múltiplas abas
    - Filtros dinâmicos baseados nos seus dados
    - Interface responsiva e fácil de usar
    """)

# Rodapé
st.markdown("---")
st.markdown("Dashboard criado com Streamlit 🎈")
