# Excel File Generation

To create the Excel version:
1. Install: pip install openpyxl pandas
2. Run: python -c "import pandas as pd; pd.read_csv('test_users.csv').to_excel('test_users.xlsx', sheet_name='TestUsers', index=False)"

Or open test_users.csv in Excel and save as .xlsx