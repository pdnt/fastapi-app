fastapi-app is a full-fledged, fictitious social media app created using FastAPI.

The application is composed of four routes that allow a person to create a user, authenticate, create a post, view other posts, and vote for them.
This API implements serialization/deserialization, schema validation, and models.

Data is stored in a PostgreSQL database, which is managed using SQLAlchemy, and alembic as a database migration tool.

**Unit testing** is performed using the pytest framework.

The application was successfully deployed on:
-   DigitalOcean, using NGINX to handle SSL termination.
-   Heroku.
-   Ubuntu Server running on an LXC container over Proxmox on my local server.
    
A CI/CD Pipeline is created using GitHub Actions.
**Continuous integration** is achieved by creating a testing environment that accesses our environment variables (which are saved as environment secrets) and creating a runner that pulls our code and executes the necessary steps to ensure our application can run.
As an extra step, a docker image is built and pushed to Docker Hub.
**Continuous delivery** is implemented by deploying our application to Heroku.

**## Routes**

****Auth:**** Allows a user to authenticate into their account using their email and password.
An access token is created, which authorizes the user to perform actions for x amount of minutes. This number can be changed under your environment variables.
If one of the credentials is incorrect, a message will be returned indicating that the credentials are invalid.

****User:**** Allows a person to create a user.
OAuth2PasswordBearer is used to let FastAPI know that we are creating a security schema.
JWT is used to encode the user and the password, using the HS256 algorithm. The password is hashed and the output is stored in a SQL database.

****Post:**** It's used to create posts, which consist of two fields, title and content.
The schema is also formed by:
- published: Boolean that defines if the post was published. It's set to TRUE.
- id: Provides a unique identifier for the post.
- created_at: Exact date of the creation of the post.
- owner_id: Links the post to the unique ID of the user that created it.
- owner: Provides a relationship between two mapped classes (Post and User).