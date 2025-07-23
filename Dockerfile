# Python 3.11 tabanlı küçük imaj
FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Flask için environment değişkenleri
ENV FLASK_APP=flask_app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1

# Uygulama portu
EXPOSE 5000

# Başlat
CMD ["flask", "run"]
