import psycopg2

# Replace these with YOUR Supabase details
SUPABASE_HOST = "db.okjbnnezljpzbloyjwip.supabase.co"
SUPABASE_DB = "postgres"
SUPABASE_USER = "postgres"  # or postgres.[randomstring]
SUPABASE_PASSWORD = "your_supabase_db_password"
SUPABASE_PORT = "5432"

try:
    conn = psycopg2.connect(
        host=SUPABASE_HOST,
        database=SUPABASE_DB,
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD,
        port=SUPABASE_PORT
    )
    print("✅ Connection successful! You can now run queries.")
    
    # Quick test: List tables (should show 'public' schema stuff)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cur.fetchall()
    print("Tables in public schema:", [t[0] for t in tables])
    
    cur.close()
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
    print("\nCommon fixes:")
    print("1. Double-check password (reset in Supabase Dashboard > Settings > Database).")
    print("2. Use port 5432 for direct (non-pooled) connection.")
    print("3. Ensure your IP is allowed: Dashboard > Settings > Database > Network Restrictions > Add your IP.")
