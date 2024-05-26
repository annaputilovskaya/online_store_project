import secrets
import string


def generate_password():
    special_chars = "!@#$%^&*()_+/"
    password_characters = string.ascii_letters + string.digits + special_chars
    password = "".join(secrets.choice(password_characters) for _ in range(10))
    return password
