from jaguar.models.target import Room

# Test target model
def test_db(db):
    session = db()
    room = Room(title='example', type='room')
    session.add(room)
    session.commit()
    assert session.query(Room).count() == 1

# Test members of a room


# Test admins of a room

# Test rooms with the same name


