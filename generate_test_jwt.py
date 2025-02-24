import jwt
from datetime import datetime, timedelta

# Read the private key
with open('priv.pem', 'rb') as f:
    private_key = f.read()

# Create a payload
payload = {
    "sub": "user123",
    "name": "John Doe",
    "admin": True,
    "iat": int(datetime.utcnow().timestamp()),
    "exp": int((datetime.utcnow() + timedelta(days=1)).timestamp())
}

# Create the JWT
token = jwt.encode(payload, private_key, algorithm='RS256')

print("\nGenerated JWT:")
print(token)

# Verify the JWT
with open('publ.pem', 'rb') as f:
    public_key = f.read()

try:
    decoded = jwt.decode(token, public_key, algorithms=['RS256'])
    print("\nVerification successful!")
    print("Decoded payload:", decoded)
except Exception as e:
    print("\nVerification failed:", str(e))