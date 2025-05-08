import subprocess
import os

# Function to run a shell command and return the output
def run_command(command, cwd=None):
    try:
        result = subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Output: {e.output}")
        raise

# URLs for the parent repository and submodule (replace these with your actual URLs)
parent_repo_url = "https://github.com/Bapuji-patta/testing"
submodule_url = "git@github.com:Bapuji-patta/testing.git"

# Path where you want to clone the repositories (adjust as needed)
parent_repo_path = os.path.join(os.getcwd(), "parent_repo")  # Directory for the parent repository
submodule_path = os.path.join(parent_repo_path, "testing")  # Submodule path inside the parent repository

# Function to clone the parent repository if it doesn't exist
def clone_parent_repo():
    if not os.path.exists(parent_repo_path):
        print(f"Cloning parent repository from {parent_repo_url}...")
        run_command(['git', 'clone', parent_repo_url, parent_repo_path])

    print("Initializing and updating submodules...")
    run_command(['git', 'submodule', 'update', '--init', '--recursive'], cwd=parent_repo_path)

# Function to clone the submodule if it doesn't exist
def clone_submodule():
    if not os.path.exists(submodule_path):
        print(f"Cloning submodule from {submodule_url}...")
        os.makedirs(submodule_path, exist_ok=True)
        run_command(['git', 'clone', submodule_url, submodule_path])

# Function to commit the parent repository changes
def commit_parent_changes():
    print("Committing changes in the parent repository...")

    # Check if submodule reference has changed (using git submodule status)
    submodule_status = run_command(['git', 'submodule', 'status'], cwd=parent_repo_path)
    if submodule_status:
        # The submodule reference has changed, stage the submodule reference
        print(f"Submodule status: {submodule_status}")
        run_command(['git', 'add', submodule_path], cwd=parent_repo_path)
        
        # Check if there are any staged changes in the parent repository
        status = run_command(['git', 'status', '--porcelain'], cwd=parent_repo_path)
        
        if status:  # If there are any changes staged
            # Commit the changes in the parent repository
            run_command(['git', 'commit', '-m', 'Updated submodule reference'], cwd=parent_repo_path)
            
            # Push the changes in the parent repository
            run_command(['git', 'push'], cwd=parent_repo_path)
        else:
            print("No changes detected in the parent repository.")
    else:
        print("No submodule reference changes detected.")

# Function to commit changes in the submodule
def commit_submodule_changes():
    print("Checking for changes in the submodule...")

    if os.path.exists(submodule_path):
        # Ensure the submodule is not in a detached HEAD state
        branch_check = run_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=submodule_path)
        if branch_check == 'HEAD':
            print("Submodule is in a detached HEAD state. Checking out the default branch...")
            run_command(['git', 'checkout', 'main'], cwd=submodule_path)  # Or 'master', or your default branch

        # Check for changes in the submodule
        changes = run_command(['git', 'status', '--porcelain'], cwd=submodule_path)
        
        if changes:
            print("Changes detected in submodule. Committing...")

            # Add all changes in the submodule
            run_command(['git', 'add', '.'], cwd=submodule_path)
            
            # Commit the changes in the submodule
            run_command(['git', 'commit', '-m', 'Automated commit from parent repo'], cwd=submodule_path)
            
            # Push the changes in the submodule
            run_command(['git', 'push'], cwd=submodule_path)
        else:
            print("No changes in the submodule.")
    else:
        print(f"Submodule path '{submodule_path}' does not exist.")

if __name__ == "__main__":
    # Clone the repositories if they don't exist
    clone_parent_repo()
    clone_submodule()

    # First, commit changes in the parent repository (including submodule reference)
    commit_parent_changes()

    # Then, commit changes in the submodule (if any)
    commit_submodule_changes()

    print("Parent repository and submodule commits completed successfully.")
