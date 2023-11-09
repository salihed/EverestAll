import os
import getpass
import pandas as pd

# Kullanıcının adını al
user_name = getpass.getuser()

# Kullanıcının masaüstü dizinini bul
desktop_path = os.path.join('C:\\Users', user_name, 'Desktop')

# Excel dosyasının tam yolunu oluştur
excel_file = os.path.join(desktop_path, 'ZSD2000 Acik Siparisler-Teslimat Planlari-ZNSB.xlsx')

# Excel dosyasını oku, 'engine' parametresi ile formatı belirt
df = pd.read_excel(excel_file, engine='openpyxl')

# Sevki Beklenen Miktar hesaplama işlemi
df['Sevki Beklenen Miktar'] = df['Sipariş miktarı'] - df['Mal Çıkış']

# Toplam Müşteri Stoğu sütununu tekil hale getirme
#unique_customer_stock = df.groupby(['Müşteri', 'Ad 1', 'Malzeme'])['Toplam Müşteri Stoğu'].sum().reset_index()

# Her bir grup için toplam satır sayısını ve Toplam Müşteri Stoğu'nu hesapla
grouped = df.groupby(['Müşteri', 'Ad 1', 'Malzeme'])
df['Satır Sayısı'] = grouped['Toplam Müşteri Stoğu'].transform('count')
df['Toplam Müşteri Stoğu'] = df['Toplam Müşteri Stoğu'] / df['Satır Sayısı']

# Toplam Müşteri Stoğu sütununu tekil hale getirme
unique_customer_stock = df.groupby(['Müşteri', 'Ad 1', 'Malzeme'])['Toplam Müşteri Stoğu'].sum().reset_index()

# Toplam Stok sütununu tekil hale getirme
unique_total_stock = df.groupby(['Termin Tarihi', 'Sipariş miktarı', 'Mal Çıkış', 'Malzeme'])['Toplam Stok'].sum().reset_index()

# Sonuçları görüntüle
#print("Toplam Müşteri Stoğu:")
#print(unique_customer_stock)

#print("\nToplam Stok:")
#print(unique_total_stock)

# Sonuçları Excel dosyasına yaz
output_excel_file = os.path.join(desktop_path, 'SonucX.xlsx')
unique_customer_stock.to_excel(output_excel_file, index=False)
print(f"Sonuçlar Excel dosyasına yazıldı: {output_excel_file}")