.PHONY: syntax-test

# Default line length limit is 79
syntax-test:
	flake8 --verbose --show-source --max-line-length=120 .
