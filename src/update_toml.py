import toml
from github import Github
import os

def main():
    client = Github(os.environ["GITHUB_TOKEN"])
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
    try:
        result = repo.update_file("/pyporoject.toml", "Auto updated to point to stable volttron releases",
                         toml.dumps(toml_dict), contentfile.sha)
        print(f"Result of update : {result}")
    except Exception as e:
        print(f"Exception raised while updating {e}")
        raise e


if __name__ == "__main__":
    main()
