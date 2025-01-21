import requests

def get_price_from_binance(symbol):
    try:
        response = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT', timeout=5)
        data = response.json()
        return {"borsa": "BINANCE", "fiyat": float(data['price'])}
    except Exception as e:
        print(f"Binance API hatası ({symbol}): {e}")
        return None

def get_price_from_coinbase(symbol):
    try:
        response = requests.get(f'https://api.coinbase.com/v2/prices/{symbol}-USD/spot', timeout=5)
        data = response.json()
        return {"borsa": "COINBASE", "fiyat": float(data['data']['amount'])}
    except Exception as e:
        print(f"Coinbase API hatası ({symbol}): {e}")
        return None

def get_price_from_kraken(symbol):
    try:
        symbol_mapping = {"BTC": "XXBTZUSD", "ETH": "XETHZUSD", "LTC": "XLTCZUSD"}
        kraken_symbol = symbol_mapping.get(symbol, "XXBTZUSD")  # Default to BTC if not found
        response = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={kraken_symbol}', timeout=5)
        data = response.json()
        return {"borsa": "KRAKEN", "fiyat": float(data['result'][kraken_symbol]['c'][0])}
    except Exception as e:
        print(f"Kraken API hatası ({symbol}): {e}")
        return None
