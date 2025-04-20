.PHONY: all venv install run clean check_env check_bib_health

# Path to the virtual environment directory
VENV_DIR := venv
PYTHON := python3
PIP := $(VENV_DIR)/bin/pip
ACTIVATE := source $(VENV_DIR)/bin/activate
DEACTIVATE := deactivate

# Default target: set up environment and run
all: check_env venv install run check_bib_health

# Create virtual environment if it doesn't exist
venv:
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)

# Install dependencies into the venv
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Check for .env file
check_env:
	@if [ -f .env ]; then \
		echo "✅  .env file found."; \
	else \
		echo "❌  .env file not found."; \
		echo "➡️  Creating .env file from .env.example."; \
		cp .env.example .env; \
		echo "➡️  Please edit .env, populate the required environment variables and execute: \"make run\""; \
	fi

# Run the sync script inside the venv
run: check_env venv
	@echo "Running Zotero2Overleaf Sync..."
	$(ACTIVATE) && python ./src/sync_zotero_2_overleaf.py && $(DEACTIVATE)

# Clean up the venv
clean:
	rm -rf $(VENV_DIR)

# Check BibTeX health after sync
check_bib_health: venv
	@echo "Running BibTeX APA Health Check..."
	$(ACTIVATE) && \
	bibfile_path=$$(grep '^OVERLEAF_REPO_PATH=' .env | cut -d'=' -f2 | tr -d '"') && \
	echo "Checking BibTeX file at: $$bibfile_path" && \
	python ./src/check_bib_health.py "$$bibfile_path" && \
	echo "✅ BibTeX health check passed!" || \
	( echo "❌ BibTeX health check failed!" && $(DEACTIVATE) && exit 1 )
	$(DEACTIVATE)
