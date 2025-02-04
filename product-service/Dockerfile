# product-service/Dockerfile
FROM ubuntu:20.04

# Prevent timezone prompt during installation.
ENV DEBIAN_FRONTEND=noninteractive

# Install build tools and dependencies.
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libboost-all-dev \
    libpqxx-dev \
    pkg-config \
    libasio-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone the Crow repository
RUN git clone https://github.com/CrowCpp/Crow.git


# Copy all source files into the container.
COPY . .

# Create a build directory, configure, and build the project.
RUN mkdir build && cd build && cmake .. -DCROW_INCLUDE_DIR=/app/Crow/include && make

EXPOSE 8080
CMD ["./build/product_service"]