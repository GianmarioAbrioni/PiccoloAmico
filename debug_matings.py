from app import app, db
from models import Dog, Mating
import sys

# Funzione per stampare i dettagli di un cane
def print_dog_details(dog):
    print(f"ID: {dog.id}, Nome: {dog.name}, Genere: {dog.gender}")
    print(f"  In riproduzione: {dog.in_breeding}, Venduto: {dog.sold}")
    print("---")

# Test delle query con app context
with app.app_context():
    print("=== DEBUGGING ACCOPPIAMENTI ===")
    
    # Test 1: Query tutti i cani
    print("\nQuery 1: Tutti i cani")
    all_dogs = Dog.query.all()
    print(f"Trovati {len(all_dogs)} cani totali:")
    for dog in all_dogs:
        print_dog_details(dog)
    
    # Test 2: Query femmine
    print("\nQuery 2: Solo femmine")
    females = Dog.query.filter_by(gender='Female').all()
    print(f"Trovati {len(females)} cani femmine:")
    for dog in females:
        print_dog_details(dog)
    
    # Test 3: Query maschi
    print("\nQuery 3: Solo maschi")
    males = Dog.query.filter_by(gender='Male').all()
    print(f"Trovati {len(males)} cani maschi:")
    for dog in males:
        print_dog_details(dog)
    
    # Test 4: Query con filtri per accoppiamento
    print("\nQuery 4: Femmine disponibili per accoppiamento (in_breeding=True, sold=False)")
    breeding_females = Dog.query.filter_by(gender='Female', in_breeding=True, sold=False).all()
    print(f"Trovati {len(breeding_females)} femmine per accoppiamento:")
    for dog in breeding_females:
        print_dog_details(dog)
    
    # Test 5: Query con filtri per accoppiamento
    print("\nQuery 5: Maschi disponibili per accoppiamento (in_breeding=True, sold=False)")
    breeding_males = Dog.query.filter_by(gender='Male', in_breeding=True, sold=False).all()
    print(f"Trovati {len(breeding_males)} maschi per accoppiamento:")
    for dog in breeding_males:
        print_dog_details(dog)