import tkinter as tk
from tkinter import filedialog
import pandas as pd


# Dosya seçildiğinde çalışacak fonksiyon
def dosya_sec():
    dosya_yolu = filedialog.askopenfilename(filetypes=[("Excel Dosyaları", "*.xlsx")])
    if dosya_yolu:
        veri = pd.read_excel(dosya_yolu)

        # MG tarihi sütununu datetime formatına dönüştürün
        veri['MG tarihi'] = pd.to_datetime(veri['MG tarihi'], errors='coerce')

        # Eksik MG tarihlerini 121 gün öncesine ayarlayın
        veri['MG tarihi'].fillna(pd.to_datetime('today') - pd.DateOffset(days=121), inplace=True)

        # Tarih farklarını hesaplayarak kategorilere atayın
        suan = pd.to_datetime('today')
        veri['Tarih Farki'] = (suan - veri['MG tarihi']).dt.days
        veri['Kategori'] = pd.cut(veri['Tarih Farki'], bins=[-1, 30, 60, 90, 120, float('inf')],
                                  labels=['0-30', '31-60', '61-90', '91-120', '120+'])

        # Net ağırlık sütununu KG cinsinden ton birimine çevirin
        veri['Net ağırlık'] = veri['Net ağırlık'] / 1000

        # Kategorilere göre Net ağırlık toplamlarını hesaplayın
        toplam_net_agirlik = veri.groupby('Kategori', observed=False)['Net ağırlık'].sum().reset_index()

        # Sonuçları bir Excel dosyası olarak kaydet
        dosya_kaydet(toplam_net_agirlik)


# Hesapla butonuna tıklanınca çalışacak fonksiyon
def hesapla():
    # Burada hesaplama işlemleri yapabilirsiniz
    print("Hesaplama yapılıyor...")


# Excel dosyası olarak sonucu kaydetme fonksiyonu
def dosya_kaydet(veri):
    dosya_yolu = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Dosyası", "*.xlsx")])
    if dosya_yolu:
        with pd.ExcelWriter(dosya_yolu, engine='xlsxwriter') as writer:
            veri.to_excel(writer, sheet_name='Sonuc', index=False)
        print("Sonuç Excel dosyası olarak kaydedildi:", dosya_yolu)


# Ana pencere oluştur
pencere = tk.Tk()
pencere.title("Stok Yaşlandırma ve Hesaplama")

# Butonları ekle
dosya_sec_btn = tk.Button(pencere, text="Dosya Seç", command=dosya_sec)
hesapla_btn = tk.Button(pencere, text="Hesapla", command=hesapla)
kaydet_btn = tk.Button(pencere, text="Kaydet", command=dosya_kaydet)

# Butonları pencereye yerleştir
dosya_sec_btn.pack()
hesapla_btn.pack()
kaydet_btn.pack()

# Ana döngüyü başlat
pencere.mainloop()
