# Social Media Feed Backend

Social Media Feed Backend finds it's application in building scalable and interactive systems like social media platforms.
Key takeaways include:

- Using GraphQL for flexible data fetching.
- Designing schemas for high-traffic applications.
- Managing complex user interactions efficiently.

## Overview

The project involves developing a backend to manage posts and user interactions for a social media feed.
The project emphasizes GraphQL API development, real-time interactions, and scalable backend solutions.

### Project Goals

- **Post Management**: Design APIs for creating, fetching, and managing posts.
- **Flexible Querying**: Implement GraphQL for advanced querying capabilities.
- **Scalability**: Optimize database schema for high-volume user interactions.

### Technologies Used

- **Django**: For backend development.
- **PostgreSQL**: To store relational data efficiently.
- **GraphQL (Graphene)**: For flexible data queries.
- **GraphQL Playground**: For testing our APIs.

### Key Features

1. **GraphQL APIs**
    - Enable flexible querying of posts and interactions.
    - Provide resolvers for creating, fetching, and managing posts and interactions.

2. **Interaction Management**
    - Allow users to like, comment, and share posts.
    - Track interactions for analytics and feedback.

3. **API Testing**
    - Publish a hosted GraphQL Playground for easy testing.

### Prerequisites

- Python 3.x

- Docker (optional for containerization)

- Set your envronment variables in a **.env** file at the project root using the sample in [env variables](.env.example)

### Getting Started

- **create aand activate a virtual environment**

```bash
    python3 -m venv venv && source venv/bin/activate
```

- **clone the repo and cd into the repo**

```bash
    git clone https://github.com/lawalgodwin/social-media-feed-backend.git && cd social-media-feed-backend
```

- **install dependencies and prepare the database**

```bash
    pip install -r requirements.txt && ./manage.py makemigrations && ./manage.py migrate
```

- **run the command below to start the api**

```bash
    ./manage.py runserver 0.0.0.0:8000
```

### Accessing the API

- The api is accessible on the host [http://localhost:8000/graphql]
- Visit [samples api requests](apidocs.md) to see samples of queries and mutations
