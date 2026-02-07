#!/usr/bin/env python3
"""
Test script to verify database connection and data loading
Run this before starting the dashboard to ensure everything works
"""

import pandas as pd
from sqlalchemy import create_engine
import sys

def test_connection():
    print("=" * 80)
    print("TESTING DATABASE CONNECTION")
    print("=" * 80)

    try:
        # Create connection
        print("\n1. Creating database connection...")
        connection_url = "postgresql://ds_ro_tenger_ways_bb3ecf37e53c6b6d:a7ZI3%24E%26Y01OUOBjwsH%23%24Zsaxb9iIBXJ@ep-mute-firefly-74914637-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        engine = create_engine(connection_url)
        print("   ✓ Connection created")

        # Test workitems query
        print("\n2. Testing workitems query...")
        query = "SELECT COUNT(*) as count FROM workitems WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
        result = pd.read_sql(query, engine)
        count = result['count'].iloc[0]
        print(f"   ✓ Found {count:,} work items")

        # Test time_entries query
        print("\n3. Testing time_entries query...")
        query = "SELECT COUNT(*) as count FROM time_entries WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
        result = pd.read_sql(query, engine)
        count = result['count'].iloc[0]
        print(f"   ✓ Found {count:,} time entries")

        # Test users query
        print("\n4. Testing users query...")
        query = "SELECT COUNT(*) as count FROM users"
        result = pd.read_sql(query, engine)
        count = result['count'].iloc[0]
        print(f"   ✓ Found {count:,} users")

        # Test work_types query
        print("\n5. Testing work_types query...")
        query = "SELECT id, name, color FROM work_types WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
        df = pd.read_sql(query, engine)
        print(f"   ✓ Found {len(df)} work types:")
        for _, row in df.iterrows():
            print(f"      - {row['name']} ({row['color']})")

        # Test priorities query (FIXED)
        print("\n6. Testing priorities query...")
        query = "SELECT id, name, color FROM priorities WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
        df = pd.read_sql(query, engine)
        print(f"   ✓ Found {len(df)} priorities:")
        for _, row in df.iterrows():
            print(f"      - {row['name']} ({row['color']})")

        # Test boards query
        print("\n7. Testing boards query...")
        query = "SELECT id, label FROM boards WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
        df = pd.read_sql(query, engine)
        print(f"   ✓ Found {len(df)} boards")

        # Test lanes query (FIXED)
        print("\n8. Testing lanes query...")
        query = "SELECT id, name, color FROM lanes WHERE organization_id = '33b4e799-b8aa-46cc-9d4d-73c915601515'"
        df = pd.read_sql(query, engine)
        print(f"   ✓ Found {len(df)} lanes:")
        for _, row in df.iterrows():
            print(f"      - {row['name']} ({row['color']})")

        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED!")
        print("=" * 80)
        print("\nYou can now run the dashboard with:")
        print("  ./run_dashboard.sh")
        print("or")
        print("  streamlit run streamlit_dashboard.py")
        print("")

        return True

    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ TEST FAILED!")
        print("=" * 80)
        print(f"\nError: {str(e)}")
        print("\nPlease check:")
        print("  1. Your internet connection")
        print("  2. The database is accessible")
        print("  3. All required packages are installed (pip install -r requirements.txt)")
        print("")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
