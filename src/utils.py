import secrets
import string


def random_string(length: int = 7) -> str:
    return ''.join(secrets.choice(string.ascii_letters) for _ in range(length))