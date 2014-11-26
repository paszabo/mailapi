import md5crypt

from .helpers import generate_random_strings


def generate_md5_password(p):
    p = str(p).strip()
    return md5crypt.unix_md5_crypt(p, generate_random_strings(length=8))
