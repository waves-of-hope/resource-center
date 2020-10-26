#!/bin/sh

# Make a directory for storing secrets
mkdir $HOME/secrets

# Decrypt the file
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_FILE_PASSPHRASE" \
--output $HOME/$SECRET_FILE $SECRET_FILE.gpg