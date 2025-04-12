# Effortlessly Sync Your Zotero Library with Overleaf: Streamline your academic writing workflow by automating citation exports and Overleaf updates!

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
OVERLEAF_REPO_PATH=/absolute/path/to/your/overleaf/repo (Local copy of your overleaf project)
EXPORT_FILENAME=your_export.bib (Chose a location where the .bib file should be stored in your overleaf project - the path needs to exist)
USERNAME=your_git_username (Optained in overleaf, usually it's just "git")
PASSWORD=your_git_password_or_token (Optained via Account Settings under: https://www.overleaf.com/user/settings)
```

> ⚠️ Do **not** commit your `.env` file. It contains sensitive credentials.

### 2.1 Clone the Overleaf Repository

If you haven't already cloned your Overleaf repository to your local machine, do so now:

```bash
git clone https://git.overleaf.com/your-overleaf-repo.git /absolute/path/to/your/overleaf/repo
```

Replace `/absolute/path/to/your/overleaf/repo` with the desired local path for your Overleaf repository. This path should match the value you set for `OVERLEAF_REPO_PATH` in the `.env` file.

### 2.2 Install and Configure Better BibTeX for Zotero

To enable the export functionality, you need to install and configure the Better BibTeX extension in Zotero:

1. Download and install Better BibTeX from [GitHub](https://github.com/retorquere/zotero-better-bibtex).
2. Open Zotero and navigate to `Tools > Add-ons`.
3. Click on the gear icon and select `Install Add-on From File...`.
4. Choose the downloaded `.xpi` file and follow the installation instructions.
5. Restart Zotero to activate the extension.
6. Configure Better BibTeX:
   - Go to `Edit > Preferences > Better BibTeX`.
   - Set up your citation key format and export preferences as needed.

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
