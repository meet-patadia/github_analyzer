import requests
import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {token}"
}

def get_repo_info(repo_url):
    # Convert URL to API format
    parts = repo_url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]
    base_url = f"https://api.github.com/repos/{owner}/{repo}"

    # Basic info
    data = requests.get(base_url, headers=headers).json()
    print("=" * 40)
    print("REPO:", data["full_name"])
    print("Description:", data["description"])
    print("=" * 40)

    # Languages
    languages = requests.get(f"{base_url}/languages", headers=headers).json()
    print("\nLANGUAGES USED:")
    for language, bytes_written in languages.items():
        print(f"  - {language}: {bytes_written:,} bytes")
    
      # Number of files
    tree = requests.get(f"{base_url}/git/trees/HEAD?recursive=1", headers=headers).json()
    files = [item for item in tree["tree"] if item["type"] == "blob"]
    print(f"\nNUMBER OF FILES: {len(files)}")

    # Largest files
    sorted_files = sorted(files, key=lambda x: x.get("size", 0), reverse=True)
    print("\nLARGEST FILES:")
    for file in sorted_files[:5]:
        size_kb = file.get("size", 0) / 1024
        print(f"  - {file['path']} ({size_kb:.1f} KB)")

    # Dependency count
    dependency_files = {
        "package.json": "JavaScript/Node",
        "requirements.txt": "Python",
        "Pipfile": "Python",
        "go.mod": "Go",
        "pom.xml": "Java",
    }

    print("\nDEPENDENCIES:")
    found_any = False

    for dep_file, language in dependency_files.items():
        match = next((f for f in files if f["path"].endswith(dep_file)), None)
        if match:
            found_any = True
            file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{match['path']}"
            content = requests.get(file_url, headers=headers).text

            if dep_file == "package.json":
                pkg = json.loads(content)
                deps = len(pkg.get("dependencies", {}))
                dev_deps = len(pkg.get("devDependencies", {}))
                print(f"  - {dep_file} ({language}): {deps} dependencies, {dev_deps} dev dependencies")

            elif dep_file == "requirements.txt":
                lines = [l for l in content.splitlines() if l and not l.startswith("#")]
                print(f"  - {dep_file} ({language}): {len(lines)} dependencies")

    if not found_any:
        print("  - No known dependency files found")

if len(sys.argv) < 2:
    print("Usage: python analyzer.py <github-repo-url>")
else:
    get_repo_info(sys.argv[1])
