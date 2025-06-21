# 🚀 Guida Deployment su Railway

## 1. Preparazione Cloudinary (Storage Immagini)

### Crea un account Cloudinary:
1. Vai su https://cloudinary.com/users/register/free
2. Registrati gratuitamente
3. Vai nella Dashboard e copia:
   - **Cloud Name**
   - **API Key**
   - **API Secret**

## 2. Preparazione del Repository

### Aggiungi questi file al tuo repository GitHub:
```bash
git add railway.json
git add requirements.txt
git add ticketbooking/settings_production.py
git add DEPLOYMENT_RAILWAY.md
git commit -m "Add Railway deployment configuration"
git push origin main
```

## 3. Deploy su Railway

### Passo 1: Crea un nuovo progetto
1. Vai su https://railway.app/dashboard
2. Clicca "New Project"
3. Seleziona "Deploy from GitHub repo"
4. Cerca e seleziona il tuo repository `ticketbooking`

### Passo 2: Configura le variabili d'ambiente
Nel pannello Railway, vai su "Variables" e aggiungi:

```env
# Django Settings
SECRET_KEY=genera-una-chiave-sicura-qui
DJANGO_SETTINGS_MODULE=ticketbooking.settings_production

# Cloudinary (usa i tuoi dati)
CLOUDINARY_CLOUD_NAME=il-tuo-cloud-name
CLOUDINARY_API_KEY=la-tua-api-key
CLOUDINARY_API_SECRET=il-tuo-api-secret

# Railway
RAILWAY_ENVIRONMENT=production
```

### Passo 3: Genera una SECRET_KEY sicura
Puoi generarla con Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Passo 4: Deploy
1. Railway inizierà automaticamente il deploy
2. Attendi che il processo sia completato (circa 3-5 minuti)
3. Clicca su "View Logs" per monitorare il progresso

## 4. Post-Deployment

### Verifica il deployment:
1. Clicca sul dominio generato (es: `tuoapp.up.railway.app`)
2. Dovresti vedere la homepage di TicketBooking
3. Gli eventi dovrebbero essere già caricati dal comando `populate_db`

### Accedi al pannello admin:
```
URL: https://tuoapp.up.railway.app/admin/
Username: admin
Password: admin123
```

⚠️ **IMPORTANTE**: Cambia subito la password admin!

### Test caricamento immagini:
1. Vai nel pannello admin
2. Modifica un evento
3. Carica un'immagine
4. Verifica che appaia correttamente (sarà salvata su Cloudinary)

## 5. Database SQLite su Railway

### Note importanti:
- Il database SQLite viene salvato in `/app/db.sqlite3`
- Railway mantiene i file durante i redeploy normali
- **ATTENZIONE**: Il database potrebbe essere resettato durante major updates

### Backup consigliato:
```bash
# Scarica il database localmente periodicamente
railway run python manage.py dumpdata > backup.json
```

## 6. Troubleshooting

### Errore "No such table":
Il comando migrate dovrebbe essere eseguito automaticamente. Se hai problemi:
```bash
railway run python manage.py migrate
railway run python manage.py populate_db
```

### Immagini non si caricano:
- Verifica le credenziali Cloudinary nelle variabili d'ambiente
- Controlla i logs per errori

### Errore 500:
- Controlla i logs in Railway
- Verifica che tutte le variabili d'ambiente siano configurate
- Assicurati che `DEBUG=False` in produzione

## 7. Comandi Utili Railway CLI

```bash
# Installa Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link al progetto
railway link

# Esegui comandi Django
railway run python manage.py createsuperuser
railway run python manage.py migrate
railway run python manage.py collectstatic

# Vedi i logs
railway logs
```

## 8. Costi

### Piano Free di Railway include:
- $5 di crediti al mese
- 500 ore di esecuzione
- 100GB di banda
- Perfetto per progetti demo/sviluppo

### Piano Free di Cloudinary include:
- 25 crediti mensili
- ~25GB di storage
- ~25GB di banda
- Più che sufficiente per questo progetto

## ✅ Il tuo sito è ora LIVE!

Condividi il link del tuo sito deployato! 🎉


# 🖼️ Come Risolvere il Problema delle Immagini su Railway

## Il Problema
Le immagini statiche locali (`static/images/events/`) non funzionano su Railway perché:
1. Railway non persiste i file statici tra i deploy
2. Le immagini devono essere caricate su Cloudinary

## Soluzione 1: Automatica (Consigliata)

### 1. Aggiorna il tuo repository con i file modificati:
```bash
git add .
git commit -m "Fix event images loading from URLs"
git push origin main
```

### 2. Railway farà automaticamente:
- Creare gli eventi
- Caricare le immagini da URL pubblici
- Salvare su Cloudinary

## Soluzione 2: Manuale (Se l'automatica non funziona)

### 1. Installa Railway CLI:
```bash
npm install -g @railway/cli
railway login
railway link
```

### 2. Esegui il comando manualmente:
```bash
railway run python manage.py load_images
```

## Soluzione 3: Carica manualmente dal pannello admin

### 1. Accedi al pannello admin:
```
https://tuoapp.up.railway.app/admin/
```

### 2. Per ogni evento:
1. Clicca su "Eventi"
2. Seleziona un evento
3. Nella sezione "Immagine", clicca "Scegli file"
4. Carica un'immagine dal tuo computer
5. Salva

L'immagine verrà automaticamente caricata su Cloudinary!

## Verifica

Dopo aver applicato una delle soluzioni:
1. Vai sulla homepage
2. Gli eventi dovrebbero mostrare immagini diverse
3. Le immagini sono salvate su Cloudinary (non nel repository)

## Note Importanti

- **NON** mettere immagini nella cartella `static/images/events/` per produzione
- Usa sempre URL pubblici o caricamento diretto
- Le immagini su Cloudinary sono permanenti
- Il piano gratuito di Cloudinary è più che sufficiente

## Debug

Se ancora non funziona, controlla:
```bash
railway logs
```

Cerca errori relativi a:
- Cloudinary configuration
- Image upload errors
- Permission denied