FROM mcr.microsoft.com/devcontainers/python:0-3.10

RUN apt-get update && apt-get install -y xz-utils lsof strace jq curl

RUN curl --proto '=https' --tlsv1.3 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

# ******************************************************
# * Anything after this point is run as a regular user *
# ******************************************************
USER vscode

RUN curl -sSL https://install.python-poetry.org | python - --version=1.3.1

# Configure Poetry to be in PATH
ENV PATH=$PATH:/home/vscode/.local/bin