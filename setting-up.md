---
description: How to set up your OpenLoop instance
---

# Setting up

OpenLoop should be running from gunicorn or another service that is production-ready. It should also have a reverse proxy (Nginx) setup for SSL. Once done point a systemd service to your service worker with your flags.

