import os
import sys
from git import Repo

def clone_and_scan(repo_url):
    github_token = os.getenv('GITHUB_TOKEN')
    
    if not github_token:
        print("Error: GITHUB_TOKEN is not set.")
        return

    auth_repo_url = repo_url.replace("https://github.com/", f"https://{github_token}@github.com/")
    
    if repo_url.endswith('.git'):
        repo_name = repo_url.split('/')[-1].replace('.git', '')
    else:
        repo_name = repo_url.split('/')[-1]

    try:
        Repo.clone_from(auth_repo_url, repo_name)
        print(f"Successfully cloned {repo_url} into {repo_name} dev branch")
    except Exception as e:
        print(f"Error cloning the repository: {e}")
        return

    os.chdir(repo_name)

    try:
        os.system("detect-secrets scan > .secrets.baseline")
        print("Successfully ran detect-secrets scan")

        result_file = f"../{repo_name}-result.txt"
        
        
        audit_command = "yes s | detect-secrets audit .secrets.baseline"
        audit_output = os.popen(audit_command).read()
        
       
        if "What would you like to do? (s)kip, (b)ack, (q)uit:" in audit_output:
            # If the prompt is found, simulate pressing 's'
            os.system(f"yes s | detect-secrets audit .secrets.baseline | tee {result_file}")
            print(f"Successfully ran detect-secrets audit with 's' and saved to {result_file}")
        else:
            # Otherwise, simulate pressing 'y'
            os.system(f"yes y | detect-secrets audit .secrets.baseline | tee {result_file}")
            print(f"Successfully ran detect-secrets audit with 'y' and saved to {result_file}")
    except Exception as e:
        print(f"Error running detect-secrets command: {e}")
    finally:
        os.chdir("..")

def main():
    if not os.path.isfile('link.txt'):
        print("Error: link.txt file not found.")
        sys.exit(1)
    
    with open('link.txt', 'r') as file:
        repo_urls = [line.strip() for line in file if line.strip()]

    for repo_url in repo_urls:
        clone_and_scan(repo_url)

if __name__ == "__main__":
    main()
