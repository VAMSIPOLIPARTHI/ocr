# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Install system dependencies required by cv2, PaddleOCR, and pdf2image
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*


# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Set up a non-root user (Hugging Face Spaces requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Copy files and ensure the new user owns them
COPY --chown=user:user . .

# Expose port (HF Spaces uses 7860 by default)
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]

