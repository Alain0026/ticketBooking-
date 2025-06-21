from django.core.management.base import BaseCommand
from events.models import Event

class Command(BaseCommand):
    help = 'Imposta URL di immagini direttamente nel database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Impostazione URL immagini per gli eventi...\n')
        
        # Mappa eventi -> URL immagini
        image_mapping = {
            'Concerto Rock Estate 2024': 'https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?w=800&h=600&fit=crop',
            'La Traviata di Giuseppe Verdi': 'https://images.unsplash.com/photo-1514320291840-2e0a9bf2a9ae?w=800&h=600&fit=crop',
            'Finale Champions League': 'https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=800&h=600&fit=crop',
            'TEDx Milano - Il Futuro è Adesso': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&h=600&fit=crop',
            'Festival del Cinema di Venezia': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&h=600&fit=crop',
            'Concerto Sinfonico di Natale': 'https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=800&h=600&fit=crop',
            'Maratona di Roma': 'https://images.unsplash.com/photo-1452626038306-9aae5e071dd3?w=800&h=600&fit=crop',
            'Festival Jazz Umbria': 'https://images.unsplash.com/photo-1511192336575-5a79af67a629?w=800&h=600&fit=crop',
            'Amleto di Shakespeare': 'https://images.unsplash.com/photo-1503095396549-807759245b35?w=800&h=600&fit=crop',
            'Blockchain & AI Summit': 'https://images.unsplash.com/photo-1582192730841-2a682d7375f9?w=800&h=600&fit=crop',
        }
        
        updated = 0
        for title, image_url in image_mapping.items():
            try:
                event = Event.objects.get(title=title)
                # Salva direttamente l'URL nel campo image
                event.image = image_url
                event.save()
                self.stdout.write(f'✅ {title} - Immagine aggiornata')
                updated += 1
            except Event.DoesNotExist:
                self.stdout.write(f'⚠️  {title} - Evento non trovato')
            except Exception as e:
                self.stdout.write(f'❌ {title} - Errore: {str(e)}')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Completato! {updated} eventi aggiornati.'))