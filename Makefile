.PHONY: all venv install run clean check_env

# Path to the virtual environment directory
VENV_DIR := venv
PYTHON := python3
PIP := $(VENV_DIR)/bin/pip
ACTIVATE := source $(VENV_DIR)/bin/activate
DEACTIVATE := deactivate

# Default target: set up environment and run
all: check_env venv install run

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

# Run the script inside the venv
run: check_env
	$(ACTIVATE) && python ./src/main.py && $(DEACTIVATE)

# Clean up the venv
clean:
	rm -rf $(VENV_DIR)
