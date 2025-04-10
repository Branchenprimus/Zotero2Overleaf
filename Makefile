.PHONY: all venv install run clean check_env

# Path to the virtual environment directory
VENV_DIR := venv
PYTHON := python3
PIP := $(VENV_DIR)/bin/pip
ACTIVATE := source $(VENV_DIR)/bin/activate
DEACTIVATE := deactivate

# Default target: set up environment and run
all: venv install check_env

# Create virtual environment if it doesn't exist
venv:
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)

# Install dependencies into the venv
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Check for .env file
check_env:
	@if [ ! -f .env ]; then \
		echo "❌  .env file not found."; \
		echo "➡️  Please create one using: cp .env.example .env"; \
		echo "➡️  Then edit .env, populate the required environment variables and execute: "make run""; \
		exit 1; \
	fi

# Run the script inside the venv
run:
	$(ACTIVATE) && python ./src/main.py && $(DEACTIVATE)

# Clean up the venv
clean:
	rm -rf $(VENV_DIR)
