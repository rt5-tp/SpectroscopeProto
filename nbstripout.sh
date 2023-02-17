#!/bin/bash

# Find all notebook files in the repository and run nbstripout on them
find . -name "*.ipynb" -exec nbstripout {} \;
