import os
import sys
import pandas as pd
from datetime import datetime
from io import StringIO

# -- Path Setup --
# This is a bit of a hack to make the script runnable from the root directory.
# It ensures that the 'app' module can be found.
# In a more robust setup, you might make this a proper CLI command with Flask-Script or Click.
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# -- End Path Setup --

from app import create_app
from app.models import db, Entity, Identifier, Event

# --- Synthetic CSV Data ---
# In a real-world scenario, you would read these from actual files:
# e.g., students_df = pd.read_csv('data/students.csv')

students_csv = """student_id,name,email,card_id
S001,Alice Johnson,alice.j@university.edu,C1001
S002,Bob Williams,bob.w@university.edu,C1002
S003,Charlie Brown,charlie.b@university.edu,C1003
"""

staff_csv = """staff_id,name,email,card_id,department
T201,Diana Prince,diana.p@university.edu,C2001,History
T202,Edward Nygma,edward.n@university.edu,C2002,Computer Science
"""

swipes_csv = """card_id,timestamp,location_name
C1001,2023-10-26 08:05:00,Main Library Entrance
C1002,2023-10-26 08:15:00,Science Building Wing A
C2001,2023-10-26 08:30:00,Staff Lounge
C1001,2023-10-26 12:30:00,Cafeteria
C1003,2023-10-26 13:00:00,Gymnasium
"""

wifi_csv = """device_hash,user_email,ap_location,timestamp
hash_alice_laptop,alice.j@university.edu,Library_Wifi_AP1,2023-10-26 09:00:00
hash_bob_phone,bob.w@university.edu,Science_Bldg_AP3,2023-10-26 09:10:00
hash_diana_tablet,diana.p@university.edu,History_Dept_AP2,2023-10-26 09:30:00
hash_alice_phone,alice.j@university.edu,Cafeteria_AP5,2023-10-26 12:32:00
"""

library_csv = """student_id,book_title,checkout_timestamp,location
S001,The Great Gatsby,2023-10-26 10:15:00,Main Library
S003,Data Structures in Python,2023-10-26 11:45:00,Science Library
"""

def seed_database():
    """
    Reads synthetic data, performs entity resolution, and populates the database.
    """
    app = create_app()
    with app.app_context():
        print("Dropping all data from the database...")
        db.drop_all()
        print("Creating database tables...")
        db.create_all()
        print("Database tables created.")

        # --- Load data into pandas DataFrames ---
        students_df = pd.read_csv(StringIO(students_csv))
        staff_df = pd.read_csv(StringIO(staff_csv))
        swipes_df = pd.read_csv(StringIO(swipes_csv))
        wifi_df = pd.read_csv(StringIO(wifi_csv))
        library_df = pd.read_csv(StringIO(library_csv))

        # --- Entity Resolution Mappings ---
        # These dictionaries will help us quickly find an entity's primary key
        # from a secondary identifier (like an email or card_id).
        identifier_to_entity_map = {}

        # --- 1. Process Entities (Students and Staff) ---
        print("Processing students and staff to create entities...")

        # Process Students
        for _, row in students_df.iterrows():
            entity = Entity(
                name=row['name'],
                entity_type='student',
                primary_email=row['email']
            )
            db.session.add(entity)
            db.session.flush() # Flush to get the generated entity.id

            # Create identifiers and map them
            id_student = Identifier(identifier_type='student_id', value=row['student_id'], entity_id=entity.id)
            id_email = Identifier(identifier_type='email', value=row['email'], entity_id=entity.id)
            id_card = Identifier(identifier_type='card_id', value=row['card_id'], entity_id=entity.id)
            db.session.add_all([id_student, id_email, id_card])

            # Populate the resolution map
            identifier_to_entity_map[row['student_id']] = entity
            identifier_to_entity_map[row['email']] = entity
            identifier_to_entity_map[row['card_id']] = entity

        # Process Staff
        for _, row in staff_df.iterrows():
            entity = Entity(
                name=row['name'],
                entity_type='staff',
                primary_email=row['email']
            )
            db.session.add(entity)
            db.session.flush()

            id_staff = Identifier(identifier_type='staff_id', value=row['staff_id'], entity_id=entity.id)
            id_email = Identifier(identifier_type='email', value=row['email'], entity_id=entity.id)
            id_card = Identifier(identifier_type='card_id', value=row['card_id'], entity_id=entity.id)
            db.session.add_all([id_staff, id_email, id_card])

            identifier_to_entity_map[row['staff_id']] = entity
            identifier_to_entity_map[row['email']] = entity
            identifier_to_entity_map[row['card_id']] = entity

        db.session.commit()
        print(f"Created {Entity.query.count()} entities.")
        print(f"Created {Identifier.query.count()} identifiers.")

        # --- 2. Process Events (Swipes, Wifi, Library) ---
        print("Processing events and linking to entities...")

        # Process Swipes
        for _, row in swipes_df.iterrows():
            entity = identifier_to_entity_map.get(row['card_id'])
            if entity:
                event = Event(
                    entity_id=entity.id,
                    timestamp=datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'),
                    location=row['location_name'],
                    source_type='swipe',
                    description=f"Card swipe at {row['location_name']}."
                )
                db.session.add(event)

        # Process Wifi Logs
        for _, row in wifi_df.iterrows():
            entity = identifier_to_entity_map.get(row['user_email'])
            if entity:
                event = Event(
                    entity_id=entity.id,
                    timestamp=datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'),
                    location=row['ap_location'],
                    source_type='wifi',
                    description=f"Connected to Wi-Fi AP {row['ap_location']}."
                )
                db.session.add(event)

                # Also, add the device hash as a new identifier if not already present
                if not identifier_to_entity_map.get(row['device_hash']):
                    id_device = Identifier(identifier_type='device_hash', value=row['device_hash'], entity_id=entity.id)
                    db.session.add(id_device)
                    identifier_to_entity_map[row['device_hash']] = entity

        # Process Library Checkouts
        for _, row in library_df.iterrows():
            entity = identifier_to_entity_map.get(row['student_id'])
            if entity:
                event = Event(
                    entity_id=entity.id,
                    timestamp=datetime.strptime(row['checkout_timestamp'], '%Y-%m-%d %H:%M:%S'),
                    location=row['location'],
                    source_type='library',
                    description=f"Checked out book: '{row['book_title']}'."
                )
                db.session.add(event)

        db.session.commit()
        print(f"Created {Event.query.count()} events.")
        print("Database seeding complete!")


if __name__ == '__main__':
    seed_database()