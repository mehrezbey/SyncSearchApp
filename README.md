# SyncSearchApp

## Overview

This project integrates a database with Elasticsearch to enable advanced search capabilities and ensures synchronization between the database and Elasticsearch in real-time.

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Elasticsearch
- Kibana
- Docker
- phpMyAdmin

## Setup

1. **Environment Setup:**
   - Create a `.env` file based on `.env.example.txt` to configure your environment variables.

2. **Running the Application:**
   - Use Docker Compose to build and run the application:
     ```bash
     docker-compose up --build
     ```

## Testing

### Synchronization Test

To test synchronization between the database and Elasticsearch:

1. Navigate to `main/routes.py`.
2. Access the endpoint `/test`.
3. Send requests to simulate insert/update/delete operations in the database according to your database.
4. Verify that changes reflect accurately in Elasticsearch.

### Search Test

To test the advanced search functionality:

1. Access `http://127.0.0.1:5000/search` in your browser.
2. Perform searches to validate the accuracy and performance of search results.

## Notes

- Ensure Docker is installed and running on your system to execute the application.
- Modify `.env` according to your specific configuration needs before running the application.
