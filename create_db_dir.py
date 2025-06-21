"""
Script per creare la directory del database su Railway
"""
import os

# Crea la directory /app se non esiste (per Railway)
if not os.path.exists('/app'):
    try:
        os.makedirs('/app')
        print("Directory /app creata con successo")
    except Exception as e:
        print(f"Errore nella creazione della directory: {e}")
else:
    print("Directory /app già esistente")