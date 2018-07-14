from jaguar.models.user import User

# Test target model
def test_user_model(db):
    session = db()
    user = User(
        title='example',
        user_name='example',
        email='example@example.com'
    )
    session.add(user)
    session.commit()
    assert session.query(User).count() == 1
