# Virtual Environments

Projects that include both a `uv.lock` file and a `pyproject.toml` file use **uv** to manage their virtual environments automatically.  
These files ensure that all users of the repository share the same local development environment and package versions.


## Building or Resetting the Environment

To build or update the virtual environment, run: `uv sync`. This command will either:

- create the virtual environment if it does not already exist.

or 
- Rebuild or reset the existing environment so that it matches the exact versions specified in `uv.lock` and `pyproject.toml`.

This guarantees consistent environments across all users of the project.

## Updating Dependencies for the Whole Project

Only update `pyproject.toml` and `uv.lock `if everyone using the repository should receive the updated package versions. To add or update shared dependencies:

- Manually modify `pyproject.toml`. For example:
    - Add the new package or update its version.
    - For Git‑based dependencies, you might update the git commit SHA if the upstream code has changed.
- Regenerate the `uv.lock` file so the change is recorded: `uv lock --upgrade-package <package-name>`


This ensures all contributors will get the updated environment the next time they run `uv sync`.


## Activating the Virtual Environment in VS Code

You can activate the virtual environment in VS Code using one of the following methods:

**Option 1**: Select interpreter through the Command Palette

    Press `Ctrl + Shift + P` and search for Python: Select Interpreter.
    Choose the virtual environment from the list (both global and local venvs should appear).
    You may need to open a new terminal for the environment to activate.

**Option 2**: Activate manually in the terminal

    Run the appropriate activation command in the VS Code integrated terminal:
    `source venv/bin/activate`

    Replace 'venv' with the name of the environment directory if different.
