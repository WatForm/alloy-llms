.PHONY: setup reset-tools

setup:
	@echo "Running setup script..."
	@python ./scripts/setup.py

reset-tools:
	@echo "Clearing all files in ./tools/"
	@rm -f ./tools/* ./tools/.* 2>/dev/null || true