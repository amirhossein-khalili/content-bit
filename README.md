
---

# Content Critic

This project allows users to register via email in two steps, with the ability to receive a verification code. Additionally, it includes endpoints for retrieving a paginated list of articles.

## Features

- **Email Verification and Registration**: Users can receive a verification code and complete their registration via email in two steps.
- **Article Retrieval**: Users can retrieve a list of articles with pagination to handle large volumes of data.
- **Docker Support**: The project can be run using Docker, with a pre-configured `Dockerfile` and `docker-compose` for easy setup.

## Project Setup

### Option 1: Traditional Setup

#### Step 1: Setting Up the Virtual Environment

1. Create a virtual environment using the following command:

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

#### Step 2: Setting Up the Environment Variables

1. Create a `.env` file in the project root directory.
2. Use the `example.env` file as a template for your `.env` file.

#### Step 3: Testing and Documentation

- A Postman collection is available in the `document` directory, which you can use to test the email verification and registration process.
- API documentation is available via Swagger at the following endpoint:
  ```
  /api/schema/swagger-ui/
  ```
- After logging in and obtaining a JWT token, you can register and interact with the API using the provided endpoints.

#### Step 4: Using JWT Tokens and Endpoints

- Use the JWT token for authentication when accessing protected endpoints.
- You can explore and test the available endpoints using Postman or Swagger.

### Option 2: Docker Setup

#### Step 1: Building and Running the Docker Containers

1. Ensure you have Docker and Docker Compose installed on your machine.
2. Build and start the Docker containers using the following command:

   ```bash
   docker-compose up --build
   ```

   This will create and start the necessary containers for the application, including the web server and database.

#### Step 2: Setting Up the Environment Variables

- As with the traditional setup, you’ll need to create a `.env` file in the project root directory. The `docker-compose.yml` file is configured to use this `.env` file for environment variables.

#### Step 3: Accessing the Application

- Once the containers are running, you can access the API documentation via Swagger at:
  ```
  http://localhost:<your_port>/api/schema/swagger-ui/
  ```
- The application is fully containerized, so you don’t need to worry about setting up a virtual environment or installing dependencies manually.


---
