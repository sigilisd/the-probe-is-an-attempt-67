import os, django, sys
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        print("✅ База данных работает!")
        
        cursor.execute("SELECT version();")
        print(f"🐘 {cursor.fetchone()[0][:50]}...")
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\n📋 Все таблицы ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
            
except Exception as e:
    print(f"❌ Ошибка: {e}")