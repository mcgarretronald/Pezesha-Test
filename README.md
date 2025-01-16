# Django REST API for Money Transfer

This project implements a simple REST API that allows users to create accounts, view account details, and transfer money between accounts. It is built with **Django** and uses an **SQLite** in-memory database for simplicity.

## Features

- **Create a new account** with a starting balance.
- **Retrieve account details** by account ID.
- **Transfer money** from one account to another.
- Ensures that:
  - An account cannot have a negative balance.
  - The transfer amount must be greater than zero.
  - If the source account doesn't have enough funds, the transfer fails.
- Uses **Docker** for containerization, with an easy-to-setup environment.

## Table of Contents

1. [Technologies Used](#technologies-used)
2. [Setup Instructions](#setup-instructions)
3. [API Endpoints](#api-endpoints)

---

## Technologies Used

- **Django**: Framework used to build the REST API.
- **SQLite**: In-memory database used for simplicity.
- **Docker**: For containerization of the application.
- **Django Rest Framework**: To quickly build REST APIs with Django.

## Setup Instructions

To set up and run the project, follow these steps:

### 1. Clone the repository:

```bash
git clone https://github.com/mcgarretronald/Pezesha-Test.git
cd money-transfer

```
### 2. Create a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```
### 3. Install dependencies:

```bash
pip install -r requirements.txt
```
### 4. Run the application locally:
```bash
python manage.py migrate 
python manage.py runserver
```
### 4. Running with Docker:
If you prefer to run the project in a Docker container:
#### 1 .Build the Docker image:
```bash
docker-compose build
```
#### 2.Start the container:
```bash
docker-compose up
```
## API Endpoints
### 1. POST /api/accounts/
Create a new account.

Request Body:
```bash
{
  "username": "john_doe",
  "phone": "0712345678",
  "balance": 1000.00
}
```
Response:

```bash
{
  "id": 1,
  "username": "john_doe",
  "phone": "0712345678",
  "balance": 1000.00,
  "created_at": "2025-01-16T00:00:00Z",
  "updated_at": "2025-01-16T00:00:00Z"
}
```
### 2. GET /api/accounts/{id}/
Retrieve details of an account by account ID.

Response:
```bash
{
  "id": 1,
  "username": "john_doe",
  "phone": "0712345678",
  "balance": 1000.00,
  "created_at": "2025-01-16T00:00:00Z",
  "updated_at": "2025-01-16T00:00:00Z"
}
```
### 3. POST /api/transfers/
Transfer money from one account to another.

Request Body:
```bash
{
  "source_phone": "0712345678",
  "destination_phone": "0723456789",
  "amount": 500.00
}
```
Response (Success):
```bash
{
  "message": "You have sent 500.00 shillings to jane_doe. Your balance is 500.00."
}
```
Response (Failure - insufficient funds):
```bash
{
  "error": "Insufficient funds in source account."
}
```
