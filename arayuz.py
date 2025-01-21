import tkinter as tk
from tkinter import messagebox, Toplevel
from db_connection.database import get_db_connection
from PIL import Image, ImageDraw, ImageTk
from design_fun import create_rounded_button,create_gradient_label
from tkinter.ttk import Combobox
from veri_isle import check_arbitrage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


after_id = None
def log_window():
    global login_window,logged_in_user

    def open_register_window():
        register_window = Toplevel()
        register_window.title("Kayıt Ol")
        register_window.geometry("500x300")
        register_window.resizable(False, False)
        login_window.withdraw()
        register_window.protocol("WM_DELETE_WINDOW", lambda: [login_window.deiconify(), register_window.destroy()])

        screen_width = register_window.winfo_screenwidth()
        screen_height = register_window.winfo_screenheight()
        window_width = 500
        window_height = 300
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        register_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

        canvas = tk.Canvas(register_window, width=500, height=500, bg="#faebd7", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        canvas.image_refs = []

        # Kullanıcı adı giriş label
        create_gradient_label(canvas, 25, 50, "Kullanıcı Adı:", width=200, height=30)
        username_entry = tk.Entry(register_window, font=("Arial", 12))
        canvas.create_window(350, 65, window=username_entry, width=200, height=30)

        # E-posta giriş label
        create_gradient_label(canvas, 25, 100, "E-posta:", width=200, height=30)
        email_entry = tk.Entry(register_window, font=("Arial", 12))
        canvas.create_window(350, 115, window=email_entry, width=200, height=30)

        # Şifre giriş label
        create_gradient_label(canvas, 25, 150, "Şifre:", width=200, height=30)
        password_entry = tk.Entry(register_window, show="*", font=("Arial", 12))
        canvas.create_window(350, 165, window=password_entry, width=200, height=30)

        # Kayıt ol butonu
        register_button = tk.Button(register_window, text="Kayıt Ol", font=("Arial", 12, "bold"), bg="#00cd00",
                                    fg="white", command=lambda: register_user(username_entry.get(), email_entry.get(),
                                                                              password_entry.get(), register_window))
        canvas.create_window(250, 250, window=register_button, width=150, height=40)

    def register_user(username, email, password, window):

        if not username or not email or not password:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return

        connection = get_db_connection()
        if connection is None:
            messagebox.showerror("Hata", "Veritabanı bağlantısı kurulamadı!")
            return

        cursor = connection.cursor()
        try:
            query = """
            INSERT INTO users (kullanici_adi, email, sifre) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (username, email, password))
            connection.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarılı! Giriş yapabilirsiniz.")
            window.destroy()
            login_window.deiconify()
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt sırasında hata oluştu: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    # Giriş yapan kullanıcı bilgilerini saklamak için global değişkenler
    logged_in_user = {"username": None, "email": None}

    def login_user():
        global logged_in_user
        username = username_entry.get()
        password = password_entry.get()
        connection = get_db_connection()
        if not username or not password:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun!")
            return
        if connection is None:
            messagebox.showerror("Hata", "Veritabanı bağlantısı kurulamadı!")
            return

        cursor = connection.cursor()
        try:
            query = """
            SELECT kullanici_adi, email FROM users WHERE kullanici_adi = %s AND sifre = %s
            """
            cursor.execute(query, (username, password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo("Başarılı", "Giriş başarılı!")
                # Kullanıcı bilgilerini sakla
                logged_in_user["username"] = user[0]
                logged_in_user["email"] = user[1]
                login_window.withdraw()
                main_arayuz()
            else:
                messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")
        except Exception as e:
            messagebox.showerror("Hata", f"Giriş sırasında hata oluştu: {e}")
        finally:
            cursor.close()
            connection.close()

    login_window = tk.Tk()
    login_window.title("Giriş Yap")
    login_window.geometry("500x300")
    login_window.resizable(False, False)

    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    window_width = 500
    window_height = 300
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    login_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    # Canvas oluştur
    canvas = tk.Canvas(login_window, width=500, height=300, bg="#faebd7", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.image_refs = []

    # Kullanıcı adı giriş label
    create_gradient_label(canvas, 50, 50, "Kullanıcı Adı:", width=150, height=30)
    username_entry = tk.Entry(login_window, font=("Arial", 12))
    canvas.create_window(350, 65, window=username_entry, width=200, height=30)

    # Şifre giriş label
    create_gradient_label(canvas, 50, 100, "Şifre:", width=150, height=30)
    password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
    canvas.create_window(350, 115, window=password_entry, width=200, height=30)

    # Giriş butonu
    login_button = tk.Button(login_window, text="Giriş Yap", font=("Rockwell", 12, "bold"), bg="#00cd00",
                             fg="white",
                             command=login_user)
    canvas.create_window(250, 200, window=login_button, width=150, height=40)

    # Kayıt ol butonu
    register_button = tk.Button(login_window, text="Kayıt Ol", font=("Rockwell", 12, "bold"), bg="#cd2626",
                                fg="white", command=open_register_window)
    canvas.create_window(250, 260, window=register_button, width=150, height=40)

    login_window.mainloop()



def main_arayuz():
    def update_canvas(data):
        canvas.itemconfig(fiyat_farki_text, text=f"{data['fiyat_farki']} USD")
        canvas.itemconfig(binance_price_text, text=f"{data['b']} USD")
        canvas.itemconfig(coinbase_price_text, text=f"{data['c']} USD")
        canvas.itemconfig(kraken_price_text, text=f"{data['k']} USD")
        canvas.itemconfig(en_dusuk_borsa_text, text=f"{data['en_dusuk_borsa']}")

    def update_prices():
        global after_id
        selected_coin = coin_var.get()
        esik_fiyat = esik_entry.get()

        if not selected_coin:
            messagebox.showerror("Hata", "Lütfen bir coin seçiniz!")
            return

        try:
            esik_fiyat = float(esik_fiyat)
        except ValueError:
            messagebox.showerror("Hata", "Eşik fiyat geçerli bir sayı olmalıdır!")
            return

        sonuc = check_arbitrage(selected_coin, esik_fiyat,email=logged_in_user["email"])
        update_canvas(sonuc)

        after_id = root.after(2000, update_prices)

    def baslat_takip():
        global after_id
        if after_id is None:
            update_prices()

    def durdur_takip():
        global after_id
        if after_id is not None:
            root.after_cancel(after_id)
            after_id = None
        canvas.itemconfig(fiyat_farki_text, text=f"--- USD")
        canvas.itemconfig(binance_price_text, text=f"--- USD")
        canvas.itemconfig(coinbase_price_text, text=f"--- USD")
        canvas.itemconfig(kraken_price_text, text=f"--- USD")
        canvas.itemconfig(en_dusuk_borsa_text, text=f"---")

    def show_graph():
        graph_window = Toplevel(root)
        graph_window.title(f"{coin_var.get()} - Canlı Fiyat Grafikleri")
        graph_window.geometry("1000x900")

        # Şekil ve eksenleri tanımla
        fig, axs = plt.subplots(2, 2, figsize=(8, 6))
        fig.suptitle(f"{coin_var.get()} Canlı Fiyat ve Fiyat Farkı Grafikleri")

        axs[0, 0].set_title("Binance Fiyatı")
        axs[0, 1].set_title("Coinbase Fiyatı")
        axs[1, 0].set_title("Kraken Fiyatı")
        axs[1, 1].set_title("Fiyat Farkı")

        for ax in axs.flat:
            ax.set_xlabel("Zaman")
            ax.set_ylabel("Fiyat (USD)")

        # Canlı veri listeleri
        timestamps = []
        binance_prices = []
        coinbase_prices = []
        kraken_prices = []
        fiyat_farklari = []

        # Canvas oluştur
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def update_graph():
            selected_coin = coin_var.get()
            esik_fiyat = esik_entry.get()

            try:
                esik_fiyat = float(esik_fiyat)
            except ValueError:
                esik_fiyat = 0.0

            # Veriyi güncelle
            sonuc = check_arbitrage(selected_coin, esik_fiyat)
            if sonuc:
                timestamps.append(len(timestamps) + 1)
                binance_prices.append(sonuc['b'])
                coinbase_prices.append(sonuc['c'])
                kraken_prices.append(sonuc['k'])
                fiyat_farklari.append(sonuc['fiyat_farki'])

                # Her bir grafiği temizle ve yeni veriyi ekle
                axs[0, 0].clear()
                axs[0, 0].plot(timestamps, binance_prices, label="Binance", color="orange")
                axs[0, 0].set_title("Binance Fiyatı")
                axs[0, 0].set_xlabel("Zaman")
                axs[0, 0].set_ylabel("Fiyat (USD)")

                axs[0, 1].clear()
                axs[0, 1].plot(timestamps, coinbase_prices, label="Coinbase", color="green")
                axs[0, 1].set_title("Coinbase Fiyatı")
                axs[0, 1].set_xlabel("Zaman")
                axs[0, 1].set_ylabel("Fiyat (USD)")

                axs[1, 0].clear()
                axs[1, 0].plot(timestamps, kraken_prices, label="Kraken", color="blue")
                axs[1, 0].set_title("Kraken Fiyatı")
                axs[1, 0].set_xlabel("Zaman")
                axs[1, 0].set_ylabel("Fiyat (USD)")

                axs[1, 1].clear()
                axs[1, 1].plot(timestamps, fiyat_farklari, label="Fiyat Farkı", color="red")
                axs[1, 1].set_title("Fiyat Farkı")
                axs[1, 1].set_xlabel("Zaman")
                axs[1, 1].set_ylabel("Fiyat Farkı (USD)")

                # Grafik çizimini yenile
                canvas.draw()

            # 2 saniye sonra tekrar çalıştır
            graph_window.after(2000, update_graph)

        update_graph()  # İlk güncelleme

    def geri_butonu():
        global after_id
        if after_id is not None:
            root.after_cancel(after_id)
            after_id = None
        root.destroy()
        login_window.deiconify()

    # Ana Arayüz
    root = tk.Toplevel()
    root.title("Kripto Arbitraj Takip Sistemi")
    root.geometry("1000x800")
    root.config(bg="#f0f0f0")
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", lambda: [login_window.deiconify(),root.destroy()])

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1000
    window_height = 800
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    canvas = tk.Canvas(root, width=1000, height=600, bg="#f0f0f0", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.image_refs = []
    bg_image_path = "C:\\Users\\candi\\PycharmProjects\\bmg\\background\\xd.png"
    try:
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((1000, 800), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.image = bg_photo  # Çöp toplayıcıdan korumak için referans
    except Exception as e:
        print(f"Arka plan yüklenirken hata oluştu: {e}")

    header_image_path = "C:\\Users\\candi\\PycharmProjects\\bmg\\background\\Arbitraj-Takip-Sistemi1.png"
    try:
        header_image = Image.open(header_image_path)
        header_image = header_image.resize((500, 82), Image.Resampling.LANCZOS)
        header_photo = ImageTk.PhotoImage(header_image)
        canvas.create_image(250, 5, image=header_photo, anchor="nw")
        canvas.image_refs.append(header_photo)  # Çöp toplayıcıdan korumak için referans
    except Exception as e:
        print(f"Başlık yüklenirken hata oluştu: {e}")

    canvas.create_rectangle(250, 415, 710, 520, fill="", outline="#828282", width=2)

    # Gradient Label - Coin Seçimi
    create_gradient_label(canvas, 260, 425, "Coin Seçiniz:", width=220, height=30)
    coin_var = tk.StringVar()
    coin_combobox = Combobox(root, textvariable=coin_var, font=("Arial", 12), state="readonly")
    coin_combobox["values"] = ["BTC", "ETH", "LTC"]
    coin_combobox.current(0)
    canvas.create_window(600, 440, window=coin_combobox, width=200, height=30)

    # Gradient Label - Eşik Fiyatı Girişi
    create_gradient_label(canvas, 260, 475, "Eşik Fiyatı Girin (USD):", width=220, height=30)
    esik_entry = tk.Entry(root, font=("Arial", 12))
    canvas.create_window(600, 490, window=esik_entry, width=200, height=30)

    # Gradient Label - Fiyat Gösterimi
    create_gradient_label(canvas, 275, 100, "Fiyat Farkı:", width=220, height=30)
    fiyat_farki_bg = canvas.create_rectangle(525, 105, 675, 125, fill="#d3d3d3", outline="")
    fiyat_farki_text = canvas.create_text(600, 115, text="--- USD", font=("Arial", 12, "bold"), fill="#333333")

    create_gradient_label(canvas, 275, 150, "Binance Fiyatı:", width=220, height=30)
    binance_fiyati_bg = canvas.create_rectangle(525, 155, 675, 175, fill="#d3d3d3", outline="")
    binance_price_text = canvas.create_text(600, 165, text="--- USD", font=("Arial", 12, "bold"), fill="#ff6600")

    create_gradient_label(canvas, 275, 200, "Coinbase Fiyatı:", width=220, height=30)
    coinbase_fiyati_bg = canvas.create_rectangle(525, 205, 675, 225, fill="#d3d3d3", outline="")
    coinbase_price_text = canvas.create_text(600, 215, text="--- USD", font=("Arial", 12, "bold"), fill="#009900")

    create_gradient_label(canvas, 275, 250, "Kraken Fiyatı:", width=220, height=30)
    kraken_fiyati_bg = canvas.create_rectangle(525, 255, 675, 275, fill="#d3d3d3", outline="")
    kraken_price_text = canvas.create_text(600, 265, text="--- USD", font=("Arial", 12, "bold"), fill="#0066cc")

    create_gradient_label(canvas, 275, 300, "En Düşük Fiyatlı Borsa:", width=220, height=30)
    en_düsük_borsa_bg = canvas.create_rectangle(525, 305, 675, 325, fill="#d3d3d3", outline="")
    en_dusuk_borsa_text = canvas.create_text(600, 315, text="---", font=("Arial", 12, "bold"), fill="#ff0000")

    # Yuvarlatılmış Butonlar
    create_rounded_button(canvas, 315, 550, "Takibi Başlat", baslat_takip, width=150, color="#00cd00")
    create_rounded_button(canvas, 515, 550, "Takibi Durdur", durdur_takip, width=150, color="#cd2626")
    create_rounded_button(canvas, 395, 625, "Grafiği Görüntüle", show_graph, width=200, color="#473c8b")
    create_rounded_button(canvas, 25, 725, "Çıkış", geri_butonu, width=100, color="#8b3a3a")

    root.mainloop()


log_window()