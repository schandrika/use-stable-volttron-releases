import toml
from github import Github
import os

def main():
    print(os.listdir(os.environ["PWD"]))
    client = Github()
    repo = client.get_repo(os.environ["GITHUB_REPOSITORY"])
    f = repo.get_contents("pyproject.toml")
    #with open('pyproject.toml', 'r') as f:
    toml_dict = toml.loads(f)
    dependencies_ = toml_dict['tool']['poetry']['dependencies']
    for lib in dependencies_:
        if lib.startswith("fake"):
            # if it has a pre-release=true flag, remove that flag
            if isinstance(dependencies_[lib], dict) and dependencies_[lib].get('allow-prereleases'):
                # del lib_details['allow-prereleases']  # this create dependencies.volttron-something as a new config entry
                # so use just version. Could switch to tomllib with python 3.11
                dependencies_[lib] = dependencies_[lib]["version"]

    with open('new_toml_file.toml', 'w') as f:
        toml.dump(toml_dict, f)


if __name__ == "__main__":
    main()
