#!/bin/sh

# Decrypt the a file containing credentials
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_FILE_PASSPHRASE" \
--output $SECRET_FILE $SECRET_FILE.gpg