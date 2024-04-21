#!/bin/bash

# Define the path to your template and output file
TEMPLATE_PATH="/opt/kong/config/kong.template.yml"
OUTPUT_PATH="/opt/kong/config/kong.yml"

# Ensure the script fails if any commands fail
set -e

# chown kong:kong /opt/kong/config
# chmod 755 /opt/kong/config

# Make a copy of the template to preserve the original
cp $TEMPLATE_PATH $OUTPUT_PATH

# Replace each placeholder with the environment variable's value
# Note: Use double quotes for the sed command to allow variable expansion

sed -i "s/\${JWT_KONG_KEY}/$JWT_KONG_KEY/g" $OUTPUT_PATH
sed -i "s/\${JWT_SECRET}/$JWT_SECRET/g" $OUTPUT_PATH
sed -i "s/\${JWT_ALGORITHM}/$JWT_ALGORITHM/g" $OUTPUT_PATH

# Now start Kong normally
exec /docker-entrypoint.sh kong docker-start