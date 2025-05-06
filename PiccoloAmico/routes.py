from flask import render_template, request, redirect, url_for, flash, jsonify, abort
from datetime import datetime
from app import app, db
from models import Dog, Pregnancy, HeatCycle, Location

# Helper function to parse date from string
def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

# API Routes for Netlify frontend
@app.route('/api/dogs', methods=['GET'])
def api_dogs_list():
    dogs = Dog.query.all()
    return jsonify([dog.to_dict() for dog in dogs])

@app.route('/api/dogs/<int:dog_id>', methods=['GET'])
def api_dog_detail(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    return jsonify(dog.to_dict())

@app.route('/api/dogs', methods=['POST'])
def api_add_dog():
    data = request.json
    
    # Check required fields
    if not data.get('name') or not data.get('breed') or not data.get('gender'):
        return jsonify({'error': 'Name, breed, and gender are required'}), 400
    
    # Create new dog
    dog = Dog(
        name=data.get('name'),
        breed=data.get('breed'),
        gender=data.get('gender'),
        birth_date=parse_date(data.get('birth_date')),
        registration_number=data.get('registration_number'),
        microchip_number=data.get('microchip_number'),
        sire_id=data.get('sire_id'),
        dam_id=data.get('dam_id'),
        notes=data.get('notes')
    )
    
    db.session.add(dog)
    db.session.commit()
    
    return jsonify(dog.to_dict()), 201

@app.route('/api/dogs/<int:dog_id>', methods=['PUT'])
def api_update_dog(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    data = request.json
    
    # Update fields
    dog.name = data.get('name', dog.name)
    dog.breed = data.get('breed', dog.breed)
    dog.gender = data.get('gender', dog.gender)
    dog.birth_date = parse_date(data.get('birth_date')) or dog.birth_date
    dog.registration_number = data.get('registration_number', dog.registration_number)
    dog.microchip_number = data.get('microchip_number', dog.microchip_number)
    dog.sire_id = data.get('sire_id', dog.sire_id)
    dog.dam_id = data.get('dam_id', dog.dam_id)
    dog.is_active = data.get('is_active', dog.is_active)
    dog.notes = data.get('notes', dog.notes)
    
    db.session.commit()
    
    return jsonify(dog.to_dict())

@app.route('/api/dogs/<int:dog_id>', methods=['DELETE'])
def api_delete_dog(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    db.session.delete(dog)
    db.session.commit()
    
    return jsonify({'message': 'Dog deleted successfully'})

# Pregnancy API endpoints
@app.route('/api/pregnancies', methods=['GET'])
def api_pregnancies_list():
    pregnancies = Pregnancy.query.all()
    return jsonify([pregnancy.to_dict() for pregnancy in pregnancies])

@app.route('/api/dogs/<int:dog_id>/pregnancies', methods=['GET'])
def api_dog_pregnancies(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    pregnancies = Pregnancy.query.filter_by(dog_id=dog_id).all()
    return jsonify([pregnancy.to_dict() for pregnancy in pregnancies])

@app.route('/api/pregnancies', methods=['POST'])
def api_add_pregnancy():
    data = request.json
    
    # Check required fields
    if not data.get('dog_id') or not data.get('start_date'):
        return jsonify({'error': 'Dog ID and start date are required'}), 400
    
    # Create new pregnancy
    pregnancy = Pregnancy(
        dog_id=data.get('dog_id'),
        sire_id=data.get('sire_id'),
        start_date=parse_date(data.get('start_date')),
        expected_due_date=parse_date(data.get('expected_due_date')),
        actual_due_date=parse_date(data.get('actual_due_date')),
        litter_size=data.get('litter_size'),
        males_count=data.get('males_count'),
        females_count=data.get('females_count'),
        status=data.get('status', 'Active'),
        notes=data.get('notes')
    )
    
    db.session.add(pregnancy)
    db.session.commit()
    
    return jsonify(pregnancy.to_dict()), 201

@app.route('/api/pregnancies/<int:pregnancy_id>', methods=['PUT'])
def api_update_pregnancy(pregnancy_id):
    pregnancy = Pregnancy.query.get_or_404(pregnancy_id)
    data = request.json
    
    # Update fields
    pregnancy.sire_id = data.get('sire_id', pregnancy.sire_id)
    pregnancy.start_date = parse_date(data.get('start_date')) or pregnancy.start_date
    pregnancy.expected_due_date = parse_date(data.get('expected_due_date')) or pregnancy.expected_due_date
    pregnancy.actual_due_date = parse_date(data.get('actual_due_date')) or pregnancy.actual_due_date
    pregnancy.litter_size = data.get('litter_size', pregnancy.litter_size)
    pregnancy.males_count = data.get('males_count', pregnancy.males_count)
    pregnancy.females_count = data.get('females_count', pregnancy.females_count)
    pregnancy.status = data.get('status', pregnancy.status)
    pregnancy.notes = data.get('notes', pregnancy.notes)
    
    db.session.commit()
    
    return jsonify(pregnancy.to_dict())

# Heat Cycle API endpoints
@app.route('/api/heat-cycles', methods=['GET'])
def api_heat_cycles_list():
    heat_cycles = HeatCycle.query.all()
    return jsonify([cycle.to_dict() for cycle in heat_cycles])

@app.route('/api/dogs/<int:dog_id>/heat-cycles', methods=['GET'])
def api_dog_heat_cycles(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    heat_cycles = HeatCycle.query.filter_by(dog_id=dog_id).all()
    return jsonify([cycle.to_dict() for cycle in heat_cycles])

@app.route('/api/heat-cycles', methods=['POST'])
def api_add_heat_cycle():
    data = request.json
    
    # Check required fields
    if not data.get('dog_id') or not data.get('start_date'):
        return jsonify({'error': 'Dog ID and start date are required'}), 400
    
    # Create new heat cycle
    heat_cycle = HeatCycle(
        dog_id=data.get('dog_id'),
        start_date=parse_date(data.get('start_date')),
        end_date=parse_date(data.get('end_date')),
        intensity=data.get('intensity'),
        notes=data.get('notes')
    )
    
    db.session.add(heat_cycle)
    db.session.commit()
    
    return jsonify(heat_cycle.to_dict()), 201

# Location API endpoints
@app.route('/api/locations', methods=['GET'])
def api_locations_list():
    locations = Location.query.all()
    return jsonify([loc.to_dict() for loc in locations])

@app.route('/api/dogs/<int:dog_id>/locations', methods=['GET'])
def api_dog_locations(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    locations = Location.query.filter_by(dog_id=dog_id).all()
    return jsonify([loc.to_dict() for loc in locations])

@app.route('/api/locations', methods=['POST'])
def api_add_location():
    data = request.json
    
    # Check required fields
    if not data.get('dog_id') or not data.get('location_name') or not data.get('start_date'):
        return jsonify({'error': 'Dog ID, location name, and start date are required'}), 400
    
    # If this is marked as current, update all other locations for this dog to not current
    if data.get('is_current', True):
        Location.query.filter_by(dog_id=data.get('dog_id'), is_current=True).update({'is_current': False})
    
    # Create new location
    location = Location(
        dog_id=data.get('dog_id'),
        location_name=data.get('location_name'),
        description=data.get('description'),
        start_date=parse_date(data.get('start_date')),
        end_date=parse_date(data.get('end_date')),
        is_current=data.get('is_current', True),
        notes=data.get('notes')
    )
    
    db.session.add(location)
    db.session.commit()
    
    return jsonify(location.to_dict()), 201

# Web interface routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dogs')
def dogs_list():
    dogs = Dog.query.all()
    return render_template('dogs/list.html', dogs=dogs)

@app.route('/dogs/add', methods=['GET', 'POST'])
def dog_add():
    if request.method == 'POST':
        # Create new dog from form data
        dog = Dog(
            name=request.form['name'],
            breed=request.form['breed'],
            gender=request.form['gender'],
            birth_date=parse_date(request.form.get('birth_date')),
            registration_number=request.form.get('registration_number'),
            microchip_number=request.form.get('microchip_number'),
            sire_id=request.form.get('sire_id') if request.form.get('sire_id') else None,
            dam_id=request.form.get('dam_id') if request.form.get('dam_id') else None,
            notes=request.form.get('notes')
        )
        
        db.session.add(dog)
        db.session.commit()
        
        flash('Dog added successfully!', 'success')
        return redirect(url_for('dogs_list'))
    
    # Get potential parents for selection
    male_dogs = Dog.query.filter_by(gender='Male').all()
    female_dogs = Dog.query.filter_by(gender='Female').all()
    
    return render_template('dogs/add.html', male_dogs=male_dogs, female_dogs=female_dogs)

@app.route('/dogs/<int:dog_id>')
def dog_detail(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    pregnancies = Pregnancy.query.filter_by(dog_id=dog_id).all()
    heat_cycles = HeatCycle.query.filter_by(dog_id=dog_id).all()
    locations = Location.query.filter_by(dog_id=dog_id).all()
    current_location = Location.query.filter_by(dog_id=dog_id, is_current=True).first()
    
    return render_template('dogs/detail.html', 
                          dog=dog, 
                          pregnancies=pregnancies, 
                          heat_cycles=heat_cycles, 
                          locations=locations,
                          current_location=current_location)

@app.route('/dogs/<int:dog_id>/edit', methods=['GET', 'POST'])
def dog_edit(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    
    if request.method == 'POST':
        # Update dog from form data
        dog.name = request.form['name']
        dog.breed = request.form['breed']
        dog.gender = request.form['gender']
        dog.birth_date = parse_date(request.form.get('birth_date'))
        dog.registration_number = request.form.get('registration_number')
        dog.microchip_number = request.form.get('microchip_number')
        dog.sire_id = request.form.get('sire_id') if request.form.get('sire_id') else None
        dog.dam_id = request.form.get('dam_id') if request.form.get('dam_id') else None
        dog.is_active = 'is_active' in request.form
        dog.notes = request.form.get('notes')
        dog.microchip_data = parse_date(request.form.get('microchip_data'))
        dog.chip_inserito = request.form.get('chip_inserito')
        dog.venduto = request.form.get('venduto')
        
        db.session.commit()
        
        flash('Dog updated successfully!', 'success')
        return redirect(url_for('dog_detail', dog_id=dog.id))
    
    # Get potential parents for selection
    male_dogs = Dog.query.filter_by(gender='Male').all()
    female_dogs = Dog.query.filter_by(gender='Female').all()
    
    return render_template('dogs/edit.html', dog=dog, male_dogs=male_dogs, female_dogs=female_dogs)



@app.route('/dogs/<int:dog_id>/vaccinations', methods=['GET', 'POST'])
def manage_vaccinations(dog_id):
    dog = Dog.query.get_or_404(dog_id)
    
    if request.method == 'POST':
        vaccination = Vaccination(
            cane_id=dog_id,
            tipo=request.form['tipo'],
            data=parse_date(request.form['data']),
            note=request.form.get('note', '')
        )
        db.session.add(vaccination)
        db.session.commit()
        flash('Vaccination added successfully', 'success')
        
    return redirect(url_for('dog_detail', dog_id=dog_id))

@app.route('/vaccinations/<int:vacc_id>/edit', methods=['POST'])
def edit_vaccination(vacc_id):
    vaccination = Vaccination.query.get_or_404(vacc_id)
    vaccination.tipo = request.form['tipo']
    vaccination.data = parse_date(request.form['data'])
    vaccination.note = request.form.get('note', '')
    db.session.commit()
    flash('Vaccination updated successfully', 'success')
    return redirect(url_for('dog_detail', dog_id=vaccination.cane_id))

@app.route('/vaccinations/<int:vacc_id>/delete', methods=['POST'])
def delete_vaccination(vacc_id):
    vaccination = Vaccination.query.get_or_404(vacc_id)
    dog_id = vaccination.cane_id
    db.session.delete(vaccination)
    db.session.commit()
    flash('Vaccination deleted successfully', 'success')
    return redirect(url_for('dog_detail', dog_id=dog_id))

@app.route('/vaccinations/<int:vacc_id>/edit', methods=['POST'])
def edit_vaccination(vacc_id):
    vaccination = Vaccination.query.get_or_404(vacc_id)
    vaccination.tipo = request.form['tipo']
    vaccination.data = parse_date(request.form['data'])
    vaccination.note = request.form.get('note')
    db.session.commit()
    flash('Vaccination updated successfully', 'success')
    return redirect(url_for('dog_detail', dog_id=vaccination.cane_id))

@app.route('/vaccinations/<int:vacc_id>/delete', methods=['POST'])
def delete_vaccination(vacc_id):
    vaccination = Vaccination.query.get_or_404(vacc_id)
    dog_id = vaccination.cane_id
    db.session.delete(vaccination)
    db.session.commit()
    flash('Vaccination deleted successfully', 'success')
    return redirect(url_for('dog_detail', dog_id=dog_id))

@app.route('/vaccinations/<int:vacc_id>/delete', methods=['POST'])
def delete_vaccination(vacc_id):
    vaccination = Vaccination.query.get_or_404(vacc_id)
    dog_id = vaccination.cane_id
    db.session.delete(vaccination)
    db.session.commit()
    return redirect(url_for('dog_detail', dog_id=dog_id))


@app.route('/statistics', methods=['GET'])
def statistics():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

    query = Pregnancy.query
    if start_date:
        query = query.filter(Pregnancy.date >= start_date)
    if end_date:
        query = query.filter(Pregnancy.date <= end_date)

    cesarei = query.filter_by(tipo='Cesareo').count()
    naturali = query.filter_by(tipo='Naturale').count()

    query_v = Vaccination.query
    if start_date:
        query_v = query_v.filter(Vaccination.date >= start_date)
    if end_date:
        query_v = query_v.filter(Vaccination.date <= end_date)
    vaccinazioni_totali = query_v.count()

    query_m = MatingEvent.query
    if start_date:
        query_m = query_m.filter(MatingEvent.date >= start_date)
    if end_date:
        query_m = query_m.filter(MatingEvent.date <= end_date)
    accoppiamenti_totali = query_m.count()

    return render_template('statistics.html', cesarei=cesarei, naturali=naturali,
                           vaccinazioni_totali=vaccinazioni_totali,
                           accoppiamenti_totali=accoppiamenti_totali)
