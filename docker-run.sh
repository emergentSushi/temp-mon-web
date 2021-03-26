#!/bin/sh
docker build . -t tempmon
docker run -d --restart unless-stopped -v ~/data:/app/data -p 80:5000 tempmon
