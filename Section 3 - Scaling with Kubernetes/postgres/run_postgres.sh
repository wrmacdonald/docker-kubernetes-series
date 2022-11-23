#! /usr/bin/env zsh

docker run -d --rm \
    --env-file=postgres.env \
    -v "$(pwd)"/csvs:/var/lib/postgresql/csvs \
    -v "$(pwd)"/scripts/init.sql:/docker-entrypoint-initdb.d/init.sql \
    -p 5432:5432 \
    --name postgres \
    postgres:latest