import os
import requests
import psycopg2
from common.utils.env_util import get_env

# =========================================================
# Data Dragon URLs
# =========================================================
VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"
CHAMPION_LIST_URL = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/champion.json"
ICON_BASE = "https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{filename}"


def get_latest_version():
    resp = requests.get(VERSIONS_URL, timeout=15)
    resp.raise_for_status()
    versions = resp.json()
    return versions[0]


def main():
    # =====================================================
    # 1) Load environment variables
    # =====================================================
    env = get_env()
    db_config = {
        "dbname": env("DB_NAME"),
        "user": env("DB_USER"),
        "password": env("DB_PASSWORD"),
        "host": env("DB_HOST"),
        "port": env("DB_PORT"),
    }

    # =====================================================
    # 2) Fetch champion data
    # =====================================================
    print("🔍 Fetching latest Data Dragon version...")
    version = get_latest_version()
    print(f"✅ Using Data Dragon version: {version}")

    locale = "en_US"
    url = CHAMPION_LIST_URL.format(version=version, locale=locale)
    print(f"🌐 Fetching champions from {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json().get("data", {})

    if not data:
        print("❌ No champion data found.")
        return

    # =====================================================
    # 3) Connect to PostgreSQL
    # =====================================================
    print(f"🗄️  Connecting to database {db_config['dbname']} at {db_config['host']}:{db_config['port']}")
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    # =====================================================
    # 4) Upsert champions
    # =====================================================
    created = updated = 0
    for champ in data.values():
        champion_key = champ["id"]
        champion_id = int(champ["key"])
        name = champ.get("name", champion_key)
        title = champ.get("title", "")
        filename = champ.get("image", {}).get("full", f"{champion_key}.png")
        image_url = ICON_BASE.format(version=version, filename=filename)

        cur.execute(
            """
            INSERT INTO league_champions (champion_id, champion_key, name, title, image_url)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (champion_id) DO UPDATE
            SET champion_key = EXCLUDED.champion_key,
                name = EXCLUDED.name,
                title = EXCLUDED.title,
                image_url = EXCLUDED.image_url
            """,
            (champion_id, champion_key, name, title, image_url),
        )
        if cur.rowcount == 1:
            created += 1
        else:
            updated += 1

    conn.commit()
    cur.close()
    conn.close()

    # =====================================================
    # 5) Summary
    # =====================================================
    print(f"🎯 Done. Champions upserted: created={created}, updated={updated}")
    print(f"🧩 Version: {version} | Locale: {locale}")


if __name__ == "__main__":
    main()
