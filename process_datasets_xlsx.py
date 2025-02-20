import pandas as pd

# Lista de arquivos TSV dentro da pasta assets
datasets = [
    "assets/estat_naio_10_fcp_ip1.tsv"
]

# Definir tamanho máximo de linhas por aba no Excel (Excel suporta no máximo 1.048.576 linhas)
MAX_ROWS_PER_SHEET = 500000  # Dividimos o arquivo em abas menores

for dataset in datasets:
    try:
        print(f"Lendo {dataset}...")
        df = pd.read_csv(dataset, delimiter="\t")  # Definir \t como delimitador

        # Corrigir possíveis espaços extras nas colunas
        df.columns = df.columns.str.strip()

        # Exibir informações básicas
        print(f"Colunas do dataset {dataset}:")
        print(df.columns)

        print(f"\nPrimeiras 5 linhas de {dataset}:")
        print(df.head())

        # Criar nome do arquivo XLSX
        xlsx_file = dataset.replace(".tsv", "_matriz.xlsx")

        # Criar o arquivo XLSX dividindo os dados em múltiplas abas
        with pd.ExcelWriter(xlsx_file, engine="openpyxl") as writer:
            for i in range(0, len(df), MAX_ROWS_PER_SHEET):
                df.iloc[i:i+MAX_ROWS_PER_SHEET].to_excel(writer, sheet_name=f"Parte_{i//MAX_ROWS_PER_SHEET + 1}", index=False)

        print(f"✅ Arquivo salvo como {xlsx_file}")

    except Exception as e:
        print(f"Erro ao processar {dataset}: {e}")
