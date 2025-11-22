FROM python:3.11-slim-bookworm                                                                                                                                                          

# Prevent interactive installs
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update  
RUN apt-get install -y --no-install-recommends curl unzip git iputils-ping dnsutils && rm -rf /var/lib/apt/lists/*

# Install uvx (used by MCPClient to spawn MCP servers)
RUN curl -fsSL https://astral.sh/uv/install.sh | bash
ENV PATH="/root/.local/bin:${PATH}"

# Create working directory
WORKDIR /app

# Copy source files from app/ directory
COPY app/ ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Optional: cache the AWS EKS MCP server binary for faster startup
RUN uvx awslabs.eks-mcp-server@latest --version || true

# Set default environment variables
ENV PYTHONUNBUFFERED=1

# Make entry point executable
RUN chmod +x /app/entry_point.sh

# Entry point
ENTRYPOINT ["./entry_point.sh"]


