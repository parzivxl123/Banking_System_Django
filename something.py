from passlib.context import CryptContext



pwd_context: CryptContext = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

password = "hello123"

print(type(password))
print(len(password))

hashed = pwd_context.hash(password)

print(hashed)

print(
    pwd_context.verify(
        password,
        hashed
    )
)