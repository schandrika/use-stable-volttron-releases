# Action to update volttron dependencies in main branch


Action to update any volttron-* dependency format

---
**From:**

  volttron-<xxx> = {version=">0.1.0rc0", allow-prereleases = true} 

**To:**
  
  volttron-<xxx> = ">0.1.0rc0"

---

This is used to update volttron dependencies when new changes(mostly from develop branch) are merged into main. 


## Example usage:
```
jobs:
  update-toml:
    runs-on: ubuntu-22.04
    steps:
      - name: update toml file
        uses: schandrika/use-stable-volttron-releases@main
        with:
          token: ${{ secrets.MY_PAT }}
```

**NOTE** This updates pyproject.toml and hence requires a github token that has write access to the repository