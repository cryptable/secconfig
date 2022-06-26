import binascii
import os
import secrets

import dotenv
from jose import jwe, jws


def generate_env_params():
    return {
        "SIGNING_KEY": secrets.token_hex(64),
        "ENCRYPTION_KEY": secrets.token_hex(32),
        "KEK_ALGORITHM": "A256KW",
        "SIGN_ALGORITHM": "HS512",
        "ENCRYPTION_ALGORITHM": "A256GCM",
    }


def store_env(env_vars: dict, *, path: str = ".env"):
    with open(path, "w") as fp:
        for (key, value) in env_vars.items():
            fp.write(f"{key}={value}\n")


def load_env(*, path: str = ".env"):
    dotenv.load_dotenv(path)


def create_secconfig(
    json_data: str,
    *,
    signing_key: str = None,
    encryption_key: str = None,
    sign_algo: str = None,
    enc_algo: str = None,
    kek_algo: str = None,
) -> str:
    if not signing_key:
        signing_key = os.getenv("SIGNING_KEY")
    if not encryption_key:
        encryption_key = os.getenv("ENCRYPTION_KEY")
    if not sign_algo:
        sign_algo = (
            os.getenv("SIGN_ALGORITHM") if os.getenv("SIGN_ALGORITHM") else "HS512"
        )
    if not enc_algo:
        enc_algo = (
            os.getenv("ENCRYPTION_ALGORITHM")
            if os.getenv("ENCRYPTION_ALGORITHM")
            else "A256GCM"
        )
    if not kek_algo:
        kek_algo = (
            os.getenv("KEK_ALGORITHM") if os.getenv("KEK_ALGORITHM") else "A256KW"
        )

    if not signing_key or not encryption_key:
        raise ValueError(
            "Missing Signing or Encryption key, check .env or environment variables"
        )

    return jws.sign(
        jwe.encrypt(
            json_data.encode("UTF8"),
            binascii.unhexlify(encryption_key),
            algorithm=kek_algo,
            encryption=enc_algo,
        ),
        binascii.unhexlify(signing_key),
        algorithm=sign_algo,
    )


def load_secconfig(
    secure_config: str,
    *,
    signing_key: str = None,
    encryption_key: str = None,
    sign_algo: str = None,
) -> str:
    if not signing_key:
        signing_key = os.getenv("SIGNING_KEY")
    if not encryption_key:
        encryption_key = os.getenv("ENCRYPTION_KEY")
    if not sign_algo:
        sign_algo = (
            os.getenv("SIGN_ALGORITHM") if os.getenv("SIGN_ALGORITHM") else "HS512"
        )

    if not signing_key or not encryption_key:
        raise ValueError(
            "Missing Signing or Encryption key, check .env or environment variables"
        )
    enc_data = jws.verify(secure_config, binascii.unhexlify(signing_key), sign_algo)
    return jwe.decrypt(enc_data, binascii.unhexlify(encryption_key)).decode("utf-8")
