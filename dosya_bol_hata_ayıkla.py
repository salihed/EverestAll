import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

# Dosya seçme işlevi
def dosya_sec():
    filepaths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])
    dosya_yolu_var.set(",".join(filepaths))

# Dosyayı bölme işlevi
def dosyayi_bol():
    dosya_yolu = dosya_yolu_var.get().split(",")[0]  # İlk dosya yolu
    satir_sayisi = int(satir_girisi.get())

    data = pd.read_excel(dosya_yolu, engine='openpyxl')
    dosya_sayisi = len(data) // satir_sayisi + (1 if len(data) % satir_sayisi else 0)

    for i in range(dosya_sayisi):
        baslangic = i * satir_sayisi
        bitis = (i + 1) * satir_sayisi
        parca = data[baslangic:bitis]
        kayit_yolu = os.path.splitext(dosya_yolu)[0] + f'_{i+1}.xlsx'
        parca.to_excel(kayit_yolu, index=False, engine='openpyxl')

    bilgi_label.config(text=f"{dosya_sayisi} dosya başarıyla oluşturuldu.")

def basarisiz_sonuclari_ayikla():
    hatali_datalar = []

    for dosya_yolu in dosya_yolu_var.get().split(","):
        data = pd.read_excel(dosya_yolu, engine='openpyxl')
        hatali_data = data[data['Sonuç'].str.startswith('BAŞARISIZ', na=False)]
        hatali_datalar.append(hatali_data)

    sonuc = pd.concat(hatali_datalar)
    kayit_yolu = os.path.join(os.path.dirname(dosya_yolu), f'Hata Alınan {os.path.basename(dosya_yolu)}')
    sonuc.to_excel(kayit_yolu, index=False, engine='openpyxl')

    bilgi_label.config(text=f"Hatalı sonuçlar {kayit_yolu} isimli dosyada kaydedildi.")

root = tk.Tk()
root.title("Dosya İşlemleri")

dosya_yolu_var = tk.StringVar()

dosya_label = tk.Label(root, text="Dosya Yolu:")
dosya_label.pack(padx=20, pady=5)

dosya_sec_buton = tk.Button(root, text="Dosya Seç", command=dosya_sec)
dosya_sec_buton.pack(padx=20, pady=5)

dosya_yolu_goster = tk.Entry(root, textvariable=dosya_yolu_var, width=50)
dosya_yolu_goster.pack(padx=20, pady=5)

satir_label = tk.Label(root, text="Satır Sayısı:")
satir_label.pack(padx=20, pady=5)

satir_girisi = tk.Entry(root, width=10)
satir_girisi.pack(padx=20, pady=5)

bol_buton = tk.Button(root, text="Dosyayı Böl", command=dosyayi_bol)
bol_buton.pack(padx=20, pady=20)

hata_ayikla_buton = tk.Button(root, text="Hata Ayıkla", command=basarisiz_sonuclari_ayikla)
hata_ayikla_buton.pack(padx=20, pady=20)

bilgi_label = tk.Label(root, text="")
bilgi_label.pack(padx=20, pady=5)

root.mainloop()
