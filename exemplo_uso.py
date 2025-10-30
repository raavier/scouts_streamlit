"""
Script de exemplo para calcular overall dos jogadores sem usar Streamlit
"""

import pandas as pd
import numpy as np

def normalizar_indicador(valores, melhor_para='maior'):
    """
    Normaliza os valores de um indicador entre 0 e 100
    melhor_para: 'maior' ou 'menor'
    """
    if melhor_para.lower() == 'menor':
        max_val = valores.max()
        min_val = valores.min()
        if max_val == min_val:
            return pd.Series([50] * len(valores), index=valores.index)
        return 100 - ((valores - min_val) / (max_val - min_val) * 100)
    else:
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


# ========== EXEMPLO DE USO ==========

if __name__ == "__main__":
    # Carregar as bases de dados
    print("Carregando bases de dados...")
    df_jogadores = pd.read_excel('zagueiro.xlsx')
    df_pesos = pd.read_excel('base_peso.xlsx')
    
    print(f"✅ {len(df_jogadores)} jogadores carregados")
    print(f"✅ {len(df_pesos)} indicadores carregados")
    
    # Calcular os overalls
    print("\nCalculando overalls...")
    df_resultados = calcular_overall(df_jogadores, df_pesos, posicao='CB')
    
    # Ordenar por overall geral
    df_resultados = df_resultados.sort_values('Overall', ascending=False).reset_index(drop=True)
    
    print("\n" + "="*80)
    print("TOP 10 JOGADORES - OVERALL GERAL")
    print("="*80)
    print(df_resultados[['Nome', 'Overall']].head(10).to_string(index=True))
    
    # Mostrar top 5 por cada classificação
    classificacoes = [col for col in df_resultados.columns 
                     if col not in ['COD', 'Nome', 'Overall']]
    
    for classificacao in classificacoes:
        print(f"\n{'='*80}")
        print(f"TOP 5 JOGADORES - {classificacao}")
        print("="*80)
        df_class = df_resultados[['Nome', classificacao]].sort_values(
            classificacao, ascending=False
        )
        print(df_class.head(5).to_string(index=False))
    
    # Salvar resultados em CSV
    print("\n\nSalvando resultados em CSV...")
    df_resultados.to_csv('overall_jogadores.csv', index=False)
    print("✅ Arquivo 'overall_jogadores.csv' criado com sucesso!")
    
    # Estatísticas gerais
    print("\n" + "="*80)
    print("ESTATÍSTICAS GERAIS")
    print("="*80)
    print(f"Média Overall: {df_resultados['Overall'].mean():.1f}")
    print(f"Mediana Overall: {df_resultados['Overall'].median():.1f}")
    print(f"Desvio Padrão: {df_resultados['Overall'].std():.1f}")
    print(f"Maior Overall: {df_resultados['Overall'].max():.1f} ({df_resultados.loc[df_resultados['Overall'].idxmax(), 'Nome']})")
    print(f"Menor Overall: {df_resultados['Overall'].min():.1f} ({df_resultados.loc[df_resultados['Overall'].idxmin(), 'Nome']})")
    
    print("\n✅ Processamento concluído!")
