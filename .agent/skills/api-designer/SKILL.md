---
name: api-designer
description: REST/GraphQL API design and OpenAPI specs. Use for API design tasks.
triggers:
  - "design API"
  - "REST API"
  - "GraphQL"
  - "OpenAPI"
---

# API Designer Skill

## Identity

You are an API design specialist focused on creating well-structured, documented, and maintainable APIs.

## When to Use

- Designing new APIs
- Creating OpenAPI specifications
- Planning API architecture
- Documenting existing APIs

## RESTful API Design Principles

### Resource Naming

```
Good:
GET    /users                 # List users
GET    /users/{id}            # Get user
POST   /users                 # Create user
PUT    /users/{id}            # Update user
DELETE /users/{id}            # Delete user
GET    /users/{id}/posts      # Get user's posts

Bad:
GET    /getUsers
POST   /createUser
GET    /user-posts/{id}
```

### HTTP Methods

| Method | Purpose           | Idempotent |
| ------ | ----------------- | ---------- |
| GET    | Retrieve resource | Yes        |
| POST   | Create resource   | No         |
| PUT    | Replace resource  | Yes        |
| PATCH  | Partial update    | No         |
| DELETE | Remove resource   | Yes        |

### Status Codes

| Code | Meaning               | Usage                      |
| ---- | --------------------- | -------------------------- |
| 200  | OK                    | Successful GET, PUT, PATCH |
| 201  | Created               | Successful POST            |
| 204  | No Content            | Successful DELETE          |
| 400  | Bad Request           | Invalid input              |
| 401  | Unauthorized          | Missing auth               |
| 403  | Forbidden             | Insufficient permissions   |
| 404  | Not Found             | Resource doesn't exist     |
| 422  | Unprocessable Entity  | Validation error           |
| 500  | Internal Server Error | Server failure             |

## OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: My API
  description: API for managing resources
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api-staging.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List all users
      tags:
        - Users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        "200":
          description: Successful response
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserList"

    post:
      summary: Create a user
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateUser"
      responses:
        "201":
          description: User created
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"

  /users/{id}:
    get:
      summary: Get a user by ID
      tags:
        - Users
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Successful response
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/User"
        "404":
          description: User not found

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        email:
          type: string
          format: email
        createdAt:
          type: string
          format: date-time

    CreateUser:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: "#/components/schemas/User"
        meta:
          type: object
          properties:
            total:
              type: integer
            page:
              type: integer
            limit:
              type: integer

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

## Response Format

### Success Response

```json
{
  "data": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### List Response with Pagination

```json
{
  "data": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "totalPages": 5
  },
  "links": {
    "first": "/users?page=1",
    "prev": null,
    "next": "/users?page=2",
    "last": "/users?page=5"
  }
}
```

### Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email"
      }
    ]
  }
}
```

## GraphQL Schema

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  createdAt: DateTime!
}

type Query {
  user(id: ID!): User
  users(page: Int, limit: Int): UserConnection!
  post(id: ID!): Post
  posts(page: Int, limit: Int): PostConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!

  createPost(input: CreatePostInput!): Post!
}

input CreateUserInput {
  name: String!
  email: String!
}

input UpdateUserInput {
  name: String
  email: String
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

scalar DateTime
```

## API Versioning

```
URL Path:    /v1/users, /v2/users
Header:      Accept: application/vnd.myapi.v1+json
Query Param: /users?version=1
```

## Tips

- Use nouns for resources, verbs via HTTP methods
- Be consistent with naming conventions
- Document all endpoints
- Use proper HTTP status codes
- Implement pagination for lists
- Version your APIs
- Validate all input
