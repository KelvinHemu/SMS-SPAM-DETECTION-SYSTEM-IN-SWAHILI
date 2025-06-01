#!/usr/bin/env python3
"""
Spam Detection System Demo Launcher
Starts both backend and frontend for the two-party messaging demo
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("\n" + "="*60)
    print("🚀 SPAM DETECTION SYSTEM - TWO-PARTY MESSAGING DEMO")
    print("="*60)
    print("📱 SMS Interface + 🛡️ ML Spam Detection + 📊 Live Dashboard")
    print("="*60 + "\n")

def check_requirements():
    """Check if required dependencies are available"""
    print("🔍 Checking requirements...")
    
    # Check Python dependencies
    try:
        import uvicorn
        import fastapi
        print("✅ Backend dependencies found")
    except ImportError as e:
        print(f"❌ Missing backend dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Node.js not found")
        print("💡 Install Node.js 16+ from https://nodejs.org")
        return False
    
    # Check if frontend dependencies are installed
    frontend_dir = Path("frontend")
    node_modules = frontend_dir / "node_modules"
    
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], 
                          cwd=frontend_dir, 
                          check=True,
                          timeout=300)
            print("✅ Frontend dependencies installed")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return False
    else:
        print("✅ Frontend dependencies found")
    
    return True

def start_backend():
    """Start the FastAPI backend"""
    print("🔧 Starting backend API server...")
    try:
        # Start backend with updated port
        backend_cmd = [
            sys.executable, "main.py", 
            '--host', '0.0.0.0',
            '--port', '3000'
        ]
        
        backend_process = subprocess.Popen(backend_cmd, cwd=project_root)
        time.sleep(3)  # Give server time to start
        
        print("✅ Backend started successfully on http://localhost:3000")
        print("📄 API docs available at http://localhost:3000/docs")
        return backend_process
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the React frontend"""
    print("🎨 Starting frontend development server...")
    try:
        frontend_dir = Path("frontend")
        
        # Start React development server
        process = subprocess.Popen([
            'npm', 'start'
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("⏳ Waiting for frontend to start...")
        time.sleep(5)  # Give React time to start
        
        if process.poll() is None:
            print("✅ Frontend started successfully on http://localhost:3000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def monitor_process(process, name):
    """Monitor a process and print its output"""
    def read_output(pipe, prefix):
        for line in iter(pipe.readline, ''):
            print(f"[{prefix}] {line.rstrip()}")
    
    # Start threads to read stdout and stderr
    threading.Thread(target=read_output, args=(process.stdout, name), daemon=True).start()
    threading.Thread(target=read_output, args=(process.stderr, f"{name}-ERR"), daemon=True).start()

def main():
    """Main demo launcher"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Requirements check failed. Please fix the issues above.")
        sys.exit(1)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        backend_process = start_backend()
        if not backend_process:
            print("❌ Failed to start backend")
            sys.exit(1)
        
        # Start monitoring backend
        monitor_process(backend_process, "BACKEND")
        
        # Start frontend
        frontend_process = start_frontend()
        if not frontend_process:
            print("❌ Failed to start frontend")
            sys.exit(1)
        
        # Start monitoring frontend
        monitor_process(frontend_process, "FRONTEND")
        
        # Print success message
        print("\n" + "="*60)
        print("🎉 DEMO READY!")
        print("="*60)
        print("📱 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:3000")
        print("📚 API Docs: http://localhost:3000/docs")
        print("="*60)
        print("💡 Test the system by:")
        print("   1. Open http://localhost:3000 in your browser")
        print("   2. Use the SMS interface to send messages")
        print("   3. Try the quick test buttons for different scenarios")
        print("   4. Check the dashboard for real-time statistics")
        print("="*60)
        print("⏹️  Press Ctrl+C to stop both servers")
        print("="*60 + "\n")
        
        # Wait for processes to finish or be interrupted
        try:
            while True:
                if backend_process.poll() is not None:
                    print("⚠️ Backend process stopped")
                    break
                if frontend_process.poll() is not None:
                    print("⚠️ Frontend process stopped")
                    break
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ Shutting down demo...")
    
    except KeyboardInterrupt:
        print("\n⏹️ Shutting down demo...")
    
    finally:
        # Clean up processes
        if backend_process and backend_process.poll() is None:
            print("🔧 Stopping backend...")
            backend_process.terminate()
            try:
                backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                backend_process.kill()
        
        if frontend_process and frontend_process.poll() is None:
            print("🎨 Stopping frontend...")
            frontend_process.terminate()
            try:
                frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                frontend_process.kill()
        
        print("✅ Demo stopped successfully")

if __name__ == "__main__":
    main() 