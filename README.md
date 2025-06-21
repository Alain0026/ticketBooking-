# 🎫 TicketBooking - Sistema di Prenotazione Eventi

<div align="center">
  <img src="https://img.shields.io/badge/Django-4.2.7-green.svg" alt="Django Version">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Bootstrap-5.3-purple.svg" alt="Bootstrap Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</div>

## 📋 Indice

- [Descrizione](#-descrizione)
- [Demo](#-demo)
- [Caratteristiche](#-caratteristiche)
- [Tecnologie](#-tecnologie)
- [Requisiti](#-requisiti)
- [Installazione](#-installazione)
- [Configurazione](#-configurazione)
- [Utilizzo](#-utilizzo)
- [Struttura del Progetto](#-struttura-del-progetto)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contribuire](#-contribuire)
- [Troubleshooting](#-troubleshooting)
- [Licenza](#-licenza)

## 🎯 Descrizione

**TicketBooking** è una piattaforma web completa per la prenotazione di biglietti per eventi, sviluppata con Django. Il sistema offre un'interfaccia moderna e intuitiva per la ricerca, visualizzazione e prenotazione di eventi, con un sistema di gestione utenti completo e API RESTful.

### 🎭 Tipologie di Eventi Supportate
- 🎵 Concerti
- 🎭 Teatro
- ⚽ Sport
- 🎤 Conferenze
- 🎪 Festival

## 🖼️ Demo

### Screenshots

| Homepage | Lista Eventi | Dettaglio Evento |
|----------|--------------|------------------|
| ![Homepage](https://via.placeholder.com/300x200?text=Homepage) | ![Eventi](https://via.placeholder.com/300x200?text=Lista+Eventi) | ![Dettaglio](https://via.placeholder.com/300x200?text=Dettaglio) |

### 🔐 Credenziali Demo

| Tipo Utente | Username | Password |
|-------------|----------|----------|
| Admin | `admin` | `admin123` |
| Utente Test 1 | `mario.rossi` | `password123` |
| Utente Test 2 | `giulia.bianchi` | `password123` |

## ✨ Caratteristiche

### 👥 Per gli Utenti
- ✅ **Registrazione e Login** con validazione email
- 🔍 **Ricerca Avanzata** con filtri per categoria, città e data
- 🛒 **Carrello Dinamico** per selezione multipla biglietti
- 📱 **QR Code** per ogni prenotazione
- 📊 **Dashboard Personale** con storico prenotazioni
- 💳 **Pagamento Simulato** con conferma ordine
- 📧 **Notifiche Email** (in sviluppo)

### 👨‍💼 Per gli Amministratori
- 📋 **Pannello Admin Completo** con statistiche
- 📈 **Gestione Eventi** con upload immagini
- 🎫 **Gestione Biglietti** con tipologie multiple
- 👥 **Gestione Utenti** con permessi
- 📊 **Report Vendite** in tempo reale
- 🔄 **Gestione Inventario** automatica

### 🔧 Tecniche
- 🚀 **API RESTful** con Django REST Framework
- 🔒 **Autenticazione JWT** (opzionale)
- 📱 **Design Responsive** con Bootstrap 5
- ⚡ **Performance Ottimizzate** con caching
- 🌐 **Internazionalizzazione** (i18n ready)
- 🔐 **CSRF Protection** su tutti i form

## 🛠️ Tecnologie

### Backend
- **Django 4.2.7** - Framework web Python
- **Django REST Framework** - API RESTful
- **SQLite** (development) / **PostgreSQL** (production)
- **Pillow** - Gestione immagini

### Frontend
- **Bootstrap 5.3** - Framework CSS
- **Font Awesome 6** - Icone
- **JavaScript ES6** - Interattività
- **AJAX** - Chiamate asincrone

### Tools
- **Git** - Version control
- **pip** - Package manager
- **virtualenv** - Ambiente virtuale

## 📋 Requisiti

### Sistema
- Python 3.8 o superiore
- pip (Python package manager)
- Git (opzionale)

### Dipendenze Python
```txt
Django==4.2.7
djangorestframework==3.14.0
Pillow==10.1.0
django-cors-headers==4.3.0
python-dotenv==1.0.0
```

## 🚀 Installazione

### 1️⃣ Clona il Repository
```bash
git clone https://github.com/tuousername/ticketbooking.git
cd ticketbooking
```

### 2️⃣ Crea l'Ambiente Virtuale
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Installa le Dipendenze
```bash
pip install -r requirements.txt
```

### 4️⃣ Configura il Database
```bash
python manage.py makemigrations accounts
python manage.py makemigrations events  
python manage.py makemigrations bookings
python manage.py migrate
```

### 5️⃣ Popola il Database
```bash
python manage.py populate_db
```

### 6️⃣ Crea le Directory per i Media
```bash
# Windows
mkdir media\events
mkdir static\images\events

# Linux/Mac
mkdir -p media/events
mkdir -p static/images/events
```

### 7️⃣ Raccogli i File Statici
```bash
python manage.py collectstatic --noinput
```

### 8️⃣ Avvia il Server
```bash
python manage.py runserver
```

Per la publicazione del sito, ho usato Railway version gratuita di 30 giorni.
il link publico del mio sito è : 'ticketbooking-martial.up.railway.app'

Visita: http://127.0.0.1:8000/

## ⚙️ Configurazione

### Variabili d'Ambiente
Crea un file `.env` nella root del progetto:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Email (Opzionale)
In `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 📖 Utilizzo

### Per Utenti

1. **Registrazione**
   - Clicca su "Registrati" nella navbar
   - Compila il form con i tuoi dati
   - Conferma la registrazione

2. **Ricerca Eventi**
   - Usa i filtri nella pagina eventi
   - Ordina per data o prezzo
   - Cerca per nome o città

3. **Prenotazione Biglietti**
   - Seleziona l'evento desiderato
   - Scegli il tipo e quantità di biglietti
   - Procedi al checkout
   - Conferma il pagamento

4. **Gestione Prenotazioni**
   - Accedi a "Le Mie Prenotazioni"
   - Visualizza i dettagli
   - Scarica il QR code
   - Cancella se necessario

### Per Amministratori

1. **Accesso Admin**
   ```
   URL: /admin/
   Username: admin
   Password: admin123
   ```

2. **Gestione Eventi**
   - Crea nuovi eventi
   - Modifica dettagli
   - Carica immagini
   - Imposta disponibilità

3. **Gestione Biglietti**
   - Definisci tipologie
   - Imposta prezzi
   - Gestisci quantità
   - Monitora vendite

## 📁 Struttura del Progetto

```
ticketbooking/
├── 📂 ticketbooking/          # Configurazioni Django
│   ├── 📄 settings.py         # Impostazioni progetto
│   ├── 📄 urls.py             # URL principali
│   ├── 📄 views.py            # Vista homepage
│   └── 📄 wsgi.py             # WSGI config
│
├── 📂 accounts/               # App gestione utenti
│   ├── 📄 models.py           # Modello CustomUser
│   ├── 📄 views.py            # Viste autenticazione
│   ├── 📄 forms.py            # Form registrazione
│   └── 📄 urls.py             # URL accounts
│
├── 📂 events/                 # App gestione eventi
│   ├── 📄 models.py           # Modelli Event, Ticket
│   ├── 📄 views.py            # Viste eventi
│   ├── 📄 serializers.py      # API serializers
│   └── 📄 api_views.py        # API views
│
├── 📂 bookings/               # App prenotazioni
│   ├── 📄 models.py           # Modelli Booking
│   ├── 📄 views.py            # Viste prenotazioni
│   └── 📄 forms.py            # Form prenotazione
│
├── 📂 templates/              # Template HTML
│   ├── 📄 base.html           # Template base
│   ├── 📄 home.html           # Homepage
│   └── 📂 events/             # Template eventi
│
├── 📂 static/                 # File statici
│   ├── 📂 css/                # Stili CSS
│   ├── 📂 js/                 # JavaScript
│   └── 📂 images/             # Immagini
│
└── 📂 media/                  # Upload utenti
```

## 🔌 API Documentation

### Endpoints Pubblici

#### Eventi
```http
GET /api/events/              # Lista eventi
GET /api/events/{id}/         # Dettaglio evento
GET /api/events/upcoming/     # Prossimi eventi
GET /api/events/featured/     # Eventi in evidenza
```

#### Filtri Disponibili
```
?category=concerti            # Filtra per categoria
?city=Milano                  # Filtra per città
?search=rock                  # Ricerca testuale
?ordering=date,-price         # Ordinamento
```

### Endpoints Autenticati

#### Prenotazioni
```http
GET    /api/bookings/         # Le mie prenotazioni
POST   /api/bookings/         # Nuova prenotazione
GET    /api/bookings/{id}/    # Dettaglio
PUT    /api/bookings/{id}/    # Modifica
DELETE /api/bookings/{id}/    # Cancella
```

#### Esempio Richiesta POST
```json
{
  "event_id": 1,
  "email": "user@example.com",
  "phone_number": "+39123456789",
  "items": [
    {
      "ticket_id": 1,
      "quantity": 2
    }
  ]
}
```

## 🧪 Testing

### Test Automatici
```bash
python manage.py test
```

### Test Manuali
1. **Registrazione**: Crea un nuovo account
2. **Login/Logout**: Verifica autenticazione
3. **Ricerca**: Testa filtri e ordinamento
4. **Prenotazione**: Completa un ordine
5. **Cancellazione**: Annulla una prenotazione

## 🚀 Deployment

### Preparazione
1. Imposta `DEBUG = False` in settings.py
2. Configura `ALLOWED_HOSTS`
3. Usa PostgreSQL per il database
4. Configura file statici con whitenoise

### Heroku
```bash
heroku create ticketbooking-app
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
heroku run python manage.py migrate
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "ticketbooking.wsgi"]
```

## 🤝 Contribuire

1. Fork del repository
2. Crea un branch (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

### Linee Guida
- Segui PEP 8 per il codice Python
- Scrivi test per nuove funzionalità
- Aggiorna la documentazione
- Usa commit messages descrittivi

## 🐛 Troubleshooting

### Errori Comuni

#### "No such table"
```bash
python manage.py migrate --run-syncdb
```

#### "Static files not found"
```bash
python manage.py collectstatic
```

#### "CSRF token missing"
Assicurati che `{% csrf_token %}` sia nei form

#### "Module not found"
```bash
pip install -r requirements.txt
```

### FAQ

**Q: Come cambio i colori del tema?**
A: Modifica le variabili CSS in `static/css/style.css`

**Q: Posso usare MySQL?**
A: Sì, installa `mysqlclient` e configura in settings.py

**Q: Come aggiungo nuove categorie?**
A: Dal pannello admin o con il comando `populate_db`

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

---

<div align="center">
  <p>Sviluppato con passione da TicketBooking Team</p>
  <p>
    <a href="#-ticketbooking---sistema-di-prenotazione-eventi">⬆️ Torna su</a>
  </p>
</div>