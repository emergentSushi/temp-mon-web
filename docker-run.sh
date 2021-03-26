#!/bin/sh
docker build . -t tempmon
docker run -d -v ~/data:/app/data -p 80:5000 tempmon
