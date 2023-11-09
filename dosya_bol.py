import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, simpledialog

# Dosya seçme işlevi
def dosya_sec():
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    dosya_yolu_var.set(filepath)

# Dosyayı bölme işlevi
def dosyayi_bol():
    # Kullanıcıdan girilen değerleri al
    dosya_yolu = dosya_yolu_var.get()
    satir_sayisi = int(satir_girisi.get())

    # Dosyayı oku
    data = pd.read_excel(dosya_yolu, engine='openpyxl')

    # Dosya sayısını belirle
    dosya_sayisi = len(data) // satir_sayisi + (1 if len(data) % satir_sayisi else 0)

    # Dosyaları oluşturma
    for i in range(dosya_sayisi):
        baslangic = i * satir_sayisi
        bitis = (i + 1) * satir_sayisi
        parca = data[baslangic:bitis]

        # Dosyayı kaydetme
        kayit_yolu = os.path.splitext(dosya_yolu)[0] + f'_{i+1}.xlsx'
        parca.to_excel(kayit_yolu, index=False, engine='openpyxl')

    bilgi_label.config(text=f"{dosya_sayisi} dosya başarıyla oluşturuldu.")

# GUI ayarları
root = tk.Tk()
root.title("Dosya Bölme Aracı")

# Değişkenler
dosya_yolu_var = tk.StringVar()

# Etiketler
dosya_label = tk.Label(root, text="Dosya Yolu:")
dosya_label.pack(padx=20, pady=5)

# Dosya seç butonu
dosya_sec_buton = tk.Button(root, text="Dosya Seç", command=dosya_sec)
dosya_sec_buton.pack(padx=20, pady=5)

# Dosya yolu gösterme
dosya_yolu_goster = tk.Entry(root, textvariable=dosya_yolu_var, width=50)
dosya_yolu_goster.pack(padx=20, pady=5)

# Satır sayısı girişi
satir_label = tk.Label(root, text="Satır Sayısı:")
satir_label.pack(padx=20, pady=5)

satir_girisi = tk.Entry(root, width=10)
satir_girisi.pack(padx=20, pady=5)

# Böl butonu
bol_buton = tk.Button(root, text="Dosyayı Böl", command=dosyayi_bol)
bol_buton.pack(padx=20, pady=20)

# Bilgi etiketi
bilgi_label = tk.Label(root, text="")
bilgi_label.pack(padx=20, pady=5)

root.mainloop()
