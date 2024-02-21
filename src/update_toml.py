import toml
from github import Github
import os

def main():
    client = Github()
    repo = client.get_repo(os.environ["GITHUB_REPOSITORY"])
    contentfile = repo.get_contents("pyproject.toml")
    string_content = contentfile.decoded_content.decode("utf-8")
    print(f"FILE CONTENTS:\n* {string_content} \n*")
    toml_dict = toml.loads(string_content)
    dependencies_ = toml_dict['tool']['poetry']['dependencies']
    for lib in dependencies_:
        if lib.startswith("fake"):
            # if it has a pre-release=true flag, remove that flag
            if isinstance(dependencies_[lib], dict) and dependencies_[lib].get('allow-prereleases'):
                # del lib_details['allow-prereleases']  # this create dependencies.volttron-something as a new config entry
                # so use just version. Could switch to tomllib with python 3.11
                dependencies_[lib] = dependencies_[lib]["version"]

    print(f"updated toml dict {toml_dict}")
    repo.update_file("pyporoject.toml", "Auto updated to point to stable volttron releases",
                     toml.dump(toml_dict), contentfile.sha)


if __name__ == "__main__":
    main()
