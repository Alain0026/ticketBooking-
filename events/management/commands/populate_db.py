from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from events.models import Event, EventCategory, Ticket
from datetime import timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Popola il database con eventi di esempio'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creazione dati di esempio...')
        
        # Crea categorie
        categories = [
            {'name': 'Concerti', 'slug': 'concerti'},
            {'name': 'Teatro', 'slug': 'teatro'},
            {'name': 'Sport', 'slug': 'sport'},
            {'name': 'Conferenze', 'slug': 'conferenze'},
            {'name': 'Festival', 'slug': 'festival'},
        ]
        
        category_objects = []
        for cat_data in categories:
            category, created = EventCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            category_objects.append(category)
            if created:
                self.stdout.write(f'Categoria creata: {category.name}')
        
        # Crea eventi di esempio
        events_data = [
            {
                'title': 'Concerto Rock Estate 2024',
                'description': 'Un incredibile concerto rock con le migliori band italiane e internazionali. Una serata indimenticabile di musica ed energia.',
                'category': 'concerti',
                'venue': 'Arena di Verona',
                'city': 'Verona',
                'address': 'Piazza Bra, 1',
                'max_capacity': 15000,
                'days_from_now': 30,
            },
            {
                'title': 'La Traviata di Giuseppe Verdi',
                'description': 'La celebre opera di Verdi in una produzione esclusiva del Teatro alla Scala. Con i migliori interpreti internazionali.',
                'category': 'teatro',
                'venue': 'Teatro alla Scala',
                'city': 'Milano',
                'address': 'Via Filodrammatici, 2',
                'max_capacity': 2000,
                'days_from_now': 45,
            },
            {
                'title': 'Finale Champions League',
                'description': 'La finale più attesa dell\'anno! Due squadre si contenderanno il trofeo più prestigioso del calcio europeo.',
                'category': 'sport',
                'venue': 'Stadio San Siro',
                'city': 'Milano',
                'address': 'Piazzale Angelo Moratti',
                'max_capacity': 80000,
                'days_from_now': 60,
            },
            {
                'title': 'TEDx Milano - Il Futuro è Adesso',
                'description': 'Una giornata di ispirazione con speaker internazionali che condivideranno idee innovative per il futuro.',
                'category': 'conferenze',
                'venue': 'MiCo Milano',
                'city': 'Milano',
                'address': 'Piazzale Carlo Magno, 1',
                'max_capacity': 1500,
                'days_from_now': 20,
            },
            {
                'title': 'Festival del Cinema di Venezia',
                'description': 'Il prestigioso festival cinematografico con anteprime mondiali, star internazionali e i migliori film dell\'anno.',
                'category': 'festival',
                'venue': 'Palazzo del Cinema',
                'city': 'Venezia',
                'address': 'Lungomare Marconi, 94',
                'max_capacity': 1000,
                'days_from_now': 90,
            },
            {
                'title': 'Concerto Sinfonico di Natale',
                'description': 'L\'Orchestra Filarmonica della Scala presenta un magico concerto con i classici natalizi e le più belle melodie.',
                'category': 'concerti',
                'venue': 'Auditorium di Milano',
                'city': 'Milano',
                'address': 'Largo Mahler',
                'max_capacity': 1400,
                'days_from_now': 15,
            },
            {
                'title': 'Maratona di Roma',
                'description': 'La maratona più emozionante d\'Italia attraverso i monumenti storici della Città Eterna.',
                'category': 'sport',
                'venue': 'Colosseo',
                'city': 'Roma',
                'address': 'Piazza del Colosseo',
                'max_capacity': 25000,
                'days_from_now': 75,
            },
            {
                'title': 'Festival Jazz Umbria',
                'description': 'Tre giorni di jazz con artisti internazionali nelle piazze storiche dell\'Umbria.',
                'category': 'festival',
                'venue': 'Piazza IV Novembre',
                'city': 'Perugia',
                'address': 'Piazza IV Novembre',
                'max_capacity': 5000,
                'days_from_now': 50,
            },
            {
                'title': 'Amleto di Shakespeare',
                'description': 'Il capolavoro shakespeariano in una nuova produzione contemporanea con effetti speciali innovativi.',
                'category': 'teatro',
                'venue': 'Teatro Romano',
                'city': 'Verona',
                'address': 'Regaste Redentore, 2',
                'max_capacity': 800,
                'days_from_now': 35,
            },
            {
                'title': 'Blockchain & AI Summit',
                'description': 'Conferenza internazionale sulle ultime innovazioni in blockchain e intelligenza artificiale.',
                'category': 'conferenze',
                'venue': 'Fiera di Roma',
                'city': 'Roma',
                'address': 'Via Portuense, 1645',
                'max_capacity': 3000,
                'days_from_now': 40,
            },
        ]
        
        # Crea eventi
        for i, event_data in enumerate(events_data, 1):
            category = next(c for c in category_objects if c.slug == event_data['category'])
            
            event, created = Event.objects.get_or_create(
                slug=slugify(event_data['title']),
                defaults={
                    'title': event_data['title'],
                    'description': event_data['description'],
                    'category': category,
                    'date': timezone.now() + timedelta(days=event_data['days_from_now']),
                    'venue': event_data['venue'],
                    'city': event_data['city'],
                    'address': event_data['address'],
                    'max_capacity': event_data['max_capacity'],
                    # Non impostiamo l'immagine qui, verrà gestita da Cloudinary
                }
            )
            
            if created:
                self.stdout.write(f'Evento creato: {event.title}')
                
                # Crea biglietti per ogni evento
                ticket_types = [
                    {
                        'name': 'Standard',
                        'ticket_type': 'standard',
                        'description': 'Biglietto standard con accesso all\'evento',
                        'price_range': (30, 80),
                        'quantity_range': (100, 500),
                    },
                    {
                        'name': 'VIP',
                        'ticket_type': 'vip',
                        'description': 'Accesso VIP con posti premium e servizi esclusivi',
                        'price_range': (100, 300),
                        'quantity_range': (20, 100),
                    },
                    {
                        'name': 'Studente',
                        'ticket_type': 'student',
                        'description': 'Prezzo ridotto per studenti con tessera universitaria',
                        'price_range': (15, 40),
                        'quantity_range': (50, 200),
                    },
                ]
                
                # Seleziona casualmente 2-3 tipi di biglietti per evento
                selected_tickets = random.sample(ticket_types, random.randint(2, 3))
                
                for ticket_data in selected_tickets:
                    price = random.randint(*ticket_data['price_range'])
                    quantity = random.randint(*ticket_data['quantity_range'])
                    sold = random.randint(0, int(quantity * 0.7))  # Venduto fino al 70%
                    
                    Ticket.objects.create(
                        event=event,
                        name=ticket_data['name'],
                        ticket_type=ticket_data['ticket_type'],
                        description=ticket_data['description'],
                        price=price,
                        quantity=quantity,
                        sold_quantity=sold,
                        max_per_order=10,
                    )
        
        # Crea utente admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ticketbooking.com',
                password='admin123',
                first_name='Admin',
                last_name='Sistema'
            )
            self.stdout.write('Utente admin creato (username: admin, password: admin123)')
        
        # Crea utenti di test
        test_users = [
            {
                'username': 'mario.rossi',
                'email': 'mario.rossi@example.com',
                'first_name': 'Mario',
                'last_name': 'Rossi',
                'password': 'password123'
            },
            {
                'username': 'giulia.bianchi',
                'email': 'giulia.bianchi@example.com',
                'first_name': 'Giulia',
                'last_name': 'Bianchi',
                'password': 'password123'
            },
        ]
        
        for user_data in test_users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    password=user_data['password']
                )
                self.stdout.write(f'Utente test creato: {user_data["username"]}')
        
        self.stdout.write(self.style.SUCCESS('Database popolato con successo!'))