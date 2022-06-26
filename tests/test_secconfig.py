import binascii
import json

import jose.jws, jose.jwe

import secconfig.config
import os.path
import os
import dotenv
import pytest
from jose.backends.cryptography_backend import CryptographyAESKey as AESKey


@pytest.fixture
def sec_params():
    return secconfig.config.generate_env_params()


def test_gen_env_properties():
    env = secconfig.config.generate_env_params()

    assert len(env["SIGNING_KEY"]) == 128
    assert len(env["ENCRYPTION_KEY"]) == 64


def test_store_env_properties(tmp_path):
    secconfig.config.store_env(
        secconfig.config.generate_env_params(), path=os.path.join(tmp_path, ".env")
    )

    dotenv.load_dotenv(os.path.join(tmp_path, ".env"))

    assert len(os.getenv("SIGNING_KEY")) == 128
    assert len(os.getenv("ENCRYPTION_KEY")) == 64


def test_create_signed_data_secconfig(sec_params):
    ref_data = """
{
    "param1": "value param1",
    "param2": "value param2"
}
"""
    sec_config = secconfig.config.create_secconfig(
        ref_data,
        signing_key=sec_params["SIGNING_KEY"],
        encryption_key=sec_params["ENCRYPTION_KEY"],
        kek_algo="A256KW",
        enc_algo="A256GCM",
        sign_algo="HS512",
    )

    assert jose.jws.verify(
        sec_config, binascii.unhexlify(sec_params["SIGNING_KEY"]), "HS512"
    )
    encrypted_data = jose.jws.verify(
        sec_config, binascii.unhexlify(sec_params["SIGNING_KEY"]), "HS512"
    )
    assert jose.jwe.decrypt(
        encrypted_data, binascii.unhexlify(sec_params["ENCRYPTION_KEY"])
    )
    decrypted_data = jose.jwe.decrypt(
        encrypted_data, binascii.unhexlify(sec_params["ENCRYPTION_KEY"])
    )
    json_data = json.loads(decrypted_data)
    assert json_data["param1"] == "value param1"
    assert json_data["param2"] == "value param2"


def test_load_secconfig(sec_params):
    ref_data = """
{
    "param1": "value param1",
    "param2": "value param2"
}
"""
    sec_config = secconfig.config.create_secconfig(
        ref_data,
        signing_key=sec_params["SIGNING_KEY"],
        encryption_key=sec_params["ENCRYPTION_KEY"],
        kek_algo="A256KW",
        enc_algo="A256GCM",
        sign_algo="HS512",
    )

    config_data = secconfig.config.load_secconfig(
        sec_config,
        signing_key=sec_params["SIGNING_KEY"],
        encryption_key=sec_params["ENCRYPTION_KEY"],
        sign_algo="HS512",
    )
    json_data = json.loads(config_data)
    assert json_data["param1"] == "value param1"
    assert json_data["param2"] == "value param2"
