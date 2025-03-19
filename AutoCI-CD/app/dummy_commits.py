import os
import subprocess
import git
import random
from datetime import datetime, timedelta

# 🛠 Configure your GitHub repository path
REPO_PATH = r"C:\Users\SRILUCKY\OneDrive\Desktop\my_github_projects\AutoCI-CD-A-Scalable-GitHub-Actions-Pipeline"

# 🛠 Set the number of commits to create
NUM_COMMITS = input("Enter the number of dummy commits to create (default: 1000): ").strip()

if NUM_COMMITS == "":
    NUM_COMMITS = 1000  # Default value if the user presses Enter
else:
    NUM_COMMITS = int(NUM_COMMITS)

# 🛠 Set commit message options
COMMIT_MESSAGES = [
    "Refactored CI/CD pipeline for better performance",
    "Fixed bug in deployment script",
    "Updated Terraform configuration for AWS infrastructure",
    "Improved logging in Jenkins pipeline",
    "Added Kubernetes deployment manifests",
    "Enhanced Dockerfile for multi-stage builds",
    "Updated GitHub Actions workflow",
    "Optimized Ansible playbooks",
    "Fixed security vulnerability in CI pipeline",
    "Added monitoring with Prometheus and Grafana",
]

# 🛠 Set realistic file names and content
DEVOPS_FILES = {
    "Jenkinsfile": """
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'mvn clean package'
            }
        }
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f k8s/deployment.yaml'
            }
        }
    }
}
""",
    "deployment.yaml": """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: my-app
        image: my-app:latest
        ports:
        - containerPort: 8080
""",
    "main.tf": """
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
""",
    "Dockerfile": """
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
""",
    "github-actions.yml": """
name: CI/CD Pipeline
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
      - name: Run tests
        run: pytest
""",
    "ansible-playbook.yml": """
- hosts: all
  tasks:
    - name: Ensure Apache is installed
      apt:
        name: apache2
        state: present
""",
}

# 🛠 Set the time range for backdated commits
DAYS_BACK = input("Enter how many days back the commits should start (default: 1000): ").strip()

if DAYS_BACK == "":
    DAYS_BACK = 1000  # Default value if user presses Enter
else:
    DAYS_BACK = int(DAYS_BACK)  # Convert input to integer

base_date = datetime.now() - timedelta(days=DAYS_BACK)

# Change directory to the repo
os.chdir(REPO_PATH)

# Initialize the repo
repo = git.Repo(REPO_PATH)

def make_commit(commit_number):
    """Creates a dummy commit with a random backdated timestamp."""
    
    # Generate commit message
    commit_message = random.choice(COMMIT_MESSAGES)
    
    # Generate a random commit date within the chosen range
    commit_date = base_date + timedelta(days=random.randint(0, DAYS_BACK))
    formatted_date = commit_date.strftime("%Y-%m-%dT%H:%M:%S")
    
    # Choose a random DevOps file and its content
    filename, content = random.choice(list(DEVOPS_FILES.items()))
    
    # Write the content to the file
    with open(filename, "w") as f:
        f.write(content)
    
    # Stage the file
    repo.index.add([filename])
    
    # Commit with custom date
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = formatted_date
    env["GIT_COMMITTER_DATE"] = formatted_date

    subprocess.run(["git", "commit", "-m", commit_message], env=env, check=True)
    print(f"✅ Commit #{commit_number} created: '{commit_message}' on {formatted_date}")

# Loop to create multiple dummy commits
for i in range(1, NUM_COMMITS + 1):
    make_commit(i)

# Ask the user if they want to push the commits
push_choice = input("Do you want to push the commits to GitHub? (yes/no): ").strip().lower()

if push_choice == "yes":
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("🚀 All commits pushed successfully!")
else:
    print("🚀 Commits created locally but not pushed.")