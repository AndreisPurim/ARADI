#!/bin/bash

# Function to create a virtual environment and run black and flake8
function format_code() {
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo "Created formatting virtual environment."
    fi

    source venv/bin/activate
    pip install black flake8
    black ./pyaradi
    flake8 ./pyaradi
    deactivate
}

# Function to create release package, check, and sign files
function create_dist() {
    python3 setup.py sdist
    python3 setup.py bdist_wheel
    # Sign everything except files that end with .asc
    for file in dist/*; do
        if [[ "$file" != *.asc ]]; then
            gpg --detach-sign -a "$file"
        fi
    done
    twine check dist/*
}

# Function to upload to test PyPI
function test_upload() {
    twine upload -r testpypi dist/*    
    # twine upload --repository-url https://test.pypi.org/legacy/ dist/*
}

function upload() {
    twine upload dist/*    
}

# Main script execution
case $1 in
    format)
        format_code
        ;;
    create_dist)
        create_dist
        ;;
    test_upload)
        test_upload
        ;;
    upload)
        upload
        ;;
    *)
        echo "Usage: $0 {format|create_dist|test_upload|upload}"
        ;;
esac

