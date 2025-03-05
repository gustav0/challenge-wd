# Walker & Dunlop Challenge Documentation
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## 1. Architecture Overview

### 1.1 Microservice Architecture Diagram
I opted for a hexagonal architecture, enabling careful separation of concerns and the hability to perform changes to the service interaction with other systems in a seamless way. (include other benefits).

<details>
<summary>Expand to see a simple diagram explaining the microservice's architecture.
</summary>
![Microservice Architecture Diagram](path/to/your/image.png)
</details>


### 1.2 Integration into Existing Services

Adapters will be the systems responsible for interaction with existing Property Management and User Database systems.

As specified in the challenge, existing services expose a REST API we can use for interaction.

### 1.3 Technology Stack Justification

- **FastAPI**: Easy to set up, highly scalable, and well-suited for I/O-heavy services.
- **Celery**: Simple to configure, scales efficiently by adding workers, and allows queue customization (e.g., priority notifications, queue per notification type).
- **SQL** Alchemy: this is personal preference, considering SQLModel is now a solid candidate. But I find SQL alchemy's ORM more than enough to perform any kind of SQL query.
- **Alembic**: datavase migration's management. Included out of habit, it is not really needed in a prototype.
- **AsyncPG**: PostgreSQL driver with async capabilities.
- **Pydantic** and PydanticSettings: for schema validation, great to keep inputs and outputs in check. Great for managing app settings.
- **Redis**: Used as Celery's result store (not for caching in this setup).
- **RabbitMQ**: Message broker for Celery task distribution.
- **Pytest**: Preferred testing framework for Python, ensuring reliable and flexible code testing.
- **Ruff**: to keep the codebases consistently formatted, and code lint.

## 2. Assumptions

- **Third-Party Services for Communication:** *Assumes the utilization of third-party services (e.g., Twilio, SendGrid, AWS SES, AWS SNS) for dispatching SMS and email notifications.*

## 3. Setup Instructions (Docker)
This repo can be setup by using docker. The set of commands needed can be found in 2 different formats. It's adviced to use the make commands as its a simplified version.

You can see a more comprehensive list of commands by running:

```bash
make help
```

### Initial Setup
Run each of the following commands in the specified order:
```bash
make pull
make build
make migrate
```
Note that `_base` image won't be pulled, we are supposed to build it.
</details> 


#### Alternative `docker compose` commands

<details>
<summary>Docker compose
</summary>

#### Initial Setup
**DISCLAIMER**: You might need to use `docker-compose` instead of `docker compose` depending on your OS and setup.
Run each of the following commands in the specified order:
```bash
docker compose pull
docker compose build _base
docker compose run --rm alembic upgrade head
```
Note that `_base` image won't be pulled, we are supposed to build it.
</details>

## 4. Run the API and Celery
Run FastAPI and Celery with logs
```bash
make run
```
Or detached mode
```bash
make run args=-d
```


<details>
<summary>Docker compose command
</summary>

### Initial Setup
```bash
docker compose up celery api
```
Or detached mode
```bash
docker compose up celery api -d
```
</details>

## 5. Run tests
You can run the complete set of tests with:
```bash
make test
```

## 6. Known limitation and Areas for Improvement
- **Test coverage**: It's not that good, about 80%, but I tried to provide at least a test for each kind of test that could live in this repo.
- **No Real SMS or Email Sending**: Right now, we're just mocking the 3rd party providers. The system isn't actually sending anything yet.  
- **No Authentication or Authorization**: There's no security in place, so technically, anyone could send notifications if they had access.  
- **Configuration Management Could Be Better**: We’re relying on a local `.env` file instead of something more secure, like a secrets manager.  
- **No Templating System**: Every request has to include the full message, which puts extra work on other services and opens the door to inconsistencies and human error.  
- **Basic Logging Only**: There's a simple logging setup, but it could be more structured and useful.  
- **No Error Tracking**: A tool like Sentry would help us catch and understand issues faster.  
- **Lack of Monitoring**: We have no way to track response times or keep an eye on our dependencies (both internal and external).  
- **No Retry Mechanism on Failures**: If something fails, it just fails. Celery supports automatic retries with exponential backoff that's relatively easy to setup.  
- **No Failover for Notification Providers**: If the active provider goes down, we're stuck. It would be great to have a system that can automatically switch to another provider.
- The notification sourcing logic is quite simple, and most of the details are left for the requester to decide, like the property, secheduled time and message. This could definitely be improved based on real requirements.

## 7. Comments for the reviewer
#### Included files
Some files like `.env` and `logs/app.log` were included to ease to setup process.

#### Initial data
The script `app/setup.py` only objective is to load 4  user preference entries into the database. Meaning, you can use user ids 1, 2, 3 and 4 from the get go.
The script will only do the insert if the Preferences table is empty.

#### Mocked User repository and Property management services
Fetch user action is returning a User schema instance genrated as needed to "simulate" API call to a different microservice. Likewise, property information is generated on demand instead of actually fetcing it from the property management service.
You can check the logc on the respective adapters.

#### Actual notification dispatched is mocked.
The output can be checked in the celery logs after succesfully scheduling a notification.

```docker compose logs celery -f```****

#### FastAPI /docs
The builting Swagger implementation is good enough to interact with the service endpoints. They are all exposed in the `/docs` path.
