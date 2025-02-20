# LARES Data Processing 📊

This repository contains **Python scripts** designed to process large **TSV files** (544MB+) and convert them into **Excel (XLSX)** while optimizing memory usage. The project was developed for **LARES - Laboratory of Social Responsibility and Sustainability at the Institute of Economics, UFRJ**.

## 🚀 Features

- ✅ **Efficient processing** of large **TSV files** using **chunk-based reading** to reduce memory usage.
- ✅ **Automatic conversion** to **Excel (XLSX)**, ensuring large datasets are properly structured.
- ✅ **Splits large datasets** into multiple Excel sheets if they exceed Excel’s row limits.
- ✅ **Modular scripts** for easy reuse and maintenance.

## 🛠️ Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/lares-data-processing.git
cd lares-data-processing

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas openpyxl

python process_datasets_xlsx.py
assets/estat_naio_10_fcp_ip1_matriz.xlsx
assets/estat_naio_10_fcp_ip1_matriz.xlsx (Sheet1, Sheet2, ...)
CHUNK_SIZE = 100000  # Change this value if needed

