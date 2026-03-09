# FDRI Development Environment Documentation

The documentation in this folder is designed to assist users working with UKCEH's FDRI GitHub repositories. 

**IDE:** The documentation in this folder is specific to **VS Code**, though some principles will be portable to other IDEs.

**Operating System:** All commands referenced in this documentation are written for **Linux** environments.

**Rendering**: Use `Ctl + Shift + V` to render the `.md` files in VS Code.

## Documents in this folder

Each `.md` file is written as standalone documentation, but if you're new to the repository we suggest reading them in the following order:

1. **VMWare-Setup-Guide.md**: Installing and configuring a virtual machine using VMWare.

2. **VSCode_setup.md**: Explains how to install and setup VSCode for FDRI projects. Includes recommended extensions/packages for FDRI projects and how to install them. 

3. **virtual_environments.md**: Explains how to create consistent virtual environments across users working within the same repository. Includes recommended best practices for managing development environments.

4. **Python_setup.md**: Covers how to configure Python in VS Code, including required extensions, using Jupyter inside VS Code, and creating new Python environments and kernels for testing.

5. **debugging_setup.md**: Describes how to configure debugging for projects in VS Code. Covers both simple debugging of individual scripts and more complex debugging workflows involving multiple files or pipelines.

6. **GH_tokens.md**: Explains how to create and add a GitHub token to your development environment.
Especially useful when working with Dockerfiles that need to clone private repositories during builds.

