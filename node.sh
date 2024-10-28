#!/bin/bash

# Check if nvm is installed
# Install and use the version specified in .nvmrc
if command -v nvm > /dev/null 2>&1; then
    nvm install
    nvm use
else
    echo "nvm is not installed."
    echo "Use default Node.js"
fi

# Install npm dependencies
npm install
npm run webpack
exit 1
