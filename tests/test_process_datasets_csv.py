import unittest
import pandas as pd

class TestProcessDatasets(unittest.TestCase):
    def test_expected_matrices(self):
        df = pd.read_csv('assets/estat_naio_10_fcp_ip1_matriz.csv')
        expected_columns = ['freq', 'prd_use', 'prd_ava', 'c_dest', 'unit', 'c_orig', 'TIME_PERIOD']  # Substitua com as colunas reais esperadas
        for col in expected_columns:
            self.assertIn(col, df.columns, f"Expected column {col} not found in CSV")

if __name__ == "__main__":
    unittest.main()