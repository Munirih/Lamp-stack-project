# Run the application locally Guide

## Step 1: Clone the Repository

Clone the project repository to your local machine.

```bash
git clone <YOUR_REPOSITORY_URL>

cd <YOUR_PROJECT_DIRECTORY>
```

---

## Step 2: Download and Extract the Project

If you downloaded the project as a ZIP file from GitHub instead of cloning it:

1. Open the GitHub repository.
2. Click **Code**.
3. Select **Download ZIP**.
4. Extract the ZIP file.
5. Open a terminal inside the extracted project folder.

If you cloned the repository using Git, you can skip this step.

---

## Step 3: Run the Application Locally

Before deploying the application to AWS, verify that it works correctly on your local machine.

### Install the Python dependencies

```bash
pip install -r requirements.txt
```

### Configure the environment variables

Create a `.env` file in the root of the project.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pythonapp
DB_USER=root
DB_PASSWORD=password
FLASK_ENV=development
```

Modify the values to match your local MySQL database.

### Start the application

```bash
python app.py
```

or

```bash
flask run
```

depending on your project.

The application should now be available at:

```
http://localhost:5000
```

Verify that the application loads correctly before continuing.

---

## Step 4: Build the Docker Image

Ensure Docker Desktop is running.

Build the Docker image:

```bash
docker build -t yourdockerhubusername/python-web-app:latest .
```

Verify that the image was created.

```bash
docker images
```

You should see something similar to:

```
REPOSITORY                           TAG
yourdockerhubusername/python-web-app latest
```

---

## Step 5: Test the Docker Container

Run the Docker container locally.

```bash
docker run -d \
  --name python-web-app \
  -p 5000:5000 \
  --env-file .env \
  yourdockerhubusername/python-web-app:latest
```

Open your browser.

```
http://localhost:5000
```

Verify that the application behaves the same way as when running it directly with Python.

To stop the container:

```bash
docker stop python-web-app

docker rm python-web-app
```

---

## Step 6: Push the Docker Image to Docker Hub

Log in to Docker Hub.

```bash
docker login
```

Enter your Docker Hub username and password when prompted.

Tag the image 

```bash
docker tag python-web-app:latest yourdockerhubusername/python-web-app:latest
```

Push the image.

```bash
docker push yourdockerhubusername/python-web-app:latest
```

Verify that the image appears in your Docker Hub repository.

This image will later be pulled by the EC2 instance during deployment.

---

Continue with creating the AWS infrastructure...