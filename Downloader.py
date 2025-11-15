# bulk download archive.org folders/subfolders and files in one
#
# This script requires the 'requests' library.
# You can install it using: pip install requests

import requests
import os
import time
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def get_identifier_from_url(url):
    """Extracts the identifier from an archive.org URL."""
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    if 'download' in path_parts:
        try:
            return path_parts[path_parts.index('download') + 1]
        except IndexError:
            return None
    elif 'details' in path_parts:
        try:
            return path_parts[path_parts.index('details') + 1]
        except IndexError:
            return None
    return None

def get_files_list(session, identifier):
    """Fetches and parses the files.xml to get a list of files."""
    files_xml_url = f"https://archive.org/download/{identifier}/{identifier}_files.xml"
    print(f"Attempting to fetch file list from: {files_xml_url}")

    try:
        response = session.get(files_xml_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Error: The files.xml for identifier '{identifier}' was not found (404).")
            print("Please check if the identifier is correct and the item exists.")
        else:
            print(f"HTTP Error fetching files.xml: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching files.xml: {e}")
        return None

def download_file(session, file_url, local_path, history_list):
    """Downloads a single file and updates status."""
    file_name = os.path.basename(local_path)
    print(f"Downloading {file_url} to {local_path}")
    try:
        with session.get(file_url, stream=True) as r:
            r.raise_for_status()
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024): # 1MB chunks
                    f.write(chunk)
        print(f"Successfully downloaded {file_name}")
        history_list.append({'file': file_name, 'status': 'Completed'})
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {file_name}: {e}")
        history_list.append({'file': file_name, 'status': f'Error: {e}'})
        return False
    except Exception as e:
        print(f"An unexpected error occurred while downloading {file_name}: {e}")
        history_list.append({'file': file_name, 'status': f'Error: {e}'})
        return False


def download_all_files(url, history_list, max_workers=5):
    """Main function to download all files from an archive.org folder."""
    if not url.endswith('/'):
        url += '/'

    identifier = get_identifier_from_url(url)
    if not identifier:
        print("Invalid archive.org URL. Could not extract identifier.")
        return

    # Use a session for connection pooling
    session = requests.Session()
    files_xml_content = get_files_list(session, identifier)
    if not files_xml_content:
        return

    try:
        root = ET.fromstring(files_xml_content)
        file_paths = [file_elem.get('name') for file_elem in root.findall('.//file') if file_elem.get('name')]
    except ET.ParseError:
        print("Error parsing files.xml. The file may be corrupt.")
        return

    if not file_paths:
        print("No files found in files.xml.")
        return

    download_dir = identifier
    os.makedirs(download_dir, exist_ok=True)
    print(f"Files will be downloaded to: {download_dir}")

    base_download_url = f"https://archive.org/download/{identifier}/"

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for file_path in file_paths:
            file_url = f"{base_download_url}{file_path}"
            local_file_path = os.path.join(download_dir, file_path.lstrip('/'))
            futures.append(executor.submit(download_file, session, file_url, local_file_path, history_list))

        for future in futures:
            future.result()  # Wait for all downloads to complete

    print(f"\nAll files processed. Downloaded to: {download_dir}")

# This allows the script to be both importable and runnable from the command line.
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python Downloader.py <archive.org_folder_url> [max_workers]")
        sys.exit(1)

    archive_url = sys.argv[1]
    # Allow configuring max_workers from command line, default to 5
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 5

    # For standalone execution, we don't have shared memory objects.
    history = []
    download_all_files(archive_url, history, max_workers=workers)
    print("\nHistory:", history)