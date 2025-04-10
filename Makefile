.PHONY: all venv install run clean

# Path to the virtual environment directory
VENV_DIR := venv
PYTHON := python3
PIP := $(VENV_DIR)/bin/pip
ACTIVATE := source $(VENV_DIR)/bin/activate

# Default target: set up environment and run
all: venv install run

# Create virtual environment if it doesn't exist
venv:
	@test -d $(VENV_DIR) || $(PYTHON) -m venv $(VENV_DIR)

# Install dependencies into the venv
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run the script inside the venv
run:
	$(ACTIVATE) && python ./src/main.py

# Clean up the venv
clean:
	rm -rf $(VENV_DIR)
