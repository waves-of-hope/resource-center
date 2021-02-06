#!/bin/sh

export ENCRYPTED_SECRET_FILEPATH=./secrets/encrypted/
export RAW_SECRET_FILEPATH=$HOME/secrets

# Encrypt a file containing credentials
gpg --symmetric --cipher-algo AES256 $RAW_SECRET_FILEPATH/$SECRET_FILE

# Move the secret to the encrypted secrets directory
mv $RAW_SECRET_FILEPATH/$SECRET_FILE.gpg $ENCRYPTED_SECRET_FILEPATH
