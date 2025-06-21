from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from events.models import Event
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Carica immagini da URL per gli eventi'

    def handle(self, *args, **kwargs):
        self.stdout.write('Caricamento immagini eventi da URL...')
        
        # URL delle immagini da Unsplash (gratis e di alta qualità)
        image_urls = [
            # Concerto Rock
            ('Concerto Rock Estate 2024', 'https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=800&h=600&fit=crop'),
            # La Traviata
            ('La Traviata di Giuseppe Verdi', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop'),
            # Champions League
            ('Finale Champions League', 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800&h=600&fit=crop'),
            # TEDx
            ('TEDx Milano - Il Futuro è Adesso', 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&h=600&fit=crop'),
            # Festival Cinema
            ('Festival del Cinema di Venezia', 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&h=600&fit=crop'),
            # Concerto Sinfonico
            ('Concerto Sinfonico di Natale', 'https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=800&h=600&fit=crop'),
            # Maratona
            ('Maratona di Roma', 'https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=800&h=600&fit=crop'),
            # Festival Jazz
            ('Festival Jazz Umbria', 'https://images.unsplash.com/photo-1511192336575-5a79af67a629?w=800&h=600&fit=crop'),
            # Amleto
            ('Amleto di Shakespeare', 'https://images.unsplash.com/photo-1503095396549-807759245b35?w=800&h=600&fit=crop'),
            # Blockchain Summit
            ('Blockchain & AI Summit', 'https://images.unsplash.com/photo-1582192730841-2a682d7375f9?w=800&h=600&fit=crop'),
        ]
        
        for event_title, image_url in image_urls:
            try:
                event = Event.objects.get(title=event_title)
                
                if not event.image or 'placeholder' in str(event.image):
                    self.stdout.write(f'Caricamento immagine per: {event_title}')
                    
                    # Scarica l'immagine
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        # Crea un file da caricare
                        image_name = f"{event.slug}.jpg"
                        event.image.save(
                            image_name,
                            ContentFile(response.content),
                            save=True
                        )
                        self.stdout.write(self.style.SUCCESS(f'✓ Immagine caricata per {event_title}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'✗ Impossibile scaricare immagine per {event_title}'))
                else:
                    self.stdout.write(f'- {event_title} ha già un\'immagine')
                    
            except Event.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'✗ Evento non trovato: {event_title}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Errore per {event_title}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\nCaricamento immagini completato!'))