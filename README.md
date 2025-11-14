# Archive.org Downloader

This script allows you to bulk download all files and subfolders from an [archive.org](https://archive.org) item.

## Prerequisites

This script requires Python 3 and the `requests` library.

You can install the `requests` library using pip:

```bash
pip install requests
```

## Usage

To download all files from an archive.org item, run the script from your terminal and pass the URL of the item as an argument.

```bash
python Downloader.py <archive.org_folder_url>
```

### Example

```bash
python Downloader.py https://archive.org/details/your-archive-item
```

The script will create a directory named after the archive item's identifier and download all files into it.
