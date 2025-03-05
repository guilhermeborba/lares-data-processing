import pandas as pd
import pycountry  # Biblioteca para conversão de códigos de país

# Caminhos dos arquivos
file_tsv = "assets/estat_naio_10_pyp1750.tsv"
file_xlsx = "assets/modelo.xlsx"
output_xlsx = "assets/modelo_atualizado_estat_naio_10_pyp1750.xlsx"

# Carregar o TSV com separador correto
df_tsv = pd.read_csv(file_tsv, sep="\t")

# Ajustar os nomes das colunas (split na primeira linha)
df_tsv.columns = df_tsv.columns[0].split(',') + list(df_tsv.columns[1:])

# Converter os anos para formato numérico
df_tsv = df_tsv.melt(id_vars=['freq', 'ind_use', 'ind_ava', 'c_dest', 'unit', 'c_orig'], 
                      var_name='year', value_name='value')

df_tsv['year'] = df_tsv['year'].astype(int)

df_tsv = df_tsv[df_tsv['unit'] == 'MIO_EUR']

# Carregar a matriz original do XLSX
xls = pd.ExcelFile(file_xlsx)
df_xlsx = pd.read_excel(xls, sheet_name='ADB CONSTANT MRIO 2022')

# Verificar os códigos de país antes do mapeamento
print("Valores únicos originais de c_dest no TSV:", df_tsv['c_dest'].unique())
print("Valores únicos originais de c_orig no TSV:", df_tsv['c_orig'].unique())

# Criar um dicionário de conversão ISO 2 -> ISO 3
iso2_to_iso3 = {country.alpha_2: country.alpha_3 for country in pycountry.countries}

# Adicionar manualmente códigos que não estão na biblioteca pycountry
iso2_to_iso3.update({
    "UK": "GBR",  # Código do Reino Unido
    "EL": "GRC",  # Grécia
    "WRL_REST": "RoW",  # Resto do mundo
    "DOM": "DOM"  # República Dominicana (caso não esteja na lista)
})

# Converter os códigos de dois para três caracteres no TSV
df_tsv['c_dest'] = df_tsv['c_dest'].map(iso2_to_iso3)
df_tsv['c_orig'] = df_tsv['c_orig'].map(iso2_to_iso3)

# Verificar se a conversão foi bem-sucedida
print("Valores únicos convertidos de c_dest:", df_tsv['c_dest'].dropna().unique())
print("Valores únicos convertidos de c_orig:", df_tsv['c_orig'].dropna().unique())

# Carregar a aba de Legend e criar dicionário de mapeamento
df_legend = pd.read_excel(xls, sheet_name='Legend')

print("Códigos de país disponíveis na Legend:", df_legend['Code'].unique())

dict_country = dict(zip(df_legend['Code'].str.strip().str.upper(), df_legend['Country']))

df_tsv['c_dest'] = df_tsv['c_dest'].map(dict_country)
df_tsv['c_orig'] = df_tsv['c_orig'].map(dict_country)

# Verificar se há dados após a conversão
print("Valores únicos em c_dest após mapeamento:", df_tsv['c_dest'].dropna().unique())
print("Valores únicos em c_orig após mapeamento:", df_tsv['c_orig'].dropna().unique())

# Pivotar para formato matriz
df_pivot = df_tsv.pivot_table(index=['c_orig', 'ind_ava'], 
                              columns=['c_dest', 'ind_use'], 
                              values='value', 
                              aggfunc='sum').fillna(0)

# Verificar se a tabela pivotada tem dados
print("Quantidade de linhas e colunas da matriz pivotada:", df_pivot.shape)
print(df_pivot.head())  # Exibir algumas linhas da tabela pivotada                              

# Resetar o índice para evitar MultiIndex
df_pivot.reset_index(inplace=True)

# Converter MultiIndex das colunas em strings
df_pivot.columns = ['_'.join(map(str, col)).strip() if isinstance(col, tuple) else col for col in df_pivot.columns]

# Exportar para novo arquivo XLSX
with pd.ExcelWriter(output_xlsx) as writer:
    df_pivot.to_excel(writer, sheet_name='ADB CONSTANT MRIO 2022', index=False)
    df_legend.to_excel(writer, sheet_name='Legend', index=False)

print(f"Arquivo atualizado salvo em: {output_xlsx}")