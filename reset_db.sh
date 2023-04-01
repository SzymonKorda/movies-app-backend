#!/bin/bash
docker stop filmweb_db
docker rm filmweb_db
docker-compose up -d
