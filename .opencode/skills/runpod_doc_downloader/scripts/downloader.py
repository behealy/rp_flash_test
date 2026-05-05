#!/usr/bin/env python3
"""

# This script is run for the opencode runpod_doc_downloader skill.
# The AI agent should execute this script when requested


Runpod Documentation Downloader Script

Downloads documentation files from https://docs.runpod.io/llms.txt
and organizes them into docs/runpod/<path>/ structure.
"""

import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse

INDEX_URL = "https://docs.runpod.io/llms.txt"
OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "runpod"


def download_file(url: str, output_path: Path) -> bool:
    """Download a file from URL to the specified path."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        output_path.write_text(response.text, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


def parse_markdown_links(content: str) -> list[tuple[str, str]]:
    """
    Parse markdown links from content.
    Returns list of tuples: (url, title)
    """
    links = []
    # Match markdown links: [title](url)
    pattern = r'\[([^\]]+)\]\((https?://[^)]+)\)'
    matches = re.findall(pattern, content)
    
    for title, url in matches:
        # Skip OpenAPI specs section
        if "api-reference" in url and "openapi" in url:
            continue
        links.append((url, title))
    
    return links


def get_relative_path(url: str) -> str:
    """Convert a URL to a relative path for the output directory."""
    parsed = urlparse(url)
    path = parsed.path.lstrip('/')
    return path


def get_subfolder_from_url(url: str) -> str:
    """Get the subfolder path from a URL."""
    path = get_relative_path(url)
    # Remove the last component (filename) to get the subfolder
    parts = path.split('/')
    if len(parts) > 1:
        return '/'.join(parts[:-1])
    return ""


def main():
    """Main function to download and organize documentation."""
    print(f"Downloading index from {INDEX_URL}...")
    response = requests.get(INDEX_URL, timeout=30)
    response.raise_for_status()
    index_content = response.text
    
    print("Parsing documentation links...")
    links = parse_markdown_links(index_content)
    print(f"Found {len(links)} documentation links")
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Download each document
    success_count = 0
    for url, title in links:
        subfolder = get_subfolder_from_url(url)
        filename = os.path.basename(url)
        
        if subfolder:
            output_path = OUTPUT_DIR / subfolder / filename
        else:
            output_path = OUTPUT_DIR / filename
        
        # Create parent directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if download_file(url, output_path):
            success_count += 1
            print(f"Downloaded: {title} -> {output_path.relative_to(OUTPUT_DIR)}")
    
    print(f"\nCompleted: {success_count}/{len(links)} files downloaded successfully")


if __name__ == "__main__":
    main()

