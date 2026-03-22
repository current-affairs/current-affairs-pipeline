from core.database import SessionLocal
from models.content import Content

from services.normalization import normalize_content
from services.dedup import is_duplicate
from services.cluster import find_cluster, create_cluster
from services.language import detect_language
from utils.hash import generate_hash
from services.canonical import update_canonical_for_cluster
from core.source_priority import get_source_priority

def process_content(data):
    db = SessionLocal()

    clean_text = normalize_content(data["content"])


    language = detect_language(clean_text)

    hash_value = generate_hash(clean_text)

    if is_duplicate(db, hash_value):
        return "duplicate"

    cluster_id = find_cluster(db, clean_text)

    if not cluster_id:
        cluster_id = create_cluster()

    content = Content(
        source_name=data["source_name"],
        source_type=data["source_type"],
        source_url=data["url"],
        title=data["title"],
        content=clean_text,
        language=language,
        published_at=data["published_at"],
        hash=hash_value,
        cluster_id=cluster_id,
        source_priority = get_source_priority(data["source_name"])
    )

    db.add(content)
    db.commit()

    update_canonical_for_cluster(db, cluster_id)

    return "stored"