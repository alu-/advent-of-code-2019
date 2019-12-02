#!/usr/bin/env bash
if [ "$#" -ne 1 ]
then
    echo "Usage: ./pandoc file.html > output_file.org"
    exit 1
fi
pandoc $1 -f html -t org --wrap=preserve
