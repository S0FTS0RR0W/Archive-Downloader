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

## Running with Docker

You can also run this application using Docker.

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system.

### Building the Image

First, build the Docker image:

```bash
docker build -t archive-downloader .
```

### Running the Container

Then, run the container:

```bash
docker run -p 5000:5000 archive-downloader
```

The application will be available at [http://localhost:5000](http://localhost:5000).

## Running with Docker Compose

You can also use Docker Compose to run the application.

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your system.

### Usage

From the root of the project directory, run:

```bash
docker-compose up
```

The application will be available at [http://localhost:5000](http://localhost:5000).
