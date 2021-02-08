#!/bin/sh

export ENCRYPTED_SECRET_FILEPATH=./secrets/encrypted/
export RAW_SECRET_FILEPATH=$HOME/secrets

# Create the raw secret directory if is doesn't exist
mkdir $RAW_SECRET_FILEPATH

# Decrypt the a file containing credentials
# --batch to prevent interactive command
# --yes to assume "yes" for questions
gpg --quiet --batch --yes --decrypt --passphrase="$SECRET_FILE_PASSPHRASE" \
--output $RAW_SECRET_FILEPATH/$SECRET_FILE \
$ENCRYPTED_SECRET_FILEPATH/$SECRET_FILE.gpg
