import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(page_title="Overall de Jogadores", layout="wide")

# Função para normalizar os valores entre 0 e 100
def normalizar_indicador(valores, melhor_para='maior'):
    """
    Normaliza os valores de um indicador entre 0 e 100
    melhor_para: 'maior' ou 'menor'
    """
    if melhor_para.lower() == 'menor':
        # Inverte a escala quando menor é melhor
        max_val = valores.max()
        min_val = valores.min()
        if max_val == min_val:
            return pd.Series([50] * len(valores), index=valores.index)
        return 100 - ((valores - min_val) / (max_val - min_val) * 100)
    else:
        # Escala normal quando maior é melhor
        max_val = valores.max()
        min_val = valores.min()
        if max_val == min_val:
            return pd.Series([50] * len(valores), index=valores.index)
        return (valores - min_val) / (max_val - min_val) * 100


def calcular_overall(df_jogadores, df_pesos, posicao='CB'):
    """
    Calcula o overall dos jogadores com base nos pesos
    """
    # Filtrar apenas indicadores com peso para a posição
    df_pesos_posicao = df_pesos[df_pesos[posicao].notna()].copy()
    
    # Criar DataFrame para armazenar os resultados
    resultados = pd.DataFrame()
    resultados['Nome'] = df_jogadores['player_name']
    resultados['COD'] = df_jogadores['COD']
    
    # Dicionário para armazenar overalls por classificação
    overalls_por_classificacao = {}
    
    # Inicializar colunas para cada classificação
    classificacoes = df_pesos_posicao['CLASSIFICACAO RANKING'].unique()
    classificacoes = [c for c in classificacoes if c != 0 and c != '?' and c != 'GK']
    
    for classificacao in classificacoes:
        overalls_por_classificacao[classificacao] = []
    
    # Para cada jogador, calcular o overall
    overall_geral = []
    
    for idx, jogador in df_jogadores.iterrows():
        soma_ponderada_geral = 0
        soma_pesos_geral = 0
        
        # Dicionário para armazenar soma por classificação
        soma_por_class = {c: {'soma': 0, 'peso': 0} for c in classificacoes}
        
        # Para cada indicador com peso
        for _, peso_row in df_pesos_posicao.iterrows():
            indicador = peso_row['INDICADOR']
            peso = peso_row[posicao]
            classificacao = peso_row['CLASSIFICACAO RANKING']
            melhor_para = peso_row['Melhor para']
            
            # Verificar se o indicador existe na base de jogadores
            if indicador in df_jogadores.columns:
                # Normalizar o indicador para todos os jogadores
                valores_normalizados = normalizar_indicador(
                    df_jogadores[indicador], 
                    melhor_para=melhor_para
                )
                
                valor_normalizado = valores_normalizados[idx]
                valor_ponderado = valor_normalizado * peso
                
                # Acumular para overall geral
                soma_ponderada_geral += valor_ponderado
                soma_pesos_geral += peso
                
                # Acumular para overall por classificação
                if classificacao in classificacoes:
                    soma_por_class[classificacao]['soma'] += valor_ponderado
                    soma_por_class[classificacao]['peso'] += peso
        
        # Calcular overall geral
        if soma_pesos_geral > 0:
            overall_geral.append(round(soma_ponderada_geral / soma_pesos_geral, 1))
        else:
            overall_geral.append(0)
        
        # Calcular overall por classificação
        for classificacao in classificacoes:
            if soma_por_class[classificacao]['peso'] > 0:
                overall_class = soma_por_class[classificacao]['soma'] / soma_por_class[classificacao]['peso']
                overalls_por_classificacao[classificacao].append(round(overall_class, 1))
            else:
                overalls_por_classificacao[classificacao].append(0)
    
    # Adicionar overall geral
    resultados['Overall'] = overall_geral
    
    # Adicionar overalls por classificação
    for classificacao in classificacoes:
        resultados[classificacao] = overalls_por_classificacao[classificacao]
    
    return resultados


def aplicar_cores_overall(val):
    """Aplica cores baseadas no valor do overall"""
    if pd.isna(val):
        return ''
    if isinstance(val, str):
        return ''
    if val >= 75:
        return 'background-color: #90EE90'  # Verde claro
    elif val >= 60:
        return 'background-color: #FFFF99'  # Amarelo claro
    elif val >= 45:
        return 'background-color: #FFD699'  # Laranja claro
    else:
        return 'background-color: #FFB3B3'  # Vermelho claro


# Título da aplicação
st.title("⚽ Sistema de Overall de Jogadores")
st.markdown("---")

# Upload dos arquivos
col1, col2 = st.columns(2)

with col1:
    arquivo_jogadores = st.file_uploader(
        "Upload da base de jogadores (zagueiro.xlsx)", 
        type=['xlsx', 'xls'],
        key='jogadores'
    )

with col2:
    arquivo_pesos = st.file_uploader(
        "Upload da base de pesos (base_peso.xlsx)", 
        type=['xlsx', 'xls'],
        key='pesos'
    )

# Se ambos arquivos foram carregados
if arquivo_jogadores is not None and arquivo_pesos is not None:
    # Carregar os dados
    df_jogadores = pd.read_excel(arquivo_jogadores)
    df_pesos = pd.read_excel(arquivo_pesos)
    
    st.success("✅ Arquivos carregados com sucesso!")
    
    # Informações sobre os dados
    with st.expander("ℹ️ Informações sobre os dados"):
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Jogadores", len(df_jogadores))
            st.metric("Total de Indicadores", len(df_jogadores.columns))
        with col2:
            st.metric("Indicadores com Peso", len(df_pesos[df_pesos['CB'].notna()]))
            classificacoes = df_pesos['CLASSIFICACAO RANKING'].unique()
            classificacoes = [c for c in classificacoes if c != 0 and c != '?' and c != 'GK']
            st.metric("Classificações", len(classificacoes))
    
    st.markdown("---")
    
    # Calcular os overalls
    with st.spinner("Calculando overalls..."):
        df_resultados = calcular_overall(df_jogadores, df_pesos, posicao='CB')
    
    st.success("✅ Cálculos concluídos!")
    
    # Ordenar por overall geral
    df_resultados_sorted = df_resultados.sort_values('Overall', ascending=False).reset_index(drop=True)
    
    # Criar abas para diferentes visualizações
    tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "📈 Por Classificação", "📋 Dados Completos"])
    
    with tab1:
        st.subheader("Overall Geral dos Jogadores")
        
        # Tabela principal com overall geral
        df_display_geral = df_resultados_sorted[['Nome', 'Overall']].copy()
        df_display_geral.index = df_display_geral.index + 1
        
        st.dataframe(
            df_display_geral.style.applymap(
                aplicar_cores_overall, 
                subset=['Overall']
            ).format({'Overall': '{:.1f}'}),
            use_container_width=True,
            height=600
        )
        
        # Estatísticas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Média Overall", f"{df_resultados['Overall'].mean():.1f}")
        with col2:
            st.metric("Maior Overall", f"{df_resultados['Overall'].max():.1f}")
        with col3:
            st.metric("Menor Overall", f"{df_resultados['Overall'].min():.1f}")
        with col4:
            st.metric("Desvio Padrão", f"{df_resultados['Overall'].std():.1f}")
    
    with tab2:
        st.subheader("Overall por Classificação")
        
        # Pegar as classificações disponíveis (exceto COD, Nome e Overall)
        classificacoes = [col for col in df_resultados_sorted.columns 
                         if col not in ['COD', 'Nome', 'Overall']]
        
        # Criar grid com as tabelas
        n_classificacoes = len(classificacoes)
        n_cols = min(2, n_classificacoes)
        
        for i in range(0, n_classificacoes, n_cols):
            cols = st.columns(n_cols)
            for j in range(n_cols):
                if i + j < n_classificacoes:
                    classificacao = classificacoes[i + j]
                    with cols[j]:
                        st.markdown(f"**{classificacao}**")
                        
                        # Ordenar por essa classificação
                        df_class = df_resultados_sorted[['Nome', classificacao]].copy()
                        df_class = df_class.sort_values(classificacao, ascending=False)
                        df_class.index = range(1, len(df_class) + 1)
                        
                        st.dataframe(
                            df_class.style.applymap(
                                aplicar_cores_overall,
                                subset=[classificacao]
                            ).format({classificacao: '{:.1f}'}),
                            use_container_width=True,
                            height=400
                        )
    
    with tab3:
        st.subheader("Tabela Completa com Todos os Overalls")
        
        # Mostrar tabela completa
        df_completo = df_resultados_sorted.copy()
        df_completo.index = df_completo.index + 1
        
        # Colunas numéricas para formatar
        colunas_numericas = [col for col in df_completo.columns 
                            if col not in ['COD', 'Nome']]
        
        st.dataframe(
            df_completo.style.applymap(
                aplicar_cores_overall,
                subset=colunas_numericas
            ).format({col: '{:.1f}' for col in colunas_numericas}),
            use_container_width=True,
            height=600
        )
        
        # Botão para download
        st.download_button(
            label="📥 Download CSV",
            data=df_completo.to_csv(index=False).encode('utf-8'),
            file_name='overall_jogadores.csv',
            mime='text/csv'
        )

else:
    st.info("👆 Por favor, faça upload dos dois arquivos para começar a análise.")
    
    # Instruções
    with st.expander("📖 Como usar"):
        st.markdown("""
        ### Instruções:
        
        1. **Upload dos Arquivos:**
           - Faça upload do arquivo de jogadores (zagueiro.xlsx)
           - Faça upload do arquivo de pesos (base_peso.xlsx)
        
        2. **Cálculo do Overall:**
           - O sistema normaliza cada indicador entre 0 e 100
           - Aplica os pesos específicos para a posição (CB)
           - Calcula o overall geral e por classificação
        
        3. **Visualizações:**
           - **Visão Geral:** Ranking geral dos jogadores
           - **Por Classificação:** Rankings separados por tipo (DGP, PASS, OFFENSIVE, DEFENSIVE)
           - **Dados Completos:** Tabela completa com todos os overalls
        
        4. **Cores:**
           - 🟢 Verde: Overall ≥ 75 (Excelente)
           - 🟡 Amarelo: Overall 60-74 (Bom)
           - 🟠 Laranja: Overall 45-59 (Regular)
           - 🔴 Vermelho: Overall < 45 (Fraco)
        """)

# Footer
st.markdown("---")
st.markdown("Sistema de Overall de Jogadores v1.0")
