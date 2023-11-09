from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox  # ttk paketini içe aktar
from tkinter import messagebox

def hesapla():
    try:
        toplam_palet = int(toplam_palet_entry.get())
        depo_calisma_saatleri = float(depo_calisma_saatleri_entry.get())
        siparis_saat_secim = siparis_saat_combobox.get()
        siparis_saat = float(siparis_saat_entry.get())
        sevkiyat_saat_secim = sevkiyat_saat_combobox.get()
        sevkiyat_saat = float(sevkiyat_saat_entry.get())
        palet_toplama_suresi = float(palet_toplama_suresi_entry.get())
        ikinci_onay_suresi = float(ikinci_onay_suresi_entry.get())
        etiketleme_suresi = float(etiketleme_suresi_entry.get())
        stretch_kapama_suresi = float(stretch_kapama_suresi_entry.get())

        # Sipariş saati hesaplaması
        if siparis_saat_secim == "n-1":
            siparis_saat = sevkiyat_saat - 1.5  # n-1 inci günün 17.00 saatine gelmesi gerekiyor
        else:
            siparis_saat = sevkiyat_saat - 24 + 5.5  # n inci günün 05.30 saatine gelmesi gerekiyor

        # İşçi ihtiyacı hesaplama
        palet_toplama_isci = (toplam_palet * palet_toplama_suresi) / (depo_calisma_saatleri * 60)
        ikinci_onay_isci = (toplam_palet * ikinci_onay_suresi) / (depo_calisma_saatleri * 60)
        etiketleme_isci = (toplam_palet * etiketleme_suresi) / (depo_calisma_saatleri * 60)
        stretch_kapama_isci = (toplam_palet * stretch_kapama_suresi) / (depo_calisma_saatleri * 60)

        toplam_isci_ihtiyaci = palet_toplama_isci + ikinci_onay_isci + etiketleme_isci + stretch_kapama_isci

        sonuc.set(f"Toplam İşçi İhtiyacı: {toplam_isci_ihtiyaci:.2f} işçi")

    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler girin.")

app = Tk()
app.title("İşçi İhtiyacı Hesaplama")

# Girdi alanları
Label(app, text="Toplam Palet Sayısı:").grid(row=0, column=0)
toplam_palet_entry = Entry(app)
toplam_palet_entry.grid(row=0, column=1)

Label(app, text="Depo Çalışma Saatleri (saat/gün):").grid(row=1, column=0)
depo_calisma_saatleri_entry = Entry(app)
depo_calisma_saatleri_entry.grid(row=1, column=1)

Label(app, text="Sipariş Saati (n-1/n):").grid(row=2, column=0)
siparis_saat_combobox = Combobox(app, values=["n-1", "n"])
siparis_saat_combobox.grid(row=2, column=1)

Label(app, text="Sipariş Saati (saat):").grid(row=3, column=0)
siparis_saat_entry = Entry(app)
siparis_saat_entry.grid(row=3, column=1)

Label(app, text="Sevkiyat Saati (n-1/n):").grid(row=4, column=0)
sevkiyat_saat_combobox = Combobox(app, values=["n-1", "n"])
sevkiyat_saat_combobox.grid(row=4, column=1)

Label(app, text="Sevkiyat Saati (saat):").grid(row=5, column=0)
sevkiyat_saat_entry = Entry(app)
sevkiyat_saat_entry.grid(row=5, column=1)

Label(app, text="Palet Toplama Süresi (dk/palet):").grid(row=6, column=0)
palet_toplama_suresi_entry = Entry(app)
palet_toplama_suresi_entry.grid(row=6, column=1)

Label(app, text="İkinci Onay Süresi (dk/palet):").grid(row=7, column=0)
ikinci_onay_suresi_entry = Entry(app)
ikinci_onay_suresi_entry.grid(row=7, column=1)

Label(app, text="Etiketleme Süresi (dk/palet):").grid(row=8, column=0)
etiketleme_suresi_entry = Entry(app)
etiketleme_suresi_entry.grid(row=8, column=1)

Label(app, text="Stretch/Kapama Süresi (dk/palet):").grid(row=9, column=0)
stretch_kapama_suresi_entry = Entry(app)
stretch_kapama_suresi_entry.grid(row=9, column=1)

Button(app, text="Hesapla", command=hesapla).grid(row=10, column=0, columnspan=2)

# Sonuç alanı
sonuc = StringVar()
Label(app, textvariable=sonuc).grid(row=11, column=0, columnspan=2)

app.mainloop()
