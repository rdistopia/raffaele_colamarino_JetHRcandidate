# Jet HR - Calcolatore Retribuzione Netta da RAL

Prototipo funzionante sviluppato per la candidatura a **Product Builder @ Jet HR**.  
L'applicazione simula la proiezione della retribuzione netta annuale e mensile partendo dalla RAL, mostrando con trasparenza tutte le voci trattenute al lordo secondo la metodologia documentata dall'Help Center di Jet HR.

---

## Caratteristiche Principali

1. **Motore Fiscale Modulare (Pure Python)**:
   - Disaccoppiato dal framework web per garantire facilità di test, manutenzione ed estendibilità.
   - Calcolo strutturato sui **5 step ufficiali Jet HR**:
     - *Step 1*: Deduzione contributi previdenziali IVS (9,19%) per determinare l'imponibile fiscale.
     - *Step 2*: Calcolo imposte lorde (IRPEF a 3 scaglioni 2024, Addizionale Regionale Lombardia e Addizionale Comunale Milano).
     - *Step 3*: Calcolo detrazioni da lavoro dipendente (Art. 13 TUIR con maggiorazione).
     - *Step 4*: Determinazione dell'imposta netta effettiva a debito.
     - *Step 5*: Netto annuale e netto mensile parametrizzabile su 12, 13 o 14 mensilità.

2. **Database SQLite con Parametri Modificabili via UI**:
   - Conforme al requisito: *"Il database con le logiche di calcolo deve essere apribile dall'app con una UI user friendly e, data la variabilità, i parametri devono essere modificabili"*.
   - Interfaccia dedicata in `/parametri` per modificare aliquote, scaglioni e soglie di esenzione.
   - Pulsante integrato *"Ripristina Valori di Fabbrica"* per ripristinare in sicurezza i parametri di default.

3. **Compatibilità Nativa con PythonAnywhere e GitHub**:
   - File `wsgi.py` pronto per l'hosting WSGI su PythonAnywhere.
   - Webhook di deploy `/api/deploy?token=...` e script `scripts/update_pythonanywhere.sh` per aggiornamenti rapidi via GitHub.

---

## Architettura del Repository

```text
Jet_HR/
├── run.py                          # Entrypoint per sviluppo locale
├── wsgi.py                         # Entrypoint WSGI per PythonAnywhere
├── requirements.txt                # Dipendenze (Flask, pytest, ecc.)
├── Architettura/                   # Specifiche, processo, requisiti e schema di calcolo
├── Fonti/                          # Raccolta ed estrazione delle fonti Help Center e MEF
├── app/                            # Applicazione Web Flask
│   ├── core/                       # Motore di calcolo puro (calculator, taxes, deductions, models)
│   ├── database/                   # SQLite, schema DDL, seed data e helper
│   ├── routes/                     # Blueprint web e API (main, admin, api, deploy)
│   ├── templates/                  # Template HTML Jinja2 e componenti modulari
│   └── static/                     # CSS custom, JS interattivo e asset grafici
├── tests/                          # Suite di test automatizzati (TDD su logiche e rotte)
└── scripts/                        # Script standalone di utilità (init_db, deploy)
```

---

## Avvio Rapido in Locale

### 1. Prerequisiti
- Python 3.10 o superiore.

### 2. Installazione delle Dipendenze
```bash
pip install -r requirements.txt
```

### 3. Inizializzazione Database
```bash
python scripts/init_db.py
```

### 4. Esecuzione dei Test
```bash
pytest
```

### 5. Avvio del Server Locale
```bash
python run.py
```
L'applicazione sarà accessibile su `http://127.0.0.1:5000`.

---

## Deployment su PythonAnywhere

1. Clonare la repository nella directory home di PythonAnywhere:
   ```bash
   git clone <URL_REPO_GITHUB>
   ```
2. Nella scheda **Web** di PythonAnywhere, creare una nuova web app selezionando **Manual Configuration (Flask)** con Python 3.10+.
3. Nel file di configurazione WSGI di PythonAnywhere, importare l'applicazione:
   ```python
   import sys
   path = '/home/<tuo-username>/Jet_HR'
   if path not in sys.path:
       sys.path.insert(0, path)

   from wsgi import application
   ```
4. Eseguire `python scripts/init_db.py` dalla console Bash di PythonAnywhere.
5. Cliccare su **Reload** nella dashboard di PythonAnywhere.
