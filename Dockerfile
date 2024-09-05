# Verwenden Sie ein offizielles Python-Image als Basis
FROM python:3.11-slim

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die Anforderungen in den Container
COPY requirements.txt /app/

# Installieren Sie die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den Code in den Container
COPY . /app/

# Exponieren Sie den Port, den Django verwendet (z.B. 8000)
EXPOSE 8000

# Starten Sie den Django Development Server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
