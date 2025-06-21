from django.core.management.base import BaseCommand
import cloudinary
import os

class Command(BaseCommand):
    help = 'Testa la configurazione di Cloudinary'

    def handle(self, *args, **kwargs):
        self.stdout.write('\n=== TEST CONFIGURAZIONE CLOUDINARY ===\n')
        
        # Controlla variabili d'ambiente
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', 'NON IMPOSTATO')
        api_key = os.environ.get('CLOUDINARY_API_KEY', 'NON IMPOSTATO')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET', 'NON IMPOSTATO')
        
        self.stdout.write(f'CLOUD_NAME: {cloud_name}')
        self.stdout.write(f'API_KEY: {"*" * len(api_key) if api_key != "NON IMPOSTATO" else "NON IMPOSTATO"}')
        self.stdout.write(f'API_SECRET: {"*" * len(api_secret) if api_secret != "NON IMPOSTATO" else "NON IMPOSTATO"}')
        
        if cloud_name == 'NON IMPOSTATO' or api_key == 'NON IMPOSTATO' or api_secret == 'NON IMPOSTATO':
            self.stdout.write(self.style.ERROR('\n❌ ERRORE: Variabili Cloudinary non configurate!'))
            self.stdout.write('Assicurati di aver impostato su Railway:')
            self.stdout.write('- CLOUDINARY_CLOUD_NAME')
            self.stdout.write('- CLOUDINARY_API_KEY')
            self.stdout.write('- CLOUDINARY_API_SECRET')
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ Variabili Cloudinary configurate correttamente!'))
            
            # Test upload
            try:
                import cloudinary.uploader
                result = cloudinary.uploader.upload(
                    "https://via.placeholder.com/150",
                    folder="test",
                    public_id="test_image"
                )
                self.stdout.write(self.style.SUCCESS('✅ Test upload riuscito!'))
                self.stdout.write(f'URL immagine: {result.get("secure_url")}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Errore upload: {str(e)}'))