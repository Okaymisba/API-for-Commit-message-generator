# ================================
# Stage 1 — Build envhub binary
# ================================
FROM python:3.12-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential wget git python3-dev gcc && \
    pip install --no-cache-dir pyinstaller

# Set working directory
WORKDIR /envhub-src

# Clone the repository
RUN git clone https://github.com/Okaymisba/EnvHub-CLI.git . && \
    git checkout master

# Install the package in development mode
RUN pip install -e .

# Build the binary
RUN pyinstaller --onefile --name envhub envhub/__main__.py

# ================================
# Stage 2 — Final image
# ================================
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Step 1: Copy your local FastAPI requirements
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt

# Step 2: Copy your FastAPI project files
COPY main.py .              
COPY .env .                 

# Step 3: Copy built envhub binary and its code
COPY --from=builder /envhub-src/dist/envhub /usr/local/bin/envhub

# Make the envhub binary executable
RUN chmod +x /usr/local/bin/envhub

# Step 4: Command to run
CMD ["envhub", "decrypt", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
