# Ustalamy bazowy obraz na Python 3.11.2
FROM python:3.11.2

# Aktualizujemy indeks pakietów i instalujemy niezbędne biblioteki systemowe
RUN apt-get update && apt-get install -y \
    # Biblioteka do obsługi formatu JPEG
    libjpeg-dev \
    # Biblioteka do obsługi kompresji danych
    zlib1g-dev \
    # Biblioteka do obsługi formatu PNG
    libpng-dev \
    # Usuwamy niepotrzebne pliki, aby zminimalizować rozmiar obrazu
    && rm -rf /var/lib/apt/lists/*

# Ustalamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy plik z wymaganiami do katalogu roboczego
COPY requirements.txt /app/requirements.txt

# Instalujemy zależności dla Pythona zdefiniowane w pliku requirements.txt
RUN pip install -r requirements.txt

# Kopiujemy wszystkie pozostałe pliki i katalogi do katalogu roboczego
COPY . /app

# Otwieramy port 8000
EXPOSE 8000

# Uruchamiamy serwer Django po 10-sekundowym uśpieniu
# Sleep jest używany, aby upewnić się, że inne zależne usługi są gotowe
CMD sleep 10 && python manage.py runserver 0.0.0.0:8000
