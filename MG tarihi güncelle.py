import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

root = tk.Tk()
root.title("MG Tarihi Güncelleme Aracı")

girdi_dosya_var = tk.StringVar()
cikti_dosya_var = tk.StringVar()
kayit_klasoru_var = tk.StringVar()

def dosya_sec(var):
    dosya_yolu = filedialog.askopenfilename(filetypes=[("Excel dosyaları", "*.xlsx;*.xls")])
    var.set(dosya_yolu)

def klasor_sec():
    klasor_yolu = filedialog.askdirectory()
    kayit_klasoru_var.set(klasor_yolu)

def dosya_guncelle():
    try:
        girdi = pd.read_excel(girdi_dosya_var.get())
        cikti = pd.read_excel(cikti_dosya_var.get())

        # Girdi dosyasındaki 'Taşıma birimi' değerlerini al
        girdi_tasima_birimleri = girdi['Taşıma birimi'].tolist()

        # Girdi dosyasındaki MG tarihi bilgisiyle çıktı dosyasını güncelle
        for tb in girdi_tasima_birimleri:
            if tb in cikti['Taşıma birimi'].values:
                cikti.loc[cikti['Taşıma birimi'] == tb, 'MG tarihi'] = girdi.loc[girdi['Taşıma birimi'] == tb, 'MG tarihi'].values[0]

        # Sonuçları belirtilen sütunlarla güncellenmiş dosyaya kaydet
        sutunlar = ['Sahip','Depo tipi', 'Depo adresi', 'Taşıma birimi', 'Ürün', 'Ürün kısa tanımı', 'Parti', 'Miktar', 'Net ağırlık', 'Stok türü', 'MG tarihi', 'Tanıtıcı X', 'Tanıtıcı Adı X', 'Pak Müşteri Kodu', 'Pak Müşteri Tanımı']
        cikti = cikti[sutunlar]
        kayit_yolu = kayit_klasoru_var.get() + "/guncellenmis_dosya.xlsx"
        cikti.to_excel(kayit_yolu, index=False)

        messagebox.showinfo("Bilgi", "Dosya başarıyla güncellendi!")
    except Exception as e:
        messagebox.showerror("Hata", str(e))


tk.Label(root, text="Referans Dosya:").pack(pady=10)
tk.Entry(root, textvariable=girdi_dosya_var, width=50).pack(pady=5)
tk.Button(root, text="Dosya Seç", command=lambda: dosya_sec(girdi_dosya_var)).pack(pady=5)

tk.Label(root, text="Stok Dosyası:").pack(pady=10)
tk.Entry(root, textvariable=cikti_dosya_var, width=50).pack(pady=5)
tk.Button(root, text="Dosya Seç", command=lambda: dosya_sec(cikti_dosya_var)).pack(pady=5)

tk.Label(root, text="Kayıt Klasörü:").pack(pady=10)
tk.Entry(root, textvariable=kayit_klasoru_var, width=50).pack(pady=5)
tk.Button(root, text="Klasör Seç", command=klasor_sec).pack(pady=5)

tk.Button(root, text="Dosyaları Güncelle", command=dosya_guncelle, bg="green", fg="white").pack(pady=20)

root.mainloop()
