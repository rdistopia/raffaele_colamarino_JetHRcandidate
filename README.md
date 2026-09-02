# Jet HR - Calcolatore Retribuzione Netta da RAL
**Candidatura Product Builder | Raffaele Colamarino**

---

### 1. Visione a Lungo Termine e Parametrizzazione Fiscale (Database Modificabile)
Ho reso il Database completamente modificabile pensando a un utilizzo long-term e considerando le continue variazioni dovute a modifiche alla legislatura (es. riforme IRPEF, manovre di bilancio e aggiornamenti delle addizionali locali). Attraverso l'interfaccia dedicata, ogni parametro, aliquota e scaglione può essere aggiornato direttamente a database senza dover intervenire sul codice applicativo, garantendo continuità e scalabilità del prodotto nel tempo.

---

### 2. Ricerca Autonoma delle Fonti e Schema di Calcolo
Per lo sviluppo ho ragionato autonomamente sui requisiti della task e ho personalmente cercato le fonti; vista la vastità dell'argomento e la necessità di utilizzare fonti certe per il motore di calcolo, ho optato per l'utilizzo come fonte primaria dei documenti presenti sul sito di Jet HR alla sezione Help Center, scaricando quelli più inerenti come HTML da estrarre successivamente in un Excel in formato .csv che ne contenesse i parametri necessari al prototipo.  

Nella cartella `Architettura/` è anche presente lo **Schema di Calcolo** (`schema_di_calcolo_.txt`) su cui si basa il prototipo, anch'esso dedotto e strutturato fedelmente secondo la metodologia documentata nell'Help Center del sito.

---

### 3. Architettura delle Cartelle
Ho elaborato l'architettura delle cartelle in modo che ogni file fosse facilmente consultabile, separando nettamente il motore di calcolo puro, la persistenza su database, l'interfaccia web e i test automatizzati:

```text
Jet_HR/
├── .gitignore                          # File di esclusione Git (venv, __pycache__, .env, *.pyc, db locali)
├── README.md                           # Presentazione del progetto, assunzioni e motivazioni
├── requirements.txt                    # Dipendenze Python (Flask, pytest, ecc.)
├── run.py                              # Entrypoint per l'avvio in ambiente di sviluppo locale (python run.py)
├── wsgi.py                             # WSGI entrypoint dedicato per il deployment su PythonAnywhere
│
├── Architettura/                       # Documentazione tecnica, di processo e requisiti di business
│   ├── Processo.txt                    # Flusso delle fasi operative dal setup al rilascio
│   ├── requisiti.txt                   # Specifiche e vincoli (Sempre valido & Iterazione 1)
│   ├── task_candidatura.txt            # Traccia originale del task Product Builder
│   ├── schema_di_calcolo_.txt          # Specifiche matematiche e pipeline di calcolo Jet HR
│   └── architettura_cartelle.txt       # Struttura e organizzazione logica del repo
│
├── Fonti/                              # Raccolta ed estrazione delle fonti normative e di dominio
│   ├── Jet_HR_Help_Center/             # Articoli di riferimento Jet HR (CCNL, contributi, novità legislative)
│   │   ├── CCNL/
│   │   ├── Contributi_e_tasse/
│   │   ├── Costo_Azienda/
│   │   ├── Novità_Legislative/
│   │   └── Altro/
│   ├── Ministero_dell'Economia_e_delle_Finanze/ # Fonti ufficiali MEF (aliquote regionali/comunali, delibere)
│   └── sintesi_normativa_2024_2025.md  # Scheda di sintesi con regole, formule e aliquote estratte
│
├── app/                                # Pacchetto applicativo principale (Web App Flask)
│   ├── __init__.py                     # Application Factory (creazione istanza Flask, filtri Jinja, setup DB)
│   │
│   ├── core/                           # Engine di calcolo (Puro Python, disaccoppiato dal Web e da Flask)
│   │   ├── __init__.py
│   │   ├── calculator.py               # Orchestratore del calcolo (RAL -> Imponibili -> Trattenute -> Netto)
│   │   ├── deductions.py               # Calcolo detrazioni da lavoro dipendente (art. 13 TUIR)
│   │   ├── formatters.py               # Helper formattazione italiana (punto migliaia, virgola decimali)
│   │   ├── models.py                   # Data class per input e breakdown trasparente
│   │   └── taxes.py                    # Calcolo scaglioni IRPEF, Addizionale Lombardia e Milano
│   │
│   ├── database/                       # Gestione della persistenza e parametri modificabili
│   │   ├── __init__.py
│   │   ├── db.py                       # Gestione connessione SQLite e helper query/transazioni
│   │   ├── schema.sql                  # Schema DDL (tabelle per scaglioni IRPEF, aliquote INPS, addizionali)
│   │   ├── seed_data.json              # Valori di default ufficiali per il ripristino di fabbrica
│   │   └── parameters.db               # Database SQLite leggero e portabile per PythonAnywhere
│   │
│   ├── routes/                         # Controller e gestione endpoint HTTP (Blueprint Flask)
│   │   ├── __init__.py
│   │   ├── main_routes.py              # Vista calcolatore (GET/POST '/', input manuale e breakdown)
│   │   ├── admin_routes.py             # Vista gestione parametri (GET/POST '/parametri', UI modifiche DB)
│   │   ├── api_routes.py               # Endpoint API REST (POST '/api/calculate', GET/PUT '/api/parameters')
│   │   └── deploy_webhook.py           # Webhook protetto da Token per auto-update Git su PythonAnywhere
│   │
│   ├── templates/                      # Template Jinja2 per la UI HTML (Responsive & Brand Identity)
│   │   ├── base.html                   # Layout base (header, navbar, footer personalizzato)
│   │   ├── calculator.html             # Pagina principale del Calcolatore (input manuale con decimali)
│   │   ├── parameters.html             # Interfaccia grafica con tabelle scaglioni interamente modificabili
│   │   └── components/                 # Componenti UI modulari riutilizzabili
│   │       ├── _breakdown_table.html   # Tabella trasparente con dettaglio voci lorde, contributi, imposte e netto
│   │       └── _alerts.html            # Flash messages (notifiche salvataggio modifiche parametri)
│   │
│   └── static/                         # Risorse statiche lato client
│       ├── css/
│       │   └── style.css               # Stili CSS personalizzati (design moderno, pulito e user-friendly)
│       ├── js/
│       │   ├── calculator.js           # Gestione interattività calcolatore e validazione input
│       │   └── parameters.js           # Gestione form parametri
│       └── img/
│           └── logo_jet_hr.svg         # Asset grafici
│
├── tests/                              # Suite di test automatizzati (garanzia di correttezza e trasparenza logiche)
│   ├── __init__.py
│   ├── test_calculator.py              # Test unitari sul calcolo (validazione ufficiale RAL 30k Jet HR)
│   ├── test_formatters.py              # Test unitari sulla formattazione italiana globale
│   ├── test_parameters.py              # Test di lettura, modifica e persistenza parametri nel database
│   └── test_routes.py                  # Test di integrazione delle rotte web, decimali e API
│
└── scripts/                            # Script di automazione e manutenzione
    ├── init_db.py                      # Script di inizializzazione/ripristino rapido del database SQLite
    └── update_pythonanywhere.sh        # Script bash per git pull e reload WSGI su PythonAnywhere
```

---

### 4. Scelta dello Stack Tecnologico (Python & PythonAnywhere)
Ho deciso di utilizzare Python e PythonAnywhere come deployer dato che negli ultimi mesi ho lavorato spesso con questa stack e la sentivo più confident, nonostante sia consapevole di soluzioni più semplici che non richiedono backend, come Vercel. Questa scelta mi ha consentito di strutturare una solida architettura client-server con SQLite locale e API REST integrate.

---

### 5. Metodologia di Sviluppo AI-Native e Controlli Incrociati
L'applicazione è stata vibe-codata utilizzando **Antigravity/Gemini 3.8** e ho applicato controlli incrociati con **Codex** per valutare e risolvere criticamente i punti più delicati (come le discrepanze tra delibere MEF locali e semplificazioni da help center, la gestione dei decimali italiani e la persistenza dinamica degli scaglioni).
