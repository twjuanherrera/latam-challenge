import sys

def install_requirements(
    requirements_path: str = "../requirements.txt"
) -> None:
    """Installs Python libraries from the specified requirements file.

    Args:
        requirements_path (str, optional): Path to the requirements.txt file. Defaults to "../requirements.txt".

    Returns:
        None
    """
    import subprocess

    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path], check=True)
        print("Successfully installed libraries from requirements.txt")
    except subprocess.CalledProcessError as e:
        print(f"Error installing libraries: {e}")