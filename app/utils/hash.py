import hashlib

def generate_hash(text: str) -> str:
    return hashlib.sha256(text[:500].encode()).hexdigest()