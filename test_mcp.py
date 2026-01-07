#!/usr/bin/env python3
"""Test script for MCP server functionality."""

import sys
import json

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import mcp
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        from mcp.types import Tool, TextContent
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_dependencies():
    """Test that ML dependencies are available."""
    print("\nTesting ML dependencies...")
    dependencies = {}
    try:
        import numpy
        dependencies['numpy'] = numpy.__version__
        print(f"✓ NumPy {numpy.__version__}")
    except ImportError:
        print("✗ NumPy not available")
        return False
    
    try:
        import pandas
        dependencies['pandas'] = pandas.__version__
        print(f"✓ Pandas {pandas.__version__}")
    except ImportError:
        print("✗ Pandas not available")
        return False
    
    try:
        import sklearn
        dependencies['scikit-learn'] = sklearn.__version__
        print(f"✓ Scikit-learn {sklearn.__version__}")
    except ImportError:
        print("✗ Scikit-learn not available")
        return False
    
    return True

def test_server_structure():
    """Test that the MCP server script is properly structured."""
    print("\nTesting MCP server structure...")
    try:
        with open('mcp_server.py', 'r') as f:
            content = f.read()
            
        # Check for required components
        checks = [
            ('Server instance', 'Server("ml-operations")' in content),
            ('list_tools decorator', '@app.list_tools()' in content),
            ('call_tool decorator', '@app.call_tool()' in content),
            ('get_ml_info tool', '"get_ml_info"' in content),
            ('check_dependencies tool', '"check_dependencies"' in content),
        ]
        
        all_passed = True
        for name, result in checks:
            if result:
                print(f"✓ {name} found")
            else:
                print(f"✗ {name} not found")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"✗ Failed to read server file: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("MCP Agent Installation Test")
    print("=" * 60)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Server Structure", test_server_structure()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ MCP Agent installation is complete and functional!")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
