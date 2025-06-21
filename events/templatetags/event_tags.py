from django import template
import hashlib

register = template.Library()

@register.filter
def event_image_url(event):
    """
    Restituisce l'URL dell'immagine dell'evento o un placeholder
    """
    if event.image and hasattr(event.image, 'url'):
        try:
            return event.image.url
        except:
            pass
    
    # Mappa immagini predefinite per titolo evento
    image_map = {
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
    
    # Se l'evento è nella mappa, usa l'immagine specifica
    if event.title in image_map:
        return image_map[event.title]
    
    # Altrimenti usa un'immagine casuale basata sul titolo
    # Genera un hash dal titolo per avere sempre la stessa immagine per lo stesso evento
    hash_object = hashlib.md5(event.title.encode())
    hex_dig = hash_object.hexdigest()
    seed = int(hex_dig[:8], 16) % 1000
    
    # Lista di immagini di fallback
    fallback_images = [
        f'https://picsum.photos/800/600?random={seed}',
        f'https://source.unsplash.com/800x600/?event,{event.category.slug if event.category else "concert"}',
        'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800&h=600&fit=crop'
    ]
    
    return fallback_images[0]