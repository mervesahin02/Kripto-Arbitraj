from api import get_price_from_binance, get_price_from_coinbase, get_price_from_kraken
from tkinter import messagebox
from db_connection.database import get_db_connection
from mail import send_email

def check_arbitrage(coin, esik_fiyat,email=None):
    binance = get_price_from_binance(coin)
    coinbase = get_price_from_coinbase(coin)
    kraken = get_price_from_kraken(coin)

    if not binance or not coinbase or not kraken:
        messagebox.showinfo("UYARI", f"{coin} için coin bilgisi mevcut değil!")
        return {"fiyat_farki": None, "en_dusuk_borsa": "Bilinmiyor"}

    prices = [
        {"isim": binance["borsa"], "fiyat": binance["fiyat"]},
        {"isim": coinbase["borsa"], "fiyat": coinbase["fiyat"]},
        {"isim": kraken["borsa"], "fiyat": kraken["fiyat"]}
    ]

    prices.sort(key=lambda x: x["fiyat"])
    en_dusuk_borsa = prices[0]["isim"]
    min_price = prices[0]["fiyat"]
    max_price = prices[-1]["fiyat"]

    fiyat_farki = round(max_price - min_price, 4)

    if fiyat_farki >= esik_fiyat:
        messagebox.showinfo("UYARI", f"{coin} için eşik fiyat aşıldı.\nEn Düşük Borsa: {en_dusuk_borsa}\nFiyat Farkı: {fiyat_farki} USD")
        if email:
            subject = f"{coin} Arbitraj Uyarısı"
            body = (
                f"{coin} için eşik fiyat aşıldı.\n"
                f"En Düşük Borsa: {en_dusuk_borsa}\n"
                f"Fiyat Farkı: {fiyat_farki} USD"
            )
            send_email(email, subject, body)
    insert_price_to_db(coin, binance["fiyat"], coinbase["fiyat"], kraken["fiyat"], fiyat_farki, en_dusuk_borsa)
    return {
        "coin": coin,
        "fiyat_farki": fiyat_farki,
        "en_dusuk_borsa": en_dusuk_borsa,
        "b": binance["fiyat"],
        "c": coinbase["fiyat"],
        "k": kraken["fiyat"]
    }

def insert_price_to_db(coin, binance_price, coinbase_price, kraken_price, fiyat_farki, en_dusuk_borsa):
    table_name = f"{coin.lower()}_prices"
    query = f"""
        INSERT INTO {table_name} (binance_price, coinbase_price, kraken_price, fiyat_farki, en_dusuk_borsa)
        VALUES (%s, %s, %s, %s, %s)
    """

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(query, (binance_price, coinbase_price, kraken_price, fiyat_farki, en_dusuk_borsa))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        print("Veritabanı bağlantısı başarısız.")
