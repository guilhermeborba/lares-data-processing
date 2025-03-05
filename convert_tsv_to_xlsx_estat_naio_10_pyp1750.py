import pandas as pd
import pycountry  # Biblioteca para conversão de códigos de país

# Caminhos dos arquivos
file_tsv = "assets/estat_naio_10_pyp1750.tsv"  # Novo TSV
file_xlsx = "assets/modelo.xlsx"
output_xlsx = "assets/modelo_atualizado_estat_naio_10_pyp1750.xlsx"

# Carregar o TSV com separador correto
df_tsv = pd.read_csv(file_tsv, sep="\t")

# Ajustar os nomes das colunas corretamente
# Renomear a primeira coluna para processar a separação
df_tsv = df_tsv.rename(columns={df_tsv.columns[0]: "freq,unit,ind_use,ind_ava,stk_flow,geo"})

# Separar a primeira coluna em múltiplas colunas
split_columns = df_tsv["freq,unit,ind_use,ind_ava,stk_flow,geo"].str.split(",", expand=True)
split_columns.columns = ["freq", "unit", "ind_use", "ind_ava", "stk_flow", "geo"]

# Remover a coluna original e adicionar as novas colunas separadas
df_tsv = df_tsv.drop(columns=["freq,unit,ind_use,ind_ava,stk_flow,geo"])
df_tsv = pd.concat([split_columns, df_tsv], axis=1)

# Substituir valores faltantes (" :") por 0.0
df_tsv.replace({":": 0.0}, inplace=True)

# Converter os anos para formato numérico
df_tsv = df_tsv.melt(id_vars=['freq', 'unit', 'ind_use', 'ind_ava', 'stk_flow', 'geo'], 
                      var_name='year', value_name='value')

df_tsv['year'] = df_tsv['year'].astype(int)

# Filtrar apenas valores em milhões de euros
df_tsv = df_tsv[df_tsv['unit'] == 'MIO_EUR']

# Filtrar apenas produção doméstica (excluir importações, caso necessário)
df_tsv = df_tsv[df_tsv['stk_flow'] == 'DOM']

# Carregar a matriz original do XLSX
xls = pd.ExcelFile(file_xlsx)
df_xlsx = pd.read_excel(xls, sheet_name='ADB CONSTANT MRIO 2022')

# Verificar códigos de país antes do mapeamento
print("Valores únicos originais de geo no TSV:", df_tsv['geo'].unique())

# Criar dicionário de conversão ISO 2 -> ISO 3
iso2_to_iso3 = {country.alpha_2: country.alpha_3 for country in pycountry.countries}
iso2_to_iso3.update({
    "UK": "GBR", "EL": "GRC", "WRL_REST": "RoW", "DOM": "DOM"
})

# Converter os códigos de país para três caracteres
df_tsv['geo'] = df_tsv['geo'].map(iso2_to_iso3)

# Carregar a aba de Legend e mapear países
df_legend = pd.read_excel(xls, sheet_name='Legend')
print("Códigos de país disponíveis na Legend:", df_legend['Code'].unique())

dict_country = dict(zip(df_legend['Code'].str.strip().str.upper(), df_legend['Country']))

# Ajustar possíveis diferenças entre ISO3 e códigos da aba Legend
iso3_to_legend = {
    "DNK": "DEN",  # Dinamarca
    "NLD": "NET",  # Holanda
    "ROU": "ROM",  # Romênia
}
df_tsv['geo'] = df_tsv['geo'].replace(iso3_to_legend)
df_tsv['geo'] = df_tsv['geo'].map(dict_country)

# Verificar mapeamento
print("Valores únicos em geo após mapeamento:", df_tsv['geo'].dropna().unique())

# Pivotar para formato matriz
df_pivot = df_tsv.pivot_table(index=['geo', 'ind_ava'], 
                              columns=['ind_use', 'year'], 
                              values='value', 
                              aggfunc='sum').fillna(0)

# Verificar se a tabela pivotada tem dados
print("Quantidade de linhas e colunas da matriz pivotada:", df_pivot.shape)
print(df_pivot.head())

# Resetar o índice para evitar MultiIndex
df_pivot.reset_index(inplace=True)

# Converter MultiIndex das colunas em strings
df_pivot.columns = ['_'.join(map(str, col)).strip() if isinstance(col, tuple) else col for col in df_pivot.columns]

# Exportar para novo arquivo XLSX
with pd.ExcelWriter(output_xlsx) as writer:
    df_pivot.to_excel(writer, sheet_name='ADB CONSTANT MRIO 2022', index=False)
    df_legend.to_excel(writer, sheet_name='Legend', index=False)

print(f"Arquivo atualizado salvo em: {output_xlsx}")
