# GraphQL API Documentation

This document contains GraphQL queries and mutations for testing in the GraphiQL interface.

## **Queries**

### 1. Fetch All Users

```graphql
query {
  allUsers {
    id
    firstName
    lastName
    email
  }
}
```

### 2. Fetch User by Email

```graphql
query {
  userByEmail(email: "user@example.com") {
    id
    firstName
    lastName
  }
}
```

### 3. Fetch All Posts

```graphql
query {
  allPosts {
    id
    content
    createdAt
    user {
      firstName
      lastName
    }
  }
}
```

### 4. Fetch Posts by User

```graphql
query {
  postsByUser(userId: "USER_ID_HERE") {
    id
    content
    createdAt
  }
}
```

### 5. Fetch All Comments

```graphql
query {
  allComments {
    id
    content
    createdAt
    user {
      firstName
      lastName
    }
    post {
      id
      content
    }
  }
}
```

### 6. Fetch Comments for a Specific Post

```graphql
query {
  commentsByPost(postId: "POST_ID_HERE") {
    id
    content
    createdAt
    user {
      firstName
      lastName
    }
  }
}
```

### 7. Fetch All Interactions

```graphql
query {
  allInteractions {
    id
    interactionType
    user {
      firstName
      lastName
    }
    post {
      id
      content
    }
  }
}
```

### 8. Fetch Interactions by Type

```graphql
query {
  interactionsByType(interactionType: LIKE) {
    id
    user {
      firstName
      lastName
    }
    post {
      id
      content
    }
  }
}
```

## **Mutations**

### 9. Create a New User

```graphql
mutation {
  createUser(
    firstName: "John"
    lastName: "Doe"
    email: "john.doe@example.com"
    password: "securepassword"
  ) {
    user {
      id
      firstName
      lastName
      email
    }
  }
}
```

### 10. Create a New Post

```graphql
mutation {
  createPost(content: "This is a new post") {
    post {
      id
      content
      createdAt
      user {
        firstName
        lastName
      }
    }
  }
}
```

### 11. Update an Existing Post

```graphql
mutation {
  updatePost(input: { id: "POST_ID_HERE", content: "Updated content" }) {
    post {
      id
      content
      updatedAt
    }
  }
}
```

### 12. Delete a Post

```graphql
mutation {
  deletePost(id: "POST_ID_HERE") {
    success
  }
}
```

### 13. Create a Comment on a Post

```graphql
mutation {
  createComment(content: "This is a comment", postId: "POST_ID_HERE") {
    comment {
      id
      content
      createdAt
      user {
        firstName
        lastName
      }
    }
  }
}
```

### 14. Delete a Comment

```graphql
mutation {
  deleteComment(id: "COMMENT_ID_HERE") {
    success
  }
}
```

### 15. Create a Like or Share Interaction

```graphql
mutation {
  createOrUpdateInteraction(postId: "POST_ID_HERE", interactionType: LIKE) {
    interaction {
      id
      interactionType
      createdAt
      post {
        id
        content
      }
    }
  }
}
```

### 16. Delete an Interaction

```graphql
mutation {
  deleteInteraction(id: "INTERACTION_ID_HERE") {
    success
  }
}
```

### 17. Authenticate User (Sign In)

```graphql
mutation {
  signIn(email: "user@example.com", password: "securepassword") {
    token
  }
}
```

### 18. Verify JWT Token

```graphql
mutation {
  verifyToken(token: "YOUR_JWT_TOKEN_HERE") {
    payload
  }
}
```

### 19. Refresh JWT Token

```graphql
mutation {
  refreshToken(token: "YOUR_REFRESH_TOKEN_HERE") {
    token
  }
}
```

