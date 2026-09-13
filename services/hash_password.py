from pwdlib import PasswordHash

_password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """
    Hashing user password.

    :password: Password for hashing.
    :return: Hash 
    """
    return _password_hash.hash(password)

def is_valid_password(password: str, hashed_password: str) -> bool:
    """
    Checking if password is valid. If password is equal hash that return True else return False. 
    
    :password: String password.
    :hashed_password: Hashed password.

    :return: True if valid, else False.
    """
    return _password_hash.verify(password, hashed_password)
