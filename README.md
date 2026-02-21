# 🖼️ File Converter

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![Framework](https://img.shields.io/badge/UI-PySide6%20%7C%20Streamlit-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**File Converter** è un'applicazione versatile progettata per semplificare la gestione delle immagini. Offre la possibilità di convertire formati e rimuovere sfondi in pochi clic, attraverso un'interfaccia desktop nativa o un'applicazione web moderna.

---

## ✨ Funzionalità Principali

- **🔄 Conversione Formati**: Supporta PNG, JPG, JPEG, WEBP e BMP.
- **✂️ Rimozione Sfondo**: Algoritmo basato su AI per rimuovere lo sfondo dalle tue foto istantaneamente.
- **🖥️ Desktop App**: Interfaccia fluida e reattiva costruita con **PySide6**.
- **🌐 Web App**: Versione accessibile via browser sviluppata con **Streamlit**.
- **🎨 Design Moderno**: Tema scuro (Dark Mode) con estetica curata sia per desktop che per web.

---

## 🚀 Come Iniziare

### 📋 Prerequisiti

- **Python 3.10** o superiore.

### 🛠️ Installazione

Scarica il progetto e installa le dipendenze usando lo script automatizzato:

**macOS / Linux:**

```bash
./setup.sh
```

**Windows:**

```batch
setup.bat
```

---

## 🎮 Esecuzione

Sia per la versione Desktop che per la Web, assicurati di aver attivato l'ambiente virtuale:

```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 🔹 Desktop App

Lancia l'applicazione nativa:

```bash
python main.py
```

### 🔹 Web App

Avvia il server Streamlit:

```bash
streamlit run web_app.py
```

---

## 📂 Struttura del Progetto

- `main.py`: Entry point per l'applicazione desktop.
- `web_app.py`: Entry point per l'applicazione web.
- `services/`: Logica core per l'elaborazione delle immagini.
- `ui/`: Componenti e stili dell'interfaccia PySide6.
- `web/`: Componenti e stili dell'interfaccia Streamlit.
- `Saved/`: Cartella predefinita per i file salvati.

---

## 🛠️ Tecnologie Utilizzate

- **[PySide6](https://doc.qt.io/qtforpython/)**: Per l'interfaccia grafica desktop.
- **[Streamlit](https://streamlit.io/)**: Per l'interfaccia web interattiva.
- **[rembg](https://github.com/danielgatis/rembg)**: Per la rimozione intelligente dello sfondo.
- **[Pillow](https://python-pillow.org/)**: Per la manipolazione delle immagini.

---

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Consulta il file `LICENSE` per ulteriori dettagli (se presente).

---

_Sviluppato con ❤️ per rendere la conversione file più semplice._
