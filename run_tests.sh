#!/bin/bash

echo "Running ISS API tests..."

python -m pytest tests/ -v
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "All tests passed"
else
    echo "Tests failed"
fi

exit $EXIT_CODE
