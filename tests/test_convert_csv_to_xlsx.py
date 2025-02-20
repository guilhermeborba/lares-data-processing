import unittest
import pandas as pd
import sys
import os

# Adiciona o diretório principal ao sys.path para que possamos importar convert_csv_to_xlsx
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from convert_csv_to_xlsx import convert_csv_to_xlsx

class TestConvertCSVToXLSX(unittest.TestCase):
    def test_conversion_creates_visible_sheet(self):
        csv_file = 'assets/test_matriz.csv'
        xlsx_file = 'assets/test_matriz.xlsx'
        
        # Convert CSV to XLSX
        convert_csv_to_xlsx(csv_file, xlsx_file)
        
        # Load the XLSX file and check if at least one sheet is visible
        xls = pd.ExcelFile(xlsx_file)
        self.assertGreater(len(xls.sheet_names), 0, "No sheets found in XLSX file")

if __name__ == "__main__":
    unittest.main()