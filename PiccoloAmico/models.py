from datetime import datetime
from app_api import db

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    father_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=True)
    mother_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=True)
    father = db.relationship('Dog', foreign_keys=[father_id], remote_side='Dog.id', backref='father_children', post_update=True)
    mother = db.relationship('Dog', foreign_keys=[mother_id], remote_side='Dog.id', backref='mother_children', post_update=True)
    nome = db.Column(db.String(100), nullable=False)
    sesso = db.Column(db.String(10), nullable=False)  # male/female
    razza = db.Column(db.String(100))
    colore = db.Column(db.String(100))
    box = db.Column(db.String(50))
    birth_date = db.Column(db.Date)
    microchip_number = db.Column(db.String(50))

    microchip_implanted = db.Column(db.Boolean, default=False)
    microchip_implant_date = db.Column(db.Date, nullable=True)
    microchip_inserted = db.Column(db.Boolean, default=False)
    microchip_date = db.Column(db.Date)
    is_sold = db.Column(db.Boolean, default=False)

    # Out of facility tracking
    is_out = db.Column(db.Boolean, default=False)
    out_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

    # Relationships
    vaccinations = db.relationship('Vaccination', backref='dog', lazy=True)
    mating_events = db.relationship('MatingEvent', backref='dog', lazy=True)
    births = db.relationship('Birth', backref='dog', lazy=True)

class Vaccination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    vaccine_type = db.Column(db.String(100), nullable=False)
    vaccine_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)

class MatingEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    mating_date = db.Column(db.Date, nullable=False)
    mating_type = db.Column(db.String(20), nullable=False)  # natural/artificial
    male_dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=True)
    male_dog = db.relationship('Dog', foreign_keys=[male_dog_id])

class Birth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    birth_type = db.Column(db.String(20), nullable=False)  # cesarean/natural
    puppy_count = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

class EventLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Pregnancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    sire_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    expected_due_date = db.Column(db.Date, nullable=True)
    actual_due_date = db.Column(db.Date, nullable=True)
    litter_size = db.Column(db.Integer, nullable=True)
    males_count = db.Column(db.Integer, nullable=True)
    females_count = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(50), default='Active')  # Active, Completed, Terminated
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with sire
    sire = db.relationship('Dog', foreign_keys=[sire_id])

    def __repr__(self):
        return f'<Pregnancy {self.id} - Dog {self.dog_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'dog_id': self.dog_id,
            'sire_id': self.sire_id,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'expected_due_date': self.expected_due_date.strftime('%Y-%m-%d') if self.expected_due_date else None,
            'actual_due_date': self.actual_due_date.strftime('%Y-%m-%d') if self.actual_due_date else None,
            'litter_size': self.litter_size,
            'males_count': self.males_count,
            'females_count': self.females_count,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class HeatCycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    intensity = db.Column(db.String(20), nullable=True)  # Mild, Moderate, Severe
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<HeatCycle {self.id} - Dog {self.dog_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'dog_id': self.dog_id,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'intensity': self.intensity,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dog.id'), nullable=False)
    location_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    is_current = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Location {self.id} - Dog {self.dog_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'dog_id': self.dog_id,
            'location_name': self.location_name,
            'description': self.description,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'is_current': self.is_current,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }