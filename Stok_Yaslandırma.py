import pandas as pd
from tkinter import *
from tkinter import filedialog, messagebox

grup_net_agirlik = None  # Global olarak grup_net_agirlik değişkenini tanımlıyoruz
toplam_net_agirlik = None  # Global olarak grup_net_agirlik değişkenini tanımlıyoruz

def dosya_sec():
    file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx;*.xls')])
    dosya_yolu_var.set(file_path)

def custom_format(value):
    """Özel binlik ayracı formatlama fonksiyonu"""
    return "{:,.0f}".format(value).replace(',', 'X').replace('.', ',').replace('X', '.')

def sonuclari_excel_aktar():
    try:
        dosya_yolu = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if dosya_yolu:
            # Excel dosyasını oluştur
            writer = pd.ExcelWriter(dosya_yolu, engine='xlsxwriter')

            # Sonuçları Excel dosyasına yaz
            formatted_values = (grup_net_agirlik / 1000).apply(custom_format).sort_index()
            sonuc = f"Stokta Bekleme Günü\n{formatted_values.to_string()}\n\nNet ağırlık (ton) Toplamı: {toplam_net_agirlik}"
            sonuc_df = pd.DataFrame([sonuc], columns=["Sonuç"])
            sonuc_df.to_excel(writer, sheet_name='Sonuçlar', index=False)

            # Excel dosyasını kaydet
            writer.save()

            messagebox.showinfo("Bilgi", f"Sonuçlar Excel'e aktarıldı:\n{dosya_yolu}")
    except Exception as e:
        messagebox.showerror("Hata", str(e))


def stok_yaslandirma():
    try:
        data = pd.read_excel(dosya_yolu_var.get())
        data['MG tarihi'] = pd.to_datetime(data['MG tarihi'], errors='coerce')
        bugun = pd.Timestamp.now()
        data['Gun'] = (bugun - data['MG tarihi']).dt.days

        # NaN veya geçersiz tarih formatı olan değerleri 'Diğer' kategorisine atama
        data.loc[data['MG tarihi'].isnull(), 'Yaslandirma'] = 'Diğer'

        # Geçerli 'Gun' değerleri için yaşlandırma kategorisi oluşturma
        kategoriler = ["0-30 gün", "31-60 gün", "61-90 gün", "91-120 gün", "120+ gün"]
        bins = [-float('inf'), 30, 60, 90, 120, float('inf')]

        mask = data['Yaslandirma'].isnull()  # Yaslandirma değeri atanmamış satırlar
        data.loc[mask, 'Yaslandirma'] = pd.cut(data.loc[mask, 'Gun'], bins=bins, labels=kategoriler, right=False)

        # Yaslandirma kategorisine göre grupla ve Net ağırlık sütununu topla
        grup_net_agirlik = data.groupby('Yaslandirma')['Net ağırlık'].sum()

        # Net ağırlığı ton cinsine dönüştür ve formatla
        formatted_values = (grup_net_agirlik / 1000).apply(custom_format).sort_index()
        toplam_net_agirlik = custom_format(grup_net_agirlik.sum() / 1000)
        sonuc = f"Stokta Bekleme Günü\n{formatted_values.to_string()}\n\nNet ağırlık (ton) Toplamı: {toplam_net_agirlik}"

        sonuc_var.set(sonuc)

    except Exception as e:
        messagebox.showerror("Hata", str(e))


app = Tk()
app.title("Stok Yaşlandırma Uygulaması")
app.minsize(480, 320)

dosya_yolu_var = StringVar()
sonuc_var = StringVar()

Label(app, text="Dosya Seç:").pack(pady=20)
Button(app, text="Dosya Seç", command=dosya_sec).pack()
Label(app, textvariable=dosya_yolu_var).pack(pady=10)

Button(app, text="Hesapla", command=stok_yaslandirma).pack(pady=20)
Label(app, text="Sonuç:").pack()
Label(app, textvariable=sonuc_var).pack(pady=10)

Button(app, text="Sonuçları Excel'e Aktar", command=sonuclari_excel_aktar).pack(pady=20)

app.mainloop()