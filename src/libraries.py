from importlib.machinery import ModuleSpec
import sys  # Import system-specific parameters and functions

def check_requirements(
        requirements_path: str = "../requirements.txt"  # Default path to requirements file
) -> bool:
    """Checks if the required libraries are already installed.

    Args:
        requirements_path (str, optional): Path to the requirements.txt file.

    Returns:
        bool: True if all required libraries are installed, False otherwise.
    """

    import importlib.util  # Module for loading module specifications

    try:
        # Read the requirements from the specified file
        with open(requirements_path, "r") as file:
            requirements: list[str] = [line.strip() for line in file if line.strip()]  # Remove empty lines

        for requirement in requirements:
            spec: ModuleSpec = importlib.util.find_spec(requirement)  # Attempt to find the module
            if spec is None:
                return False  # Indicate missing library

        return True  # All libraries are found

    except FileNotFoundError:
        print(f"Requirements file not found at: {requirements_path}")
        return False

def install_requirements(
    requirements_path: str = "../requirements.txt"  # Default path to requirements file
) -> None:
    """Installs Python libraries from the specified requirements file.

    Args:
        requirements_path (str, optional): Path to the requirements.txt file.

    Returns:
        None
    """

    import subprocess  # Module for executing external processes

    try:
        # Check if all required libraries are already installed
        if not check_requirements(requirements_path):
            # Install missing libraries using pip
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path], check=True)
            print("Successfully installed libraries from requirements.txt")
        else:
            print("All required libraries are already installed.")

    except subprocess.CalledProcessError as e:
        print(f"Error installing libraries: {e}")
    except Exception as e:
        print(f"Unexpected error in libraries.py: {e}")
