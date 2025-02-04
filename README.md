# Microservices-Based E-Commerce Platform

This repository demonstrates a microservices-based e-commerce platform built with:

- **Product Service:**  
  A C++ service using [Crow](https://github.com/CrowCpp/Crow) and [libpqxx](https://github.com/jtv/libpqxx) that retrieves product data from a PostgreSQL database.

- **Order Service:**  
  A Python service using Flask and psycopg2 that allows order creation and persists orders in PostgreSQL.

- **PostgreSQL Database:**  
  Used to persist products and orders. The database is automatically initialized using the SQL script in `db/init.sql`.

- **Docker Compose:**  
  Orchestrates the multi-container setup including the two services and PostgreSQL.

- **CI/CD Pipeline:**  
  GitHub Actions workflow builds Docker images, runs unit and integration tests, and ensures the platform is working correctly.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/install/)
- (Optional) [CMake](https://cmake.org/) and a C++ compiler if you wish to build locally.

### Running Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/microservices-ecommerce.git
   cd microservices-ecommerce