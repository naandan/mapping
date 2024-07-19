import pandas as pd

# Misalkan 'locations' adalah data Anda dan 'column_names' adalah nama kolomnya
locations = [
    {'city': 'Jakarta', 'country': 'Indonesia'},
    {'city': 'Bandung', 'country': 'Indonesia'},
    # Data lainnya
]

column_names = ['city', 'country']
locations_df = pd.DataFrame(locations, columns=column_names)

def save(row):
    index = row.name
    # Lakukan sesuatu dengan 'index' dan 'row'
    print(f"Index: {index+1}, Data: {row['city']}")
    # Implementasi penyimpanan data


# Gunakan apply dengan axis=1 untuk meneruskan setiap baris ke fungsi 'save'
locations_df.apply(save, axis=1)
