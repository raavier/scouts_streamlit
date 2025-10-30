# Sistema de Overall de Jogadores ⚽

Sistema desenvolvido em Python/Streamlit para calcular o overall de jogadores de futebol com base em indicadores ponderados por posição.

## 📋 Funcionalidades

- ✅ Cálculo de Overall Geral (média ponderada de todos os indicadores)
- ✅ Cálculo de Overall por Classificação (DGP, PASS, OFFENSIVE, DEFENSIVE)
- ✅ Normalização automática dos indicadores (0-100)
- ✅ Interface visual intuitiva com cores por performance
- ✅ Rankings ordenados por cada tipo de classificação
- ✅ Export para CSV

## 🚀 Como Executar

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o aplicativo

```bash
streamlit run app_overall_jogadores.py
```

### 3. Usar o sistema

1. Faça upload do arquivo `zagueiro.xlsx` (base de jogadores)
2. Faça upload do arquivo `base_peso.xlsx` (base de pesos)
3. O sistema calculará automaticamente os overalls
4. Navegue pelas abas para ver diferentes visualizações

## 📊 Como Funciona

### Cálculo do Overall

1. **Normalização**: Cada indicador é normalizado entre 0 e 100
   - Para indicadores onde "maior é melhor": valor normalizado = (valor - min) / (max - min) * 100
   - Para indicadores onde "menor é melhor": a escala é invertida

2. **Ponderação**: Cada indicador normalizado é multiplicado pelo seu peso específico para a posição

3. **Overall Geral**: Média ponderada de todos os indicadores
   ```
   Overall = Σ(indicador_normalizado * peso) / Σ(pesos)
   ```

4. **Overall por Classificação**: Mesma fórmula, mas considerando apenas indicadores de cada classificação específica

### Classificações Disponíveis

- **GERAL**: Overall geral do jogador
- **DGP**: Desempenho em jogo posicional
- **PASS**: Qualidade de passe
- **OFFENSIVE**: Ações ofensivas
- **DEFENSIVE**: Ações defensivas

### Escala de Cores

- 🟢 **Verde** (75-100): Excelente
- 🟡 **Amarelo** (60-74): Bom
- 🟠 **Laranja** (45-59): Regular
- 🔴 **Vermelho** (0-44): Fraco

## 📁 Estrutura dos Arquivos

### zagueiro.xlsx
Contém os dados dos jogadores com todos os indicadores:
- COD (código do jogador)
- player_name (nome do jogador)
- POSICAO AJUSTADA (posição)
- +220 indicadores de performance

### base_peso.xlsx
Contém os pesos para cada indicador por posição:
- INDICADOR (nome do indicador)
- CLASSIFICACAO RANKING (tipo de classificação)
- SUBCLASSIFICACAO RANKING
- Melhor para (maior/menor)
- CB, RB, LB, DM, CM, AM, W, CF (pesos por posição)

## 🔧 Personalização

Para adicionar novas posições, basta modificar a função `calcular_overall()` alterando o parâmetro `posicao`:

```python
df_resultados = calcular_overall(df_jogadores, df_pesos, posicao='RB')  # Para laterais direitos
```

## 📈 Expansão Futura

O sistema está preparado para:
- ✅ Adicionar outras posições (RB, LB, DM, CM, AM, W, CF)
- ✅ Comparar jogadores de diferentes posições
- ✅ Criar rankings multi-posição
- ✅ Adicionar filtros por time, liga, idade, etc.

## 💡 Dicas de Uso

1. **Ordene por diferentes colunas**: Clique nos cabeçalhos das colunas para ordenar
2. **Use a busca**: Procure jogadores específicos usando Ctrl+F
3. **Export**: Baixe os dados em CSV para análises externas
4. **Compare**: Use a aba "Por Classificação" para ver especialidades de cada jogador

## 🐛 Troubleshooting

**Erro ao carregar arquivos**: Certifique-se de que os arquivos estão no formato .xlsx

**Valores zerados**: Verifique se os nomes dos indicadores na base de jogadores correspondem aos da base de pesos

**Erro de normalização**: Garanta que os indicadores têm valores numéricos válidos

## 📝 Licença

Desenvolvido para análise de performance de jogadores de futebol.
