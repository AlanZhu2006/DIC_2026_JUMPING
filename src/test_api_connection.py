"""
API Connection Test Script

This script tests the API connections configured in api_config.json
"""

import json
import pathlib
import sys
from typing import Dict, Tuple

# Add parent directory to path to import gpt_request
sys.path.insert(0, str(pathlib.Path(__file__).parent))

try:
    from gpt_request import (
        request_claude_token,
        request_gemini_token,
        request_gpt41_token,
        cfg,
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure to run this script from the src/ directory")
    sys.exit(1)


def test_claude_api() -> Tuple[bool, str]:
    """Test Claude API connection"""
    print("\n[Testing] Claude API...")
    try:
        api_key = cfg("claude", "api_key")
        base_url = cfg("claude", "base_url")
        
        if not api_key or api_key == "..." or "YOUR_" in api_key:
            return False, "API key not configured (still placeholder)"
        
        if not base_url or base_url == "...":
            return False, "Base URL not configured (still '...')"
        
        # Simple test prompt
        test_prompt = "Say 'Hello' in one word."
        response, usage = request_claude_token(test_prompt, max_tokens=10)
        
        if response:
            return True, f"[SUCCESS] Response: {response[:50]}..."
        else:
            return False, "[ERROR] No response received"
            
    except Exception as e:
        return False, f"[ERROR] {str(e)}"


def test_gemini_api() -> Tuple[bool, str]:
    """Test Gemini API connection"""
    print("\n[Testing] Gemini API...")
    try:
        api_key = cfg("gemini", "api_key")
        base_url = cfg("gemini", "base_url")
        
        if not api_key or api_key == "..." or "YOUR_" in api_key:
            return False, "API key not configured (still placeholder)"
        
        if not base_url or base_url == "...":
            return False, "Base URL not configured (still '...')"
        
        # Simple test prompt
        test_prompt = "Say 'Hello' in one word."
        response, usage = request_gemini_token(test_prompt, max_tokens=10)
        
        if response:
            return True, f"[SUCCESS] Response: {response[:50]}..."
        else:
            return False, "[ERROR] No response received"
            
    except Exception as e:
        return False, f"[ERROR] {str(e)}"


def test_gpt41_api() -> Tuple[bool, str]:
    """Test GPT-4.1 API connection"""
    print("\n[Testing] GPT-4.1 API...")
    try:
        api_key = cfg("gpt41", "api_key")
        base_url = cfg("gpt41", "base_url")
        
        if not api_key or api_key == "..." or "YOUR_" in api_key:
            return False, "API key not configured (still placeholder)"
        
        if not base_url or base_url == "...":
            return False, "Base URL not configured (still '...')"
        
        # Simple test prompt
        test_prompt = "Say 'Hello' in one word."
        response, usage = request_gpt41_token(test_prompt, max_tokens=10)
        
        if response:
            return True, f"[SUCCESS] Response: {response[:50]}..."
        else:
            return False, "[ERROR] No response received"
            
    except Exception as e:
        return False, f"[ERROR] {str(e)}"


def test_iconfinder_api() -> Tuple[bool, str]:
    """Test IconFinder API connection (optional)"""
    print("\n[Testing] IconFinder API (optional)...")
    try:
        api_key = cfg("iconfinder", "api_key")
        
        if not api_key or api_key in ["...", "YOUR_ICONFINDER_KEY"] or "YOUR_" in api_key:
            return False, "[WARNING] API key not configured (optional, can skip)"
        
        # IconFinder doesn't need a full test, just check if key is set
        return True, "[OK] API key configured (not tested, IconFinder is optional)"
            
    except Exception as e:
        return False, f"[WARNING] Error: {str(e)} (IconFinder is optional)"


def check_config_file() -> Tuple[bool, Dict]:
    """Check if api_config.json exists and is valid"""
    config_path = pathlib.Path(__file__).parent / "api_config.json"
    
    if not config_path.exists():
        return False, {"error": f"api_config.json not found at {config_path}"}
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return True, config
    except json.JSONDecodeError as e:
        return False, {"error": f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return False, {"error": f"Error reading config: {str(e)}"}


def main():
    """Main test function"""
    import sys
    import io
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 60)
    print("API Connection Test - API Connection Test")
    print("=" * 60)
    
    # Check config file
    config_ok, config_data = check_config_file()
    if not config_ok:
        print(f"\n[ERROR] Config file error: {config_data.get('error')}")
        print("\nPlease ensure src/api_config.json exists and is valid JSON")
        return
    
    print("\n[OK] Config file found and valid")
    
    # Test results
    results = []
    
    # Test Claude (required for Planner and Coder)
    success, message = test_claude_api()
    results.append(("Claude API", success, message))
    
    # Test Gemini (required for Critic)
    success, message = test_gemini_api()
    results.append(("Gemini API", success, message))
    
    # Test GPT-4.1 (alternative LLM)
    success, message = test_gpt41_api()
    results.append(("GPT-4.1 API", success, message))
    
    # Test IconFinder (optional)
    success, message = test_iconfinder_api()
    results.append(("IconFinder API", success, message))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    required_apis = ["Claude API", "Gemini API"]
    optional_apis = ["GPT-4.1 API", "IconFinder API"]
    
    all_required_ok = True
    for name, success, message in results:
        status = "[OK]" if success else "[FAIL]"
        api_type = "Required" if name in required_apis else "Optional"
        print(f"\n{status} {name} ({api_type})")
        print(f"   {message}")
        if name in required_apis and not success:
            all_required_ok = False
    
    print("\n" + "=" * 60)
    if all_required_ok:
        print("[SUCCESS] All required APIs are working!")
    else:
        print("[FAIL] Some required APIs failed. Please check your configuration.")
        print("\nPlease edit src/api_config.json and set correct API keys")
    print("=" * 60)


if __name__ == "__main__":
    main()
