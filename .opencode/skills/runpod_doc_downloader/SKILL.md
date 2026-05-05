---
name: runpod_doc_downloader
description: Checks https://docs.runpod.io/llms.txt file and downloads the indexed documentation files into a structured folder hierarchy
user-invocable: true
---

# Runpod Documentation Downloader.

## Description

This skill downloads the Runpod documentation index from `https://docs.runpod.io/llms.txt`, extracts all document URLs, downloads each document, and places them in an organized folder structure under `docs/runpod/`.

## Usage
When you are prompted to use this skill, simply run the script at scripts/downloader.py
