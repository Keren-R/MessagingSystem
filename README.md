# Messaging System API

The Messaging System API is a Django-based web application designed to facilitate messaging between users. 
It provides a platform for users to send and receive messages securely. 
The API is built using Django and Django Rest Framework, ensuring robustness, scalability, and ease of use.


## Features

- User Authentication: Secure user authentication system to protect user data and messages.
- Send and Receive Messages: Allows users to send messages to other users and view messages received from others.
- Message Status: Messages can be marked as read or unread.
- RESTful API: Provides a RESTful API for seamless integration with frontend applications.

## Technologies Used

- Django: Backend framework for building the web application.
- Django Rest Framework (DRF): Toolkit for building APIs with Django.
- SQLite: Database to store user data and messages.
- Whitenoise: Simplifies serving static files.
- Python 3: Programming language used for backend development.

## Setup Environment
### Prerequisites
* Python 3.10
* SQLite

### Installation

1. Clone the Repository:

    ```commandline
    git clone https://github.com/Keren-R/MessagingSystem.git
   ```

2. Navigate to the Project Directory:

    ```commandline
    cd messaging-system
    ```

3. Install Dependencies:

    ```commandline
    pip install -r requirements.txt
    ```

4. Database Migration

    Apply database migrations to create the necessary tables:

    ```commandline
    python manage.py migrate
    ```

   5. Start the Server
      ```commandline
      python manage.py runserver
      ```

      The server will start on http://127.0.0.1:8000/.

## Deployed Server 
Access the deployed Message System API using the following URL:
    http://keren.pythonanywhere.com


## API Usage
### Authentication

   To access the API endpoints, you need to authenticate by providing a username and password to the Django-rest console.

### Endpoints:

1. Send message: POST /api/messages/
2. Retrieve all messages per logged in user: GET /api/messages/
3. Retrieve all unread messages per logged in user: /api/unread/
4. Update message (mark as read): PUT /api/messages/<message_id>/
5. Delete Message: DELETE /api/messages/<message_id>/


### Postman Examples

Examples of requests demonstrating how to use the API are attached in a Postman file. You can import this file into Postman to explore and test the API endpoints.