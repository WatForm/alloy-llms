# alloy-llms
Investigation into how well LLMs can understand and produce Alloy models

## Instructions:

### Setup

Run the following:

```
git clone https://github.com/nancyday/alloy-llms
cd ./alloy-llms
make setup
```

This downloads the latest `.jar` files for Alloy 5 and Alloy 6 (using curl) and stores them in `./tools`. They can be removed with `make reset-tools`.

### Checking validity of models:

Run the following:
```
python ./scripts/check_validity.py ./tests/test_models/basic.als 
```

Replace `./tests/test_models/basic.als` with the path to any file to check validity.

