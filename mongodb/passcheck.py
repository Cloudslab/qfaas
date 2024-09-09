import bcrypt

# The stored bcrypt hash
stored_hash = b"$2b$12$DSgu8/q5Wb2UNEo/fFLTquqsajfTerZpayYM.ZiADBmV/e.25zey2"

# The plain-text password to verify
password = b"QFaaS@2024" # Default password

# Verify the password
if bcrypt.checkpw(password, stored_hash):
    print("Password matches!")
else:
    print("Password does not match.")