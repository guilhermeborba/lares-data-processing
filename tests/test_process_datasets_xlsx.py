import pandas as pd

def split_dataframe(df, chunk_size):
    chunks = []
    for i in range(0, df.shape[0], chunk_size):
        chunks.append(df.iloc[i:i + chunk_size])
    return chunks

# Lista de arquivos TSV dentro da pasta assets
datasets = [
    "assets/estat_naio_10_fcp_ip1.tsv"
]

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

        # Transformação: Convertendo para formato de matriz
        matriz = df.to_numpy()  # Melhor abordagem para matriz
        print(f"\nMatriz extraída de {dataset}:")
        print(matriz[:5])  # Exibir as primeiras 5 linhas da matriz

        # Dividir DataFrame em partes menores
        chunks = split_dataframe(df, 1000000)  # Dividir em partes menores

        # Salvar matriz como XLSX
        xlsx_file = dataset.replace(".tsv", "_matriz.xlsx")
        with pd.ExcelWriter(xlsx_file) as writer:
            for i, chunk in enumerate(chunks):
                chunk.to_excel(writer, index=False, sheet_name=f'Sheet{i+1}')
        print(f"Arquivo salvo como {xlsx_file}")

    except Exception as e:
        print(f"Erro ao processar {dataset}: {e}")