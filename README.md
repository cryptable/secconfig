Secure Config
=============

Introdution
-----------

Simple configuration library which support encryption and tamper detection.
The secret protecting the configuration are stored in environment variables or .env files.
By convention the files are protected with HMAC512.
By convention the secure data is encrypted with A256GCM with A256KW.
The keys of the protection are stored in .env file.
The idea it to store the necessary parameters in the file to encrypt/decrypt secure configurations from a database.

API
---

### Load secure configuration

Command:
```python
def load_secconfig(secure_config: str,
    *,
    signing_key: str = None,
    encryption_key: str = None,
    sign_algo: str = None,
) -> str
```

Params: 

| param          | Explanation                                                                    |
|----------------|--------------------------------------------------------------------------------|
| secure_config  | string to be decrypted using the environment, .env-file or optional parameters |
| signing_key    | optional: hash-key (512 bits or 64 bytes) to verify the configuration file     | 
| encryption-key | optional: symmetric encryption key to decrypt the configuration file           | 
| sign-algo      | optional: signature algorithm to verify the file                               | 

Description: Decrypt the encrypted configuration file and return the plain string of the configuration file.
You need to parse it further using json or yaml or eny kind of configuration file you encrypted using the tools.

### Create secure configuration

Command:
```python
def create_secconfig(secure_config: str,
    json_data: str,
    *,
    signing_key: str = None,
    encryption_key: str = None,
    sign_algo: str = None,
    enc_algo: str = None,
    kek_algo: str = None,
) -> str
```

Params: 

| param          | Explanation                                                                              |
|----------------|------------------------------------------------------------------------------------------|
| jsdn_data      | string to be encrypted using the environment variables, .env-file or optional parameters |
| signing_key    | optional: hash-key (512 bits or 64 bytes) to sign the configuration file                 | 
| encryption-key | optional: symmetric encryption key to encrypt the configuration file                     | 
| sign-algo      | optional: signature algorithm to sign the file                                           | 
| enc_algo       | optional: encryption algorithm to encrypt the file                                       | 
| sign-algo      | optional: key-wrapping algorithm to keywrap the symmetric encryption key                 | 

Description: Decrypt the encrypted configuration file and return the plain string of the configuration file.
You need to parse it further using json or yaml or eny kind of configuration file you encrypted using the tools.

CLI
---

### Generate .env file

Command: **secconfig env-file**

Params: 

| param     | short | Explanation                           |
|-----------|-------|---------------------------------------|
| --file    | -f    | store in file filename (default .env) |
| --verbose | -v    | Show configuration to screen          |

Description: Create .env-file with security parameters. This .env-file will be loaded on startup of the application.
You can also use the file to create the environment parameters in container for example.
You can also adapt the default file, but document yourself before adapting it.

examples
- Create .env file in cmd directory
```sh
secconfig env-file 
```

### Create your config-file

Command: **secconfig create**

Params: 

| param     | short | Explanation                      |
|-----------|-------|----------------------------------|
| --infile  | -i    | config-file filename to protect  |
| --outfile | -o    | output filename for application  |
| --envfile | -e    | path to .env-file (default .env) |
| --verbose | -v    | show the encrypted content       |

Description: Create secure configuration file using the environment variables or .env file.

examples
- Create secure config file
```sh
secconfig create -i config.json -o config.sec 
```

### Show content of secure config-file

Command: **secconfig show**

Params: 

| param     | short | Explanation                            |
|-----------|-------|----------------------------------------|
| --infile  | -i    | secure config-file filename to protect |
| --outfile | -o    | output filename to store plain config  |
| --envfile | -e    | path to .env-file (default .env)       |

Description: Decrypts the secure configuration file and store the decrypted file in the output-filename.

examples
- Show secure config file
```sh
secconfig show -i config.sec -o config.json 
```

Supports:
- generate .env file with necessary variables
- output is jose string-data.

TODO
----

- Asymmetric key support