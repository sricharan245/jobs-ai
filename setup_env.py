import os
import subprocess
import sys
import platform

def main():
    # Step 1: Create the virtual environment
    venv_name = "jobsai-env"
    python_executable = sys.executable  # Path to the current Python interpreter
    if not os.path.exists(venv_name):
        print(f"Creating virtual environment: {venv_name}")
        subprocess.run([python_executable, "-m", "venv", venv_name])
    else:
        print(f"Virtual environment {venv_name} already exists.")

    # Step 2: Install dependencies from requirements.txt
    pip_executable = os.path.join(
        venv_name, "bin", "pip") if platform.system() != "Windows" else os.path.join(venv_name, "Scripts", "pip")
    
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print(f"Installing dependencies from {requirements_file}...")
        subprocess.run([pip_executable, "install", "-r", requirements_file])
    else:
        print(f"{requirements_file} not found. Skipping dependency installation.")

    # Step 3: Provide instructions to activate the environment
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_name, "Scripts", "activate.bat")
        print(f"To activate the virtual environment, run:\n{activate_script}")
    else:
        activate_script = os.path.join(venv_name, "bin", "activate")
        print(f"To activate the virtual environment, run:\nsource {activate_script}")

    print("Setup completed.")

if __name__ == "__main__":
    main()
