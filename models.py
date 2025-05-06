from datetime import datetime
from app import db

class Dog(db.Model):
    __tablename__ = 'dogs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    coat = db.Column(db.String(100))
    microchip_number = db.Column(db.String(50), unique=True)
    microchip_date = db.Column(db.Date)
    birth_date = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    in_breeding = db.Column(db.Boolean, default=True, nullable=False)
    sold = db.Column(db.Boolean, default=False, nullable=False)
    sold_date = db.Column(db.Date)
    
    # Box location 
    box = db.Column(db.String(50), default='')
    
    # Out of facility tracking
    is_out = db.Column(db.Boolean, default=False)
    out_date = db.Column(db.Date)
    return_date = db.Column(db.Date)
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Parent references (for genealogy)
    mother_id = db.Column(db.Integer, db.ForeignKey('dogs.id'))
    father_id = db.Column(db.Integer, db.ForeignKey('dogs.id'))
    
    # Relationships
    mother = db.relationship('Dog', foreign_keys=[mother_id], remote_side=[id], backref='mother_puppies')
    father = db.relationship('Dog', foreign_keys=[father_id], remote_side=[id], backref='father_puppies')
    vaccinations = db.relationship('Vaccination', backref='dog', cascade='all, delete-orphan')
    
    # Mating relationships
    matings_as_female = db.relationship('Mating', foreign_keys='Mating.female_id', backref='female', cascade='all, delete-orphan')
    matings_as_male = db.relationship('Mating', foreign_keys='Mating.male_id', backref='male', cascade='all, delete-orphan')
    
    # Birth relationship
    births = db.relationship('Birth', backref='mother', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Dog {self.name}>'


class Vaccination(db.Model):
    __tablename__ = 'vaccinations'
    
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Vaccination {self.type} for Dog {self.dog_id}>'


class Mating(db.Model):
    __tablename__ = 'matings'
    
    id = db.Column(db.Integer, primary_key=True)
    female_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable=False)
    male_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'natural' or 'artificial'
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    births = db.relationship('Birth', backref='mating', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Mating between Female {self.female_id} and Male {self.male_id}>'


class Birth(db.Model):
    __tablename__ = 'births'
    
    id = db.Column(db.Integer, primary_key=True)
    mother_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable=False)
    mating_id = db.Column(db.Integer, db.ForeignKey('matings.id'))
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'natural' or 'cesarean'
    puppies_count = db.Column(db.Integer, nullable=False)
    male_count = db.Column(db.Integer, default=0)
    female_count = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<Birth {self.date} for Mother {self.mother_id}>'


class OutLog(db.Model):
    __tablename__ = 'out_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    dog_id = db.Column(db.Integer, db.ForeignKey('dogs.id'), nullable=False)
    action = db.Column(db.String(10), nullable=False)  # 'out' or 'return'
    date = db.Column(db.Date, nullable=False)
    expected_return_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relazione con il cane
    dog = db.relationship('Dog', backref='out_logs')
    
    def __repr__(self):
        return f'<OutLog {self.action} for Dog {self.dog_id} on {self.date}>'
