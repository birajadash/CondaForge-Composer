import os
import zipfile
import subprocess
import json

def unzip_starter_project_repo(zip_path, project_folder):
    """
    Unzips the selected package into a new project folder.

    Args:
        zip_path (str): Path to the zip file.
        project_folder (str): Path to the project folder where the zip file should be extracted.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(project_folder)

    print(f"Project unzipped into: {project_folder}")

# Call the function
unzip_starter_project_repo('C:\Users\basan\Downloads\langchain_crash_course.zip', 'C:\Users\basan\Desktop\00_PythonWIP\Team Project\trial automation2')

# Rest of your code follows here...

def list_conda_envs():
    """
    List all existing conda environments.

    Returns:
        list: The list of existing conda environments.
    """
    envs = subprocess.check_output(['conda', 'env', 'list', '--json'])
    envs_json = json.loads(envs)
    return [os.path.basename(env) for env in envs_json['envs']]

def list_env_packages(env_name):
    """
    List all packages installed in a conda environment.

    Args:
        env_name (str): The name of the conda environment.

    Returns:
        list: The list of packages installed in the environment.
    """
    try:
        packages = subprocess.check_output(['conda', 'list', '--json', '-n', env_name])
        packages_json = json.loads(packages)
        return [package['name'] for package in packages_json]
    except subprocess.CalledProcessError:
        print(f"Error: Failed to list packages for environment '{env_name}'. Make sure this environment exists.")
        return []

def read_requirements(requirements_path):
    """
    Read a 'requirements.txt' file.

    Args:
        requirements_path (str): The path to the 'requirements.txt' file.

    Returns:
        list: The list of packages listed in the file.
    """
    with open(requirements_path, 'r') as f:
        return [line.strip() for line in f]

def create_conda_env(env_name, requirements_path):
    """
    Create a new conda environment and install the packages listed in a 'requirements.txt' file.

    Args:
        env_name (str): The name of the new conda environment.
        requirements_path (str): The path to the 'requirements.txt' file.
    """
    try:
        # Create the new conda environment
        subprocess.check_call(['conda', 'create', '-n', env_name, '--yes'])

        # Install the packages listed in the 'requirements.txt' file
        requirements = read_requirements(requirements_path)
        for package in requirements:
            try:
                subprocess.check_call(['conda', 'install', '-n', env_name, package, '--yes'])
            except subprocess.CalledProcessError:
                print(f"Failed to install {package} with conda. Trying with pip...")
                subprocess.check_call(['conda', 'run', '-n', env_name, 'pip', 'install', package])
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to create environment '{env_name}' or install packages. {e}")

# The path to the 'requirements.txt' file
requirements_path = r'C:/Users/basan/Desktop/00_PythonWIP/Team Project/trial automation2/langchain_crash_course/requirements.txt'

# Read the 'requirements.txt' file
requirements = read_requirements(requirements_path)

# List all existing conda environments
envs = list_conda_envs()

matching_envs = []

for env in envs:
    print(f"Environment: {env}")

    # List all packages installed in the environment
    packages = list_env_packages(env)

    print(f"Packages installed in {env}:")
    for package in packages:
        print(f"  - {package}")

    # Compare the packages installed in the environment with the packages listed in the 'requirements.txt' file
    missing_packages = [package for package in requirements if package not in packages]

    if missing_packages:
        print(f"The following packages are listed in '{requirements_path}' but not installed in the '{env}' environment: {', '.join(missing_packages)}")
    else:
        matching_envs.append(env)

    print()

# Print the environments that match the requirements
if matching_envs:
    print(f"The following environments match the requirements: {', '.join(matching_envs)}")
else:
    print("No existing environment matches the requirements. Creating a new environment...")
    create_conda_env('new_env', requirements_path)