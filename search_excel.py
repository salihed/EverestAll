import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def dosya_arama(klasor_yolu, aranacak_kelime):
    dosyalar = [f for f in os.listdir(klasor_yolu) if f.endswith(('.xlsx', '.xls'))]
    bulunan_dosyalar = []

    for dosya in dosyalar:
        dosya_yolu = os.path.join(klasor_yolu, dosya)
        try:
            data = pd.read_excel(dosya_yolu, engine='openpyxl')
            if data.applymap(lambda x: aranacak_kelime in str(x)).sum().sum() > 0:
                bulunan_dosyalar.append(dosya)
        except:
            pass

    return bulunan_dosyalar

def klasor_sec():
    klasor = filedialog.askdirectory()
    klasor_yolu.set(klasor)

def ara_ve_goster():
    klasor = klasor_yolu.get()
    kelime = kelime_entry.get()

    sonuclar = dosya_arama(klasor, kelime)

    if sonuclar:
        sonuc_var.set("\n".join(sonuclar))
    else:
        sonuc_var.set("Belirttiğiniz kelime veya ifadeyi içeren bir dosya bulunamadı.")

# GUI oluşturma
root = tk.Tk()
root.title("Excel Dosya Arama")

klasor_yolu = tk.StringVar()
sonuc_var = tk.StringVar()

# Klasör seçme butonu
klasor_label = tk.Label(root, text="Klasör Yolu:")
klasor_label.pack(pady=20)
klasor_entry = tk.Entry(root, textvariable=klasor_yolu, width=50)
klasor_entry.pack(pady=10)
klasor_buton = tk.Button(root, text="Klasör Seç", command=klasor_sec)
klasor_buton.pack(pady=10)

# Aranacak kelime girişi
kelime_label = tk.Label(root, text="Aranacak Kelime:")
kelime_label.pack(pady=20)
kelime_entry = tk.Entry(root, width=50)
kelime_entry.pack(pady=10)

# Ara butonu
ara_buton = tk.Button(root, text="Ara", command=ara_ve_goster)
ara_buton.pack(pady=20)

# Sonuç alanı
sonuc_label = tk.Label(root, text="Sonuçlar:")
sonuc_label.pack(pady=20)
sonuc_text = tk.Label(root, textvariable=sonuc_var)
sonuc_text.pack(pady=10)

root.mainloop()
