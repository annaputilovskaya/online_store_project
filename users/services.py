import secrets
import string


def generate_password():
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(password_characters) for _ in range(10))
    return password

