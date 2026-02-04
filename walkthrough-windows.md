# Guida all'avvio - Windows

## Prerequisiti

Assicurati di avere **Python 3.10+** installato.
Durante l'installazione di Python, ricorda di spuntare la casella **"Add Python to PATH"**.

Per verificare se è installato, apri PowerShell o Prompt dei Comandi e scrivi:

```powershell
python --version
```

## Installazione

1. Apri la cartella del progetto.
2. Clicca con il tasto destro in uno spazio vuoto e seleziona "Apri nel Terminale" (o apri PowerShell/CMD e naviga nella cartella).
3. Crea un virtual environment:
   ```powershell
   python -m venv .venv
   ```
4. Attiva l'environment:
   - **PowerShell**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
     _Nota: Se ricevi un errore sui permessi, esegui `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` e riprova._
   - **CMD (Prompt dei Comandi)**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
5. Installa le librerie richieste:
   ```powershell
   pip install -r requirements.txt
   ```

## Avviare il Programma

1. Assicurati che l'environment sia attivo (dovresti vedere `(.venv)` all'inizio della riga). Se no, attivalo come descritto sopra.
2. Lancia il file principale:
   ```powershell
   python main.py
   ```
