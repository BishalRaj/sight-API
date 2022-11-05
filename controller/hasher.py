from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], depricated="auto")


class Hasher:
    def get_hash_password(password):
        return hash_password
