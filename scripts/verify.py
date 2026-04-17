"""
DevDocs Assistant — Stack Verification Script

Confirms that all infrastructure services are running and accessible:
  1. PostgreSQL connection via psycopg3
  2. Server version check
  3. pgvector extension enabled
  4. Vector operations (create table, insert, similarity search, cleanup)
  5. Redis connectivity

Usage:
    uv run python scripts/verify.py
"""

import os
import sys

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load environment variables from .env at repo root
# ---------------------------------------------------------------------------
# find_dotenv=False: we explicitly point to the repo root .env
# override=False: existing env vars take precedence (useful in CI)
load_dotenv(override=False)

DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set. Copy .env.example to .env")
    sys.exit(1)


def check_postgres() -> None:
    """Test PostgreSQL connectivity and basic operations."""
    import psycopg

    print("=" * 60)
    print("1. Connecting to PostgreSQL...")
    print("=" * 60)

    # psycopg3 uses 'with' for automatic connection cleanup.
    # autocommit=True: each statement runs in its own transaction.
    # In production you'd manage transactions explicitly, but for a
    # health check, autocommit keeps things simple.
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        # ---------------------------------------------------------------
        # Server version
        # ---------------------------------------------------------------
        row = conn.execute("SELECT version()").fetchone()
        print(f"   Connected: {row[0]}")
        print()

        # ---------------------------------------------------------------
        # Enable pgvector extension
        # ---------------------------------------------------------------
        print("2. Enabling pgvector extension...")
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        row = conn.execute(
            "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
        ).fetchone()
        print(f"   pgvector version: {row[0]}")
        print()

        # ---------------------------------------------------------------
        # Vector operations — the actual proof that pgvector works
        # ---------------------------------------------------------------
        print("3. Testing vector operations...")

        # Create a temporary table with a 3-dimensional vector column.
        # 3 dimensions keeps it simple for a smoke test.
        # In production we'll use 384 dimensions (bge-small-en-v1.5).
        conn.execute("""
            CREATE TABLE IF NOT EXISTS _verify_vectors (
                id    SERIAL PRIMARY KEY,
                label TEXT NOT NULL,
                embedding VECTOR(3)
            )
        """)

        # Insert test vectors.
        # Think of these as 3D points in space — cosine similarity
        # measures the angle between them, not the distance.
        conn.execute("""
            INSERT INTO _verify_vectors (label, embedding) VALUES
                ('cat',    '[1.0, 0.0, 0.0]'),
                ('kitten', '[0.9, 0.1, 0.0]'),
                ('dog',    '[0.0, 1.0, 0.0]'),
                ('car',    '[0.0, 0.0, 1.0]')
        """)

        # Similarity search: find the 2 closest vectors to 'cat' [1,0,0]
        # using cosine distance (<=>) — this is the operator you'll use
        # in every RAG query.
        #
        # Expected result: 'cat' (distance 0) and 'kitten' (very close).
        results = conn.execute("""
            SELECT label,
                   embedding,
                   embedding <=> '[1.0, 0.0, 0.0]' AS cosine_distance
            FROM _verify_vectors
            ORDER BY cosine_distance
            LIMIT 2
        """).fetchall()

        for label, embedding, distance in results:
            print(f"   {label:10s}  embedding={embedding}  distance={distance:.4f}")

        # Cleanup — don't leave test artifacts in the database
        conn.execute("DROP TABLE _verify_vectors")
        print("   Table created, queried, and cleaned up successfully.")
        print()


def check_redis() -> None:
    """Test Redis connectivity."""
    print("4. Connecting to Redis...")

    # redis-py is not in our dependencies yet (we don't need it
    # until Phase 5), so we handle ImportError gracefully.
    try:
        import redis
    except ImportError:
        print("   SKIPPED: redis package not installed (expected until Phase 5)")
        print()
        return

    r = redis.from_url(REDIS_URL)
    pong = r.ping()
    print(f"   Redis ping: {'PONG' if pong else 'FAILED'}")
    print()


def main() -> None:
    """Run all health checks."""
    print()
    print("DevDocs Assistant — Stack Verification")
    print()

    try:
        check_postgres()
    except Exception as e:
        print(f"   POSTGRES FAILED: {e}")
        sys.exit(1)

    try:
        check_redis()
    except Exception as e:
        print(f"   REDIS FAILED: {e}")
        sys.exit(1)

    print("=" * 60)
    print("All checks passed. Stack is ready.")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
