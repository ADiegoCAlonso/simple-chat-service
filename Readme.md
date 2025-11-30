# **Simple Chat Service: Build & Run Guide**

This guide details how to containerize and execute the Simple Chat Service using Docker.

## **Prerequisites**

* **Docker Desktop** (or Docker Engine) must be installed and running on your machine.  
* You must be inside the project directory (where the Dockerfile is located).

## **1\. Build the Docker Image**

The build command reads the Dockerfile, installs the Python dependencies defined in requirements.txt, and creates an immutable image of your application.

Run the following command in your terminal:

docker build \-t simple-chat-bot .

**breakdown of flags:**

* docker build: The command to generate an image.  
* \-t simple-chat-bot: Tags (names) the image "simple-chat-bot" so you can refer to it easily later.  
* .: Context path. Tells Docker to look for the Dockerfile in the *current directory*.

## **2\. Run the Container**

Once the build is complete, use the following command to start the service:

docker run \-p 8000:80 simple-chat-bot

**breakdown of flags:**

* \-p 8000:80: Port mapping. It maps port **8000** on your local machine (host) to port **80** inside the container (where FastAPI is listening).  
* simple-chat-bot: The name of the image we built in step 1\.

*Optional: To run the container in the background (detached mode), add the \-d flag:*

docker run \-d \-p 8000:80 simple-chat-bot

## **3\. Verify the Service**

Once the container is running, the API is accessible via localhost.

### **Automatic Documentation (Swagger UI)**

Open your web browser and navigate to:

**http://localhost:8000/docs**

This interface allows you to interactively test the /chat endpoint directly from your browser.

### **Terminal Test (cURL)**

You can test the endpoint using curl:

curl \-X 'POST' \\  
  'http://localhost:8000/chat' \\  
  \-H 'Content-Type: application/json' \\  
  \-d '{  
  "message": "Hello"  
}'

## **Troubleshooting**

Port Already in Use  
If you see an error saying Bind for 0.0.0.0:8000 failed: port is already allocated, it means another application is using port 8000\. Try mapping to a different port (e.g., 8001):  
docker run \-p 8001:80 simple-chat-bot

Then access the service at http://localhost:8001/docs.

**Stopping the Container**

* If running in the foreground: Press Ctrl+C.  
* If running in the background (detached):  
  1. Run docker ps to find the Container ID.  
  2. Run docker stop \<CONTAINER\_ID\>.