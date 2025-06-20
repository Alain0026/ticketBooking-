# TicketBooking - Sistema di Prenotazione Biglietti per Eventi

## 📋 Descrizione del Progetto

TicketBooking è una piattaforma web completa per la prenotazione di biglietti per eventi, sviluppata con Django e Django REST Framework. Il sistema offre un'interfaccia moderna e intuitiva per la gestione di eventi, biglietti e prenotazioni.

## 🚀 Caratteristiche Principali

### Per gli Utenti
- **Registrazione e Autenticazione**: Sistema completo di registrazione e login
- **Ricerca Eventi**: Filtri per categoria, città, disponibilità e ordinamento
- **Prenotazione Biglietti**: Processo guidato in 3 passaggi
- **Gestione Prenotazioni**: Dashboard personale per visualizzare e gestire le prenotazioni
- **Biglietti Digitali**: QR Code per ogni prenotazione

### Per gli Amministratori
- **Pannello Admin Personalizzato**: Interfaccia completa per la gestione
- **Gestione Eventi**: Creazione e modifica di eventi con categorie
- **Gestione Biglietti**: Tipologie multiple di biglietti per evento
- **Monitoraggio Vendite**: Statistiche in tempo reale
- **Gestione Utenti**: Controllo completo degli utenti registrati

### API REST
- **Eventi**: GET /api/events/ (lista, dettagli, ricerca)
- **Biglietti**: GET /api/tickets/
- **Prenotazioni**: CRUD completo con autenticazione

## 🛠 Installazione e Configurazione

### 1. Clonare il Repository
```bash
# Crea la directory del progetto
mkdir ticketbooking
cd ticketbooking

# Inizializza git (opzionale)
git init
```

### 2. Creare l'Ambiente Virtuale
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Installare le Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configurazione del Database
```bash
# Crea le migrazioni per i modelli personalizzati
python manage.py makemigrations accounts
python manage.py makemigrations events
python manage.py makemigrations bookings

# Applica le migrazioni
python manage.py migrate
```

### 5. Popolare il Database con Dati di Esempio
```bash
python manage.py populate_db
```

Questo comando creerà:
- 5 categorie di eventi
- 10 eventi di esempio con immagini
- Biglietti per ogni evento
- Utenti di test:
  - **Admin**: username: `admin`, password: `admin123`
  - **User 1**: username: `mario.rossi`, password: `password123`
  - **User 2**: username: `giulia.bianchi`, password: `password123`

### 6. Creare le Directory per Media e Static
```bash
# Windows
mkdir media\events
mkdir static\images\events

# Linux/Mac
mkdir -p media/events
mkdir -p static/images/events
```

### 7. Raccogliere i File Statici
```bash
python manage.py collectstatic --noinput
```

### 8. Avviare il Server di Sviluppo
```bash
python manage.py runserver
```

Il sito sarà disponibile su: http://127.0.0.1:8000/

## 📁 Struttura del Progetto

```
ticketbooking/
├── manage.py                 # Script principale Django
├── requirements.txt          # Dipendenze Python
├── .gitignore               # File da ignorare in git
│
├── ticketbooking/           # Configurazioni principali
│   ├── __init__.py
│   ├── settings.py          # Configurazioni Django
│   ├── urls.py              # URL principali
│   ├── wsgi.py              # Entry point WSGI
│   └── asgi.py              # Entry point ASGI
│
├── accounts/                # App gestione utenti
│   ├── __init__.py
│   ├── apps.py              # Configurazione app
│   ├── models.py            # Modello CustomUser
│   ├── views.py             # Viste registrazione/profilo
│   ├── forms.py             # Form personalizzati
│   ├── urls.py              # URL accounts
│   ├── admin.py             # Admin utenti
│   └── migrations/
│       └── __init__.py
│
├── events/                  # App gestione eventi
│   ├── __init__.py
│   ├── apps.py              # Configurazione app
│   ├── models.py            # Modelli Event, Ticket
│   ├── views.py             # Viste lista/dettaglio eventi
│   ├── forms.py             # Form eventi
│   ├── serializers.py       # API serializers
│   ├── api_views.py         # API views
│   ├── urls.py              # URL eventi
│   ├── api_urls.py          # URL API eventi
│   ├── admin.py             # Admin eventi
│   ├── migrations/
│   │   └── __init__.py
│   └── management/
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── populate_db.py  # Comando per popolare DB
│
├── bookings/                # App gestione prenotazioni
│   ├── __init__.py
│   ├── apps.py              # Configurazione app
│   ├── models.py            # Modelli Booking, BookingItem
│   ├── views.py             # Viste prenotazioni
│   ├── forms.py             # Form prenotazioni
│   ├── serializers.py       # API serializers
│   ├── api_views.py         # API views
│   ├── urls.py              # URL prenotazioni
│   ├── api_urls.py          # URL API prenotazioni
│   ├── admin.py             # Admin prenotazioni
│   └── migrations/
│       └── __init__.py
│
├── templates/               # Template HTML
│   ├── base.html            # Template base
│   ├── home.html            # Homepage
│   ├── includes/
│   │   └── header.html      # Navbar include
│   ├── registration/
│   │   ├── login.html       # Login
│   │   └── signup.html      # Registrazione
│   ├── accounts/
│   │   ├── profile.html     # Profilo utente
│   │   └── edit_profile.html # Modifica profilo
│   ├── events/
│   │   ├── event_list.html  # Lista eventi
│   │   └── event_detail.html # Dettaglio evento
│   └── bookings/
│       ├── booking_form.html    # Form prenotazione
│       ├── booking_confirm.html # Conferma prenotazione
│       ├── booking_success.html # Successo prenotazione
│       ├── booking_detail.html  # Dettaglio prenotazione
│       ├── cancel_booking.html  # Cancella prenotazione
│       └── my_bookings.html     # Le mie prenotazioni
│
├── static/                  # File statici
│   ├── css/
│   │   ├── style.css        # Stili principali
│   │   └── responsive.css   # Stili responsive
│   ├── js/
│   │   ├── main.js          # JavaScript principale
│   │   └── booking.js       # JavaScript prenotazioni
│   └── images/
│       ├── logo.png
│       ├── hero-illustration.svg
│       ├── event-placeholder.jpg
│       └── events/          # Immagini eventi
│           ├── event1.jpg
│           ├── event2.jpg
│           └── ...
│
└── media/                   # File caricati
    └── events/              # Immagini eventi caricate
```

## 🎨 Design e Interfaccia

### Tecnologie Frontend
- **Bootstrap 5.3**: Framework CSS responsive
- **Font Awesome 6**: Icone moderne
- **Google Fonts**: Typography (Poppins)
- **CSS Personalizzato**: Animazioni e stili custom

### Caratteristiche UI/UX
- **Design Moderno**: Interfaccia pulita con gradienti e ombre
- **Animazioni**: Transizioni fluide e effetti hover
- **Responsive**: Ottimizzato per tutti i dispositivi
- **Dark Mode Ready**: Supporto per temi scuri
- **Accessibilità**: ARIA labels e navigazione da tastiera

## 🔒 Sicurezza

- **CSRF Protection**: Attiva su tutti i form
- **Autenticazione**: Sistema Django built-in
- **Validazione**: Lato client e server
- **Sanitizzazione**: Input utente validato
- **HTTPS Ready**: Configurabile per produzione

## 📊 Modelli di Dati

### CustomUser
- Estende AbstractUser di Django
- Campi aggiuntivi: telefono, data nascita, indirizzo

### Event
- Informazioni evento: titolo, data, luogo
- Relazioni: categoria, biglietti
- Proprietà calcolate: sold_out, disponibilità

### Ticket
- Tipologie: standard, VIP, studente
- Gestione quantità e prezzi
- Limite per ordine

### Booking
- Codice univoco generato
- Stati: pending, confirmed, cancelled
- Relazioni: utente, evento, biglietti

## 🚦 API Endpoints

### Eventi
```
GET /api/events/              # Lista eventi
GET /api/events/{id}/         # Dettaglio evento
GET /api/events/upcoming/     # Prossimi eventi
GET /api/events/featured/     # Eventi in evidenza
```

### Prenotazioni (Autenticazione richiesta)
```
GET    /api/bookings/         # Le mie prenotazioni
POST   /api/bookings/         # Nuova prenotazione
GET    /api/bookings/{id}/    # Dettaglio prenotazione
POST   /api/bookings/{id}/confirm/  # Conferma
POST   /api/bookings/{id}/cancel/   # Cancella
```

## 🧪 Test del Sistema

### 1. Test Registrazione
- Vai su `/accounts/signup/`
- Compila il form con dati validi
- Verifica email e login automatico

### 2. Test Prenotazione
- Login con utente test
- Cerca un evento disponibile
- Seleziona biglietti e procedi
- Conferma ordine

### 3. Test Admin
- Accedi a `/admin/` con credenziali admin
- Crea nuovo evento
- Aggiungi biglietti
- Monitora prenotazioni

## 🐛 Troubleshooting

### Errore: "No such table"
```bash
python manage.py migrate --run-syncdb
```

### Errore: "Static files not found"
```bash
python manage.py collectstatic
```

### Errore: "CSRF token missing"
- Assicurati che `{% csrf_token %}` sia nei form
- Verifica MIDDLEWARE in settings.py

## 📈 Possibili Estensioni

1. **Sistema di Pagamento Reale**
   - Integrazione Stripe/PayPal
   - Gestione rimborsi

2. **Notifiche Email**
   - Conferma prenotazione
   - Promemoria eventi

3. **Sistema di Review**
   - Recensioni eventi passati
   - Rating e commenti

4. **App Mobile**
   - React Native
   - Flutter

5. **Analytics Dashboard**
   - Grafici vendite
   - Report dettagliati

## 📝 Note per lo Sviluppo

- **Debug Mode**: Attivo in sviluppo (settings.py)
- **Database**: SQLite per sviluppo, PostgreSQL per produzione
- **Media Files**: Configurare storage cloud per produzione
- **Cache**: Implementare Redis per performance

## 🤝 Contribuire

1. Fork del progetto
2. Crea branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri Pull Request

## 📄 Licenza

Questo progetto è sviluppato per scopi didattici e dimostrativi.

---

**Sviluppato con passione e amore usando Django 4.2.7**