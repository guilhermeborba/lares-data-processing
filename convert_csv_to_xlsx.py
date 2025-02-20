import pandas as pd

def split_dataframe(df, chunk_size):
    chunks = []
    for i in range(0, df.shape[0], chunk_size):
        chunks.append(df.iloc[i:i + chunk_size])
    return chunks

def convert_csv_to_xlsx(csv_file, xlsx_file):
    try:
        df = pd.read_csv(csv_file)
        chunks = split_dataframe(df, 1000000)  # Dividir em partes menores

        with pd.ExcelWriter(xlsx_file) as writer:
            for i, chunk in enumerate(chunks):
                chunk.to_excel(writer, index=False, sheet_name=f'Sheet{i+1}')
        print(f"Arquivo XLSX salvo como {xlsx_file}")
    except Exception as e:
        print(f"Erro ao converter {csv_file}: {e}")

if __name__ == "__main__":
    csv_file = 'assets/estat_naio_10_fcp_ip1_matriz.csv'
    xlsx_file = 'assets/estat_naio_10_fcp_ip1_matriz.xlsx'
    convert_csv_to_xlsx(csv_file, xlsx_file)