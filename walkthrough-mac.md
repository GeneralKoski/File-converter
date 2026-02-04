# Guida all'avvio - macOS

## Prerequisiti

Assicurati di avere **Python 3.10+** installato.
Puoi verificarlo aprendo il Terminale e scrivendo:

```bash
python3 --version
```

Se non è installato, puoi scaricarlo da [python.org](https://www.python.org/downloads/) o installarlo via Homebrew: `brew install python`.

## Installazione Automatica (Consigliata)

Nella cartella del progetto, esegui lo script di setup:

1. Apri il Terminale nella cartella del progetto.
2. Esegui il comando:
   ```bash
   ./setup.sh
   ```
   _Nota: Se ti dice "permission denied", dai i permessi con `chmod +x setup.sh` e riprova._

## Installazione Manuale

Se preferisci fare tutto a mano:

1. Crea un virtual environment:
   ```bash
   python3 -m venv .venv
   ```
2. Attiva l'environment:
   ```bash
   source .venv/bin/activate
   ```
3. Installa le librerie richieste:
   ```bash
   pip install -r requirements.txt
   ```

## Avviare il Programma

1. Assicurati che l'environment sia attivo (dovresti vedere `(.venv)` all'inizio della riga nel terminale). Se no, attiva con `source .venv/bin/activate`.
2. Lancia il file principale:
   ```bash
   python main.py
   ```
