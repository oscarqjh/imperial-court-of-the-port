#!/usr/bin/env python3
"""
Test script to verify database connection and agent tools functionality
"""

import asyncio
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

async def test_database_connection():
    """Test basic database connectivity"""
    try:
        from app.db import get_engine, get_session_factory
        from sqlalchemy import text
        
        print("🔧 Testing database engine creation...")
        engine = get_engine()
        print("✅ Engine created successfully")
        
        print("🔧 Testing session factory creation...")
        session_factory = get_session_factory()
        print("✅ Session factory created successfully")
        
        print("🔧 Testing database connection...")
        async with session_factory() as session:
            result = await session.execute(text("SELECT 1 as test_col"))
            row = result.scalar()
            if row == 1:
                print("✅ Database connection successful")
                return True
            else:
                print("❌ Database connection failed: unexpected result")
                return False
                
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        print(f"📊 Full traceback: {traceback.format_exc()}")
        return False

async def test_agent_tools():
    """Test agent tools functionality"""
    try:
        from app.agent_tools import AgentDatabaseTools
        
        print("\n🤖 Testing agent tools...")
        
        tools = AgentDatabaseTools()
        
        # Test system health check
        print("🔧 Testing system health check...")
        health_result = await AgentDatabaseTools.check_system_health()
        
        if isinstance(health_result, dict) and "error" not in health_result:
            print("✅ System health check successful")
            print(f"📊 Result keys: {list(health_result.keys())}")
            return True
        else:
            print(f"❌ System health check failed: {health_result}")
            return False
            
    except Exception as e:
        print(f"❌ Agent tools test failed: {e}")
        import traceback
        print(f"📊 Full traceback: {traceback.format_exc()}")
        return False

def test_sync_wrapper():
    """Test sync wrapper functionality"""
    try:
        from app.agent_tools import AgentDatabaseTools
        
        print("\n🔄 Testing sync wrapper...")
        
        # This should work without async context
        result = AgentDatabaseTools.check_system_health()
        
        if isinstance(result, dict) and "error" not in result:
            print("✅ Sync wrapper test successful")
            print(f"📊 Result keys: {list(result.keys())}")
            return True
        else:
            print(f"❌ Sync wrapper test failed: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Sync wrapper test failed: {e}")
        import traceback
        print(f"📊 Full traceback: {traceback.format_exc()}")
        return False

async def main():
    """Main test function"""
    print("🧪 Starting database and agent tools testing...\n")
    
    # Test 1: Database connection
    db_success = await test_database_connection()
    
    # Test 2: Agent tools (async)
    tools_success = await test_agent_tools() if db_success else False
    
    # Test 3: Sync wrapper
    sync_success = test_sync_wrapper() if db_success else False
    
    print(f"\n📋 Test Results:")
    print(f"   Database Connection: {'✅ PASS' if db_success else '❌ FAIL'}")
    print(f"   Agent Tools (async): {'✅ PASS' if tools_success else '❌ FAIL'}")
    print(f"   Sync Wrapper:       {'✅ PASS' if sync_success else '❌ FAIL'}")
    
    if db_success and tools_success and sync_success:
        print("\n🎉 All tests passed! Your agent tools should work correctly.")
        return True
    else:
        print("\n❌ Some tests failed. Please check the error messages above.")
        if not db_success:
            print("💡 Try running 'python install_missing_deps.py' first to install missing dependencies.")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        print(f"📊 Full traceback: {traceback.format_exc()}")
        sys.exit(1)
