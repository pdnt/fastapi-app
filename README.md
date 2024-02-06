# FastAPI Social Media App

**fastapi-app** is a fully functional, fictitious social media application built using FastAPI.

The application consists of four routes enabling users to perform actions such as creating a user account, authentication, posting content, viewing other posts, and voting on them. It incorporates features such as serialization/deserialization, schema validation, and database models.

Data storage is managed using a PostgreSQL database, leveraging SQLAlchemy for ORM functionality and alembic for seamless database migrations.

Unit testing is conducted using the pytest framework to ensure the reliability and correctness of the application.

## Deployment

The application has been successfully deployed on multiple platforms:

- **DigitalOcean**: Utilizing NGINX for SSL termination.
- **Heroku**: Deployed to Heroku's cloud platform.
- **Ubuntu Server**: Hosted on an LXC container via Proxmox on a local server.

## CI/CD Pipeline

A robust CI/CD pipeline has been established using GitHub Actions:

- **Continuous Integration (CI)**: A testing environment is created to access environment variables securely stored as secrets. A runner is configured to pull the latest code and execute necessary tests, ensuring the application's functionality.
- **Continuous Delivery (CD)**: Docker images are built and pushed to Docker Hub, facilitating deployment.

## Routes

### Auth
Allows users to authenticate into their account using their email and password. An access token is generated, authorizing user actions for a configurable duration. Invalid credentials trigger an appropriate error message.

### User
Enables users to create accounts securely. OAuth2PasswordBearer ensures a robust security schema, with JWT used to encode user credentials. Passwords are securely hashed and stored in the PostgreSQL database.

### Post
Facilitates the creation of posts, comprising title and content fields. Additional post attributes include:

- **published**: Boolean indicating post publication status.
- **id**: Unique identifier for each post.
- **created_at**: Timestamp indicating post creation time.
- **owner_id**: Links posts to the unique user ID of their creator.
- **owner**: Establishes a relationship between post and user entities.

Users can only create posts associated with their unique ID and cannot delete posts owned by others.

### Vote
Enables users to add or remove votes on posts. Users can vote on their posts and are restricted from adding multiple votes to the same post or removing votes they haven't cast.

## Acknowledgements

This project is the culmination of a comprehensive 19-hour [Python API development course](https://www.freecodecamp.org/news/creating-apis-with-python-free-19-hour-course/) offered by freeCodeCamp.
