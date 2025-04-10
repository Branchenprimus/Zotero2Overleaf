# Project Setup and Usage

This repository contains a Python project with an automated setup using a `Makefile`. It includes a virtual environment, dependency management, and script execution.

## Requirements

Make sure you have the following installed on your system:

- Python 3 (`python3`)
- `make` (standard on Linux/macOS)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Branchenprimus/Zotero2Overleaf.git
```
```bash
cd Zotero2Overleaf
```

### 2. Create and Populate the `.env` File

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

Then open `.env` in a text editor and provide the required values:

```env
ZOTERO_API_URL=https://api.zotero.org/users/123456/items?format=bibtex
OVERLEAF_REPO_PATH=/absolute/path/to/your/overleaf/repo
EXPORT_FILENAME=your_export.bib
USERNAME=your_git_username
PASSWORD=your_git_password_or_token
```

> ⚠️ Do **not** commit your `.env` file. It contains sensitive credentials.

### 3. Run the Project

After filling out your `.env` file, run:

```bash
make
```

This will:

1. Create a Python virtual environment in `./venv` (if it doesn’t exist)
2. Activate the environment
3. Install dependencies from `requirements.txt`
4. Run the main script located in `./src/main.py`

## What the Script Does

The script automates the export and synchronization of a Zotero library with a linked Overleaf Git repository. It performs the following steps:

1. **Checks if Zotero is running** — Ensures the local Zotero client is active before attempting export.
2. **Exports the Zotero library** — Fetches a BibTeX export via the Zotero API and saves it to a file in the Overleaf project directory.
3. **Injects Git credentials** — Temporarily modifies the Git remote URL to include username and password for pushing to Overleaf.
4. **Performs Git operations**:
   - Pulls the latest changes
   - Adds the updated `.bib` file
   - Extracts and lists newly added citation keys
   - Commits and pushes changes to the Overleaf repository

## Additional Commands

- Re-run the script after initial setup:

  ```bash
  make run
  ```

- Clean up the virtual environment:

  ```bash
  make clean
  ```

## Notes

- This setup assumes a Unix-like environment (Linux or macOS).  
- For Windows users, you may need to run the steps manually or use WSL (Windows Subsystem for Linux).
