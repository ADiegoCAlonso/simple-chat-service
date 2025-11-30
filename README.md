# Simple Chat Service: Build & Run Guide

This guide details how to containerize and execute the Simple Chat Service using Docker.

## Prerequisites

* **Docker Desktop** (or Docker Engine) must be installed and running on your machine.
* You must be inside the project directory (where the `Dockerfile` is located).

## 1. Build the Docker Image

The build command reads the `Dockerfile`, installs the Python dependencies defined in `requirements.txt`, and creates an immutable image of your application.

Run the following command in your terminal:

```bash
docker build -t simple-chat-bot .

