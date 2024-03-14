import os
import toml
from github import Github


def main():
    client = Github(os.environ["GITHUB_TOKEN"])
    repo = client.get_repo(os.environ["GITHUB_REPOSITORY"])
    print(f"repo is {repo}")
    contentfile = repo.get_contents("pyproject.toml")
    string_content = contentfile.decoded_content.decode("utf-8")
    print(f"GOT token {os.environ['GITHUB_TOKEN']}")
    toml_dict = toml.loads(string_content)
    dependencies_ = toml_dict['tool']['poetry']['dependencies']
    for lib in dependencies_:
        if lib.startswith("volttron"):
            # if it has a pre-release=true flag, remove that flag
            if isinstance(dependencies_[lib], dict) and dependencies_[lib].get('allow-prereleases'):
                # del lib_details['allow-prereleases']  # this create dependencies.volttron-<xx> as a new config entry
                # i.e. toml library doesn't handle nested dict well. so for now use just version.
                # this should be okay for now as we don't use anything other than version and allow-prereleases for
                # volttron dependencies
                # Could switch to tomllib with python 3.11
                dependencies_[lib] = dependencies_[lib]["version"]

    try:
        result = repo.update_file("pyproject.toml", "Auto updated to point to stable volttron releases",
                         toml.dumps(toml_dict), contentfile.sha)
        print(f"Result of update : {result}")
    except Exception as e:
        print(f"Exception raised while updating {e}")
        raise e


if __name__ == "__main__":
    main()
