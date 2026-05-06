# GitHub tokens

Some repositories require adding a GitHub (GH) token to your development environment. This is typically needed when a Dockerfile must clone a **private GitHub repository** as part of the build process. Docker needs access to the private repository; otherwise the `git clone` command inside the container will fail. A Dockerfile may include an instruction like:

```bash
RUN --mount=type=secret,id=GH_TOKEN,env=GH_TOKEN \
    git config --global url."https://x-access-token:$GH_TOKEN@github.com/".insteadOf https://github.com/
```

This configuration allows Docker to authenticate using the GH token during the build.


## Creating and Adding a GitHub Token

Before starting, ensure the GitHub CLI (gh) is installed (globally) on your machine. This can be done by executing the command: `sudo apt install gh` in your preferred IDE terminal/CLI. 

To add a GitHub token to your development environment, follow the steps below:

1. Execute the command: `gh auth login` in the terminal. gh auth login. This will open an interactive authentication menu.
2. Select **GitHub.com** as the account you want to log into.
3. Select **HTTPS** as the protocol.
4. Choose **Login with a web browser**.
5. Copy the one‑time code shown in the terminal and press Enter. A GitHub login page should open automatically in your browser.
6. Log in with the GitHub account that has access to the private repository.
7. During login, create a new access token when prompted, and copy it.
8. Back in the terminal, configure Git authentication by executing: `gh auth setup-git`. This command usually produces no visible output.
9. Export your token to the environment by executing: `export GH_TOKEN=<insert_your_ghp_token>`. This makes the token available for Docker builds that expect `GH_TOKEN`.


**Important Notes**

- The export `GH_TOKEN=...` command only applies to the current terminal session. To persist the token across sessions, add the export command to your `~/.bashrc` or equivalent shell profile.

- Never commit tokens to version control.

- If your repository uses Docker secrets, ensure your build command includes:
    
    `--secret id=GH_TOKEN,env=GH_TOKEN`
    
    so the token is available during the build.
