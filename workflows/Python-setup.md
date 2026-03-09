# Setting up Python in VSCode 

[Download][download_python_link] and install Python to your local or virtual machine.

**Note:** Some projects or dependencies may require specific versions of Python. If multiple versions are needed, each one must be installed separately and added to your system path.  VS Code can then be configured to use the correct Python interpreter for your project.


# Python extensions for VS Code

After installing Python on your machine, install the Python‑related extensions in VS Code.  
VS Code will automatically detect the Python versions installed on your system.

See `VSCode_setup.md` for detailed instructions on how to install extensions.

Required extensions:

- **Python**
- **Python Environments**

These enable linting, environment selection, interpreter discovery, and basic Python tooling. Python files can be written without these extensions, but these extensions are required to run and debug with Python in VS Code.


# Using Jupyter in VS Code

To work with Jupyter notebooks (`.ipynb`) in VS Code:

1. Install the **Jupyter** extension in VS Code.
2. Install Jupyter into your active development environment by executing in the VS Code integrated terminal:

   ```bash
   pip install jupyter
   ```


## Virtual Environments and Jupyter

It is recommended to install tools like Jupyter inside a **virtual environment** rather than globally. If you have an existing .venv, activate it and install Jupyter inside it by executing the following commands in the VS Code integrated terminal:

1. source .venv/bin.activate
2. `pip install Jupyter`


**Important note on uv sync**

Running `uv sync` overwrites your virtual environment to match the `pyproject.toml`.
If you manually install a package with pip install and it is not listed in `pyproject.toml`, it may be removed the next time `uv sync` runs.
To avoid repeatedly reinstalling Jupyter:

- **Option A** (global): Add jupyter to `pyproject.toml`.
- **Option B** (recommended): Create a lightweight extra virtual environment just for notebook testing.

Option B is safer when other developers sharing the repo do not need Jupyter or extra packages.
See `virtual_environments.md` for more details on uv sync and environment version control.


## Kernels

When running a Jupyter notebook in VS Code, you must select a kernel that corresponds to the environment where Jupyter is installed.
If your main project environment includes heavy dependencies, restarting the kernel can be slow.
In this case, creating a lightweight environment specifically for notebook testing can greatly speed up your workflow.

**Creating a lightweight Jupyter kernel**

1. Create a new virtual environment:`python3 -m venv light-env`
2. Activate the new virtual environment: `source light-env/bin/activate`
3. Install only the minimal packages needed: `pip install ipykernel numpy polars`
4. Register the new environment as a new Jupyter kernel: `python -m ipykernel install --user --name light-env --display-name "Lightweight Python"`
5. In your Jupyter notebook, select the new "Lightweight Python" kernel in the top-right corner.
 
This gives you a fast, easily resettable kernel suitable for experimentation and testing.


# Hyperlinks

[download_python_link]: https://www.python.org/downloads/