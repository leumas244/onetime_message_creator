# Django Dashboard-Template

## Was ist das Django Dashboard-Template?

Dieses Projekt ist eine Vorlage für Django-Webseiten, welche hauptsächlich ein Dashboard nutzen. Die Vorlage hat diese
fertigen Funktionen:

- Login- / Logout-Funktion
- Lightmode / Darkmode
- Benachrichtigungen in der Topbar
- Einstellungsänderungen
- Passwortänderungen

## Anleitung zum Nutzen der Vorlage
Ab hier gibt es ein kleines HandsOn wie das Projekt lokal initialisiert wird.

### 1. Projekt umbenennen

Das Projekt sollte nach dem Klonen direkt umbenannt werden. Dafür wird der Root-Ordner
(der Ordner, der durch das Klonen erzeugt wurde) im Dateiexplorer umbenannt. Dann muss im Root-Ordner der Ordner
"onetime_message_creator" über Refactor->Rename umbenannt werden. Am besten man nennt das Projekt so wie das Git-Repo.

(Fals in settings.py Zeile 54 nicht geändert wird muss diese geändert werden.)

### 2. Git remote Host ändern

Nun sollte das Projekt auf ein anderes Repro gestellt werden. Dafür ein Repro erstellen und dann folgenden Befehle:

```
git remote set-url origin <MEIN_REPO_LINK>
git remote -v
```

### 3. Datenbank initialisieren

Als Erstes, muss die Datenbank initialisiert werden. Diese bleibt durch die gitignore IMMER lokal. Mit dem Befehl:

```
python manage.py migrate
```

### 4. Superuser erstellen

Danach wird ein Admin-User gebraucht. Dieser wird mit nachfolgendem Befehl erstellt:

```
python manage.py createsuperuser
```

### 5. Server starten und betreiben

- Nun kann der Server gestartet werden.

```
python manage.py runserver
```

- Um im Nachhinein neue Datenbank Tabellen zu erstellen oder ändern, müssen während der Server ausgeschaltet ist, zwei
  weitere Befehle in dieser Reihenfolge ausgeführt werden.

```
python manage.py makemigrations
# Dann
python manage.py migrate
```
