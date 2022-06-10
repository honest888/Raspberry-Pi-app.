#!/usr/bin/env bash
gunicorn3 -w 5 -b 0.0.0.0:3001 wsgi:app --timeout 600
