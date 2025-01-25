# Valdin: Streamlining Business Operations

Welcome to **Valdin**, an innovative web-based platform designed to streamline and enhance product management, inventory tracking, and activity monitoring for businesses. This repository contains the codebase, documentation, and resources for the Valdin project.

---

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)

---

## Overview
**Valdin** is a web based system designed to streamline small scale business operational workflow. 

---

## Features
- **Product Management**: Add, edit, and update product information, including images, prices, categories, and descriptions.
- **Client Management:** Add, edit, and update client information.
- **Cart Management:** Update product quantity or delete product.
- **Inventory Tracking**: Real-time insights into product quantities and inventory status.
- **Activity Monitoring**: Track and log changes made to products with detailed user activity records.
- **Custom Error Handling**: Displays detailed error messages to improve debugging and enhance user experience.
- **Responsive Interface**: A clean, modern UI built for both desktop and mobile users.

---

## Technologies Used
- **Backend**: Python, Django
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Admin Interface**: Django Admin
- **Additional Tools**: Django Multiupload, pgAdmin for database management

---

## Architecture
Valdin follows a modular and containerized architecture:
- **Backend**: Django-based server managing all business logic and database interactions.
- **Database**: PostgreSQL for robust and scalable data storage.
- **Containerization**: Docker ensures the project is easily deployable across different environments.
- **Development Tools**: `docker-compose` for orchestrating services and environments.

---

## Setup and Installation
Follow these steps to set up Valdin on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/dgamee/valdin_project.git
   cd valdin_project
   ```
   
2. Ensure Docker is installed on your system.

3. Build and run the Docker containers:
   ``` bash
   docker compose up --build
   ```
4. Access the application:
   ``` bash
   Web app: http://localhost:8000 (Login using admin admin12345)
   pgAdmin: http://localhost:16543 (Login using rayden.ai@gmail.com and root)
   ```

5. To stop the services:
   ``` bash
   docker compose down
   ```

---

## Usage
- **Login:** Use the provided credentials to access the admin interface .
- **Manage Client:** Navigate to the "Clients" section to add, edit, or update client information.
- **Manage Product:** Navigate to the "Products" section to add, edit, or update product information and add product to cart.
- **Manage Cart:** Navigate to the "Cart" icon to update product quantity or delete product.
- **Track Activities:** View the activity log for detailed insights into changes made by users.