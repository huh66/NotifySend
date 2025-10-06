# NotifySend

Ein C# Windows-Kommandozeilenprogramm zum Senden von Nachrichten über TCP-Sockets.

## Beschreibung

NotifySend ist ein einfaches Konsolenprogramm, das strukturierte Nachrichten im JSON-Format über TCP an einen Zielserver sendet. Es eignet sich besonders für Benachrichtigungen und Logging-Systeme.

## Features

- Senden von Nachrichten über TCP-Sockets
- JSON-Formatierung der Nachrichten
- Konfigurierbare Parameter (Header, Level, Subject, etc.)
- Deutsche Lokalisierung
- Einfache Kommandozeilenoberfläche

## Voraussetzungen

- .NET 8.0 oder höher
- Windows-Betriebssystem

## Installation

1. Repository klonen:
```bash
git clone <repository-url>
cd NotifySend
```

2. Projekt kompilieren:
```bash
dotnet build
```

3. Ausführbare Datei erstellen:
```bash
dotnet publish -c Release
```

## Verwendung

### Syntax

```
NotifySend.exe MESSAGE=<Text> IPV4=<Address> [Parameter...]
```

### Parameter

| Parameter | Typ | Erforderlich | Standard | Beschreibung |
|-----------|-----|--------------|----------|--------------|
| `MESSAGE` | String | Ja | - | Der zu sendende Nachrichtentext |
| `IPV4` | String | Ja | - | Ziel-IP-Adresse |
| `HEADER` | String | Nein | "INFORMATION" | Header der Nachricht |
| `LEVEL` | String | Nein | "INFO" | Log-Level (INFO, WARN, ERROR) |
| `SUBJECT` | String | Nein | "" | Betreff der Nachricht |
| `REFERENZ` | Integer | Nein | 0 | Referenznummer |
| `PORT` | Integer | Nein | 1526 | Ziel-Port |

### Beispiele

**Einfache Nachricht:**
```bash
NotifySend.exe MESSAGE="Test-Nachricht" IPV4=127.0.0.1
```

**Nachricht mit allen Parametern:**
```bash
NotifySend.exe MESSAGE="Fehler aufgetreten" IPV4=192.168.1.100 LEVEL=ERROR HEADER="SYSTEM" SUBJECT="Kritischer Fehler" REFERENZ=12345 PORT=8080
```

**Hilfe anzeigen:**
```bash
NotifySend.exe --help
```

## JSON-Nachrichtenformat

Das Programm sendet Nachrichten im folgenden JSON-Format:

```json
{
    "HEADER": "INFORMATION",
    "LEVEL": "INFO",
    "SUBJECT": "Betreff",
    "REFERENZ": 0,
    "MESSAGE": "Nachrichtentext"
}
```

## Fehlerbehandlung

- Bei Verbindungsfehlern wird eine entsprechende Fehlermeldung ausgegeben
- Ungültige Parameter führen zur Anzeige der Hilfe
- Fehlende erforderliche Parameter werden erkannt und gemeldet

## Entwicklung

### Projektstruktur

```
NotifySend/
├── NotifySend.cs          # Hauptprogramm
├── NotifySend.csproj      # Projektdatei
├── NotifySend.sln         # Visual Studio Solution
└── README.md              # Diese Datei
```

### Kompilierung

```bash
# Debug-Version
dotnet build

# Release-Version
dotnet build -c Release

# Veröffentlichung
dotnet publish -c Release -r win-x64 --self-contained
```

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe LICENSE-Datei für Details.

## Beitragen

Beiträge sind willkommen! Bitte erstellen Sie einen Pull Request oder melden Sie Fehler über die Issues-Funktion.

## Changelog

### Version 1.0.0
- Initiale Version
- Grundlegende TCP-Kommunikation
- JSON-Nachrichtenformat
- Kommandozeilenparameter-Unterstützung
