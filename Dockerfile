# Use the official Python image from the Python Docker Hub repository as the base image
FROM python:3.12-slim-bullseye

# Set the working directory to /app in the container
WORKDIR /usr/src/app

# Create a non-root user named 'user' with a home directory
RUN useradd -m user

# Copy the requirements.txt file to the container to install Python dependencies
COPY requirements.txt ./

# Install the Python packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
ENV QR_OUTPUT_DIR="./qr_codes"
ENV LOG_OUTPUT_DIR="./logs"
ENV QR_FILL_COLOR="black"
ENV QR_BACK_COLOR="white"

# Before copying the application code, create the logs and qr_codes directories
# and ensure they are owned by the non-root user
RUN mkdir logs qr_codes && chown user:user logs qr_codes

# Copy the rest of the application's source code into the container, setting ownership to 'user'
COPY --chown=user:user . .

# Switch to the 'user' user to run the application
USER user

# Use the Python interpreter as the entrypoint and the script as the first argument
# This allows additional command-line arguments to be passed to the script via the docker run command
ENTRYPOINT ["python", "main.py"]
CMD ["--url","https://github.com/njitmani/Assignment7/"]