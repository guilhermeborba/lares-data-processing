import pandas as pd

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

        # Salvar matriz como CSV
        csv_file = dataset.replace(".tsv", "_matriz.csv")
        df.to_csv(csv_file, index=False)
        print(f"Arquivo salvo como {csv_file}")

        # Verifica se o DataFrame não está vazio antes de salvar como XLSX
        if not df.empty:
            print(f"⚠️ Aviso: O arquivo XLSX não será gerado no processo atual. A conversão será feita no script separado.")

    except Exception as e:
        print(f"Erro ao processar {dataset}: {e}")