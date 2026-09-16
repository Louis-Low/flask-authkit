from app import bcrypt


def test_password_hashing(app):
    with app.app_context():
        hashed = bcrypt.generate_password_hash("correct horse battery staple")
        assert bcrypt.check_password_hash(hashed, "correct horse battery staple")
        assert not bcrypt.check_password_hash(hashed, "wrong")


def test_registration_and_duplicate_account(client):
    response = client.post("/register", data={"username":"alex", "email":"alex@example.com", "password":"StrongPass1!", "confirm_password":"StrongPass1!", "terms":"y"}, follow_redirects=True)
    assert b"Account created" in response.data
    response = client.post("/register", data={"username":"alex", "email":"alex@example.com", "password":"StrongPass1!", "confirm_password":"StrongPass1!", "terms":"y"})
    assert b"already" in response.data


def test_login_logout_and_protected_route(client):
    client.post("/register", data={"username":"alex", "email":"alex@example.com", "password":"StrongPass1!", "confirm_password":"StrongPass1!", "terms":"y"})
    assert client.get("/profile").status_code == 302
    response = client.post("/login", data={"identity":"alex@example.com", "password":"StrongPass1!"}, follow_redirects=True)
    assert b"Your profile" in response.data
    assert client.get("/logout").status_code == 302


def test_failed_login(client):
    client.post("/register", data={"username":"alex", "email":"alex@example.com", "password":"StrongPass1!", "confirm_password":"StrongPass1!", "terms":"y"})
    response = client.post("/login", data={"identity":"alex@example.com", "password":"wrongpass"})
    assert b"Invalid sign-in details" in response.data


def test_invalid_registration(client):
    response = client.post("/register", data={"username":"a", "email":"not-email", "password":"short", "confirm_password":"different"})
    assert response.status_code == 200
    assert b"valid email" in response.data or b"Field must be between" in response.data
