#!/usr/bin/env python3
"""
Test script to verify the MCP server works correctly.
"""

import subprocess
import sys
import time
import signal
import os

def test_server():
    """Test if the server starts without errors."""
    print("Testing MCP server startup...")
    
    # Start the server process
    env = os.environ.copy()
    env["PATH"] = f"{os.path.expanduser('~/.local/bin')}:{env.get('PATH', '')}"
    
    try:
        process = subprocess.Popen(
            ["uv", "run", "weather_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        
        # Wait a moment for startup
        time.sleep(2)
        
        # Check if process is still running (good sign)
        if process.poll() is None:
            print("✅ Server started successfully!")
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Server failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return False
            
    except FileNotFoundError:
        print("❌ uv command not found. Make sure uv is installed and in PATH.")
        return False
    except Exception as e:
        print(f"❌ Error testing server: {e}")
        return False

if __name__ == "__main__":
    if test_server():
        print("\n🎉 Your MCP server is ready!")
        print("\nNext steps:")
        print("1. Configure Claude Desktop to use this server")
        print("2. Test with queries like 'What's the weather in Sacramento?'")
        sys.exit(0)
    else:
        print("\n❌ Server test failed. Check the error messages above.")
        sys.exit(1)
