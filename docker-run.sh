#!/bin/sh
docker build . -t tempmon
docker run -d -v ~/data:/app/data -p 8000:80 tempmon
