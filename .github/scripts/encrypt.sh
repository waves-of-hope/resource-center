#!/bin/sh

# Encrypt a file containing credentials
gpg --symmetric --cipher-algo AES256 $SECRET_FILE