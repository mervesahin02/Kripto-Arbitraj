# 🪙 Kripto Arbitraj Botu
Bu proje, farklı kripto para borsaları arasındaki fiyat farklarını tespit ederek otomatik arbitraj işlemleri gerçekleştirmek amacıyla geliştirilmiştir. Python diliyle yazılmıştır ve API üzerinden veri çekme, analiz etme, kullanıcı arayüzü sunma ve e-posta bildirimleri gönderme gibi özellikler içerir.​

##🚀 Özellikler
Gerçek Zamanlı Veri Çekme: Borsalardan anlık fiyat verilerini alır.

Fiyat Farkı Analizi: Borsalar arasındaki fiyat farklarını hesaplar.

Kullanıcı Arayüzü: Kullanıcı dostu bir arayüz ile işlemleri yönetme imkanı sunar.

E-posta Bildirimleri: Belirlenen arbitraj fırsatları için e-posta yoluyla bildirim gönderir.​
## 🛠️ Kullanılan Teknolojiler

- Python
- [Requests](https://pypi.org/project/requests/)
- JSON & API kullanımı
- Binance API (veya başka borsalar)
- Terminal/komut satırı arayüzü
  
## 🧱 Dosya Yapısı
- api.py: Borsa API'leri ile iletişimi sağlar.
  
- veri_isle.py: Fiyat verilerini işler ve analiz eder.
  
- arayuz.py: Kullanıcı arayüzünü oluşturur.

- mail.py: E-posta bildirimlerini gönderir.

- design_fun.py: Arayüz tasarım fonksiyonlarını içerir.

- __init__.py: Modül tanımlayıcı dosya.​

