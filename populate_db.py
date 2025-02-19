import os
import django
import random
from faker import Faker
from events.models import Event, Category, Participant

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

# Initialize Faker
fake = Faker()

def clear_database():
    """Delete existing data before populating new data."""
    Participant.objects.all().delete()
    Event.objects.all().delete()
    Category.objects.all().delete()
    print("Database cleared successfully!")

def create_categories(count=5):
    """Create fake event categories."""
    categories = [Category.objects.create(
        name=fake.word().capitalize(),
        description=fake.sentence()
    ) for _ in range(count)]
    print(f"Created {len(categories)} categories.")
    return categories

def create_events(categories, count=10):
    """Create fake events and assign them to categories."""
    events = [Event.objects.create(
        name=fake.sentence(nb_words=3),
        description=fake.paragraph(),
        date=fake.date_this_year(),
        time=fake.time(),
        location=fake.city(),
        category=random.choice(categories)
    ) for _ in range(count)]
    print(f"Created {len(events)} events.")
    return events

def create_participants(events, count=20):
    """Create fake participants and assign them to events."""
    participants = []
    for _ in range(count):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.email()
        )
        assigned_events = random.sample(events, random.randint(1, 3))  # Assign participant to 1-3 events
        participant.events.set(assigned_events)
        participants.append(participant)
    print(f"Created {len(participants)} participants.")
    return participants

def populate_database():
    """Main function to populate the database."""
    clear_database()  # Optional: Remove existing data before populating new data

    categories = create_categories()
    events = create_events(categories)
    create_participants(events)

    print("\nDatabase populated successfully!")

if __name__ == "__main__":
    populate_database()
