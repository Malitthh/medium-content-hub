# API Testing Guide
> A personal reference for SOAP, REST, and GraphQL — covering concepts, HTTP fundamentals, testing strategies, and tooling.

---

## Table of Contents

1. [The Restaurant Analogy — API types at a glance](#1-the-restaurant-analogy)
2. [HTTP Fundamentals](#2-http-fundamentals)
   - [HTTP Methods](#21-http-methods)
   - [HTTP Status Codes](#22-http-status-codes)
   - [Request & Response Structure](#23-request--response-structure)
   - [Headers](#24-headers)
3. [SOAP](#3-soap)
   - [What is SOAP?](#31-what-is-soap)
   - [SOAP Request Structure](#32-soap-request-structure)
   - [When to use SOAP](#33-when-to-use-soap)
4. [REST](#4-rest)
   - [What is REST?](#41-what-is-rest)
   - [REST Endpoints & CRUD](#42-rest-endpoints--crud)
   - [REST Request & Response Examples](#43-rest-request--response-examples)
   - [Common REST Problems](#44-common-rest-problems)
5. [GraphQL](#5-graphql)
   - [What is GraphQL?](#51-what-is-graphql)
   - [Query — Reading Data](#52-query--reading-data)
   - [Mutation — Writing Data](#53-mutation--writing-data)
   - [Subscription — Real-time Data](#54-subscription--real-time-data)
   - [GraphQL Error Responses](#55-graphql-error-responses)
   - [The HTTP 200 Trap](#56-the-http-200-trap)
6. [API Comparison Table](#6-api-comparison-table)
7. [Testing APIs — General Strategy](#7-testing-apis--general-strategy)
   - [Testing Layers](#71-testing-layers)
   - [Types of Test Cases](#72-types-of-test-cases)
8. [Testing REST APIs](#8-testing-rest-apis)
   - [Postman — REST Setup](#81-postman--rest-setup)
   - [Common REST Assertions](#82-common-rest-assertions)
9. [Testing GraphQL APIs](#9-testing-graphql-apis)
   - [GraphQL-Specific Test Cases](#91-graphql-specific-test-cases)
   - [Apollo Sandbox Guide](#92-apollo-sandbox-guide)
   - [Postman — GraphQL Setup](#93-postman--graphql-setup)
   - [Postman Test Scripts for GraphQL](#94-postman-test-scripts-for-graphql)
   - [Newman — CI/CD Integration](#95-newman--cicd-integration)
10. [Tool Comparison: Apollo vs Postman](#10-tool-comparison-apollo-vs-postman)
11. [Recommended Workflow for SDETs](#11-recommended-workflow-for-sdets)
12. [Quick Reference Cheatsheets](#12-quick-reference-cheatsheets)
    - [HTTP Status Codes Cheatsheet](#121-http-status-codes-cheatsheet)
    - [Postman GraphQL Assertions Cheatsheet](#122-postman-graphql-assertions-cheatsheet)
    - [GraphQL Operation Types Cheatsheet](#123-graphql-operation-types-cheatsheet)
13. [Public APIs for Practice](#13-public-apis-for-practice)

---

## 1. The Restaurant Analogy

Think of an API as a restaurant. The type of API determines how you order your food.

| API Type | Analogy | Description |
|----------|---------|-------------|
| **SOAP** | Fine dining restaurant | Rigid, formal protocol. You fill out an order form (XML envelope). Very structured and reliable, but verbose and slow. |
| **REST** | À la carte restaurant | Fixed menu (endpoints). You order a "User meal" and get everything on the plate — name, email, photo, address — whether you wanted it all or not. |
| **GraphQL** | Build-your-own meal | You tell the kitchen exactly what you want: "Give me just the username and profile picture." One trip to the counter, custom order every time. |

---

## 2. HTTP Fundamentals

Every API — SOAP, REST, and GraphQL — communicates over HTTP. Understanding HTTP is the foundation of API testing.

### 2.1 HTTP Methods

HTTP methods (also called verbs) describe the intent of a request.

| Method | Purpose | Idempotent? | Safe? | Example |
|--------|---------|-------------|-------|---------|
| `GET` | Retrieve a resource | Yes | Yes | `GET /users/1` — fetch user with ID 1 |
| `POST` | Create a new resource | No | No | `POST /users` — create a new user |
| `PUT` | Replace a resource entirely | Yes | No | `PUT /users/1` — replace user 1's full data |
| `PATCH` | Partially update a resource | Yes | No | `PATCH /users/1` — update only the email of user 1 |
| `DELETE` | Remove a resource | Yes | No | `DELETE /users/1` — delete user 1 |
| `HEAD` | Same as GET but returns headers only (no body) | Yes | Yes | Check if a resource exists without downloading it |
| `OPTIONS` | Describes what methods a resource supports | Yes | Yes | Used in CORS preflight checks |

> **Idempotent** means calling it multiple times gives the same result as calling it once.
> **Safe** means it does not modify server state.

---

### 2.2 HTTP Status Codes

Status codes tell you what happened with your request. They are grouped into five classes.

#### 1xx — Informational
Rarely seen in API testing. The server is acknowledging it received the request and is still processing.

| Code | Name | Meaning |
|------|------|---------|
| `100` | Continue | The server received the request headers; client should send the body |
| `101` | Switching Protocols | Used when upgrading to WebSocket (important for GraphQL Subscriptions) |

#### 2xx — Success
The request was received, understood, and accepted.

| Code | Name | Meaning | Common Use |
|------|------|---------|------------|
| `200` | OK | Standard success response | GET, PUT, PATCH responses |
| `201` | Created | A new resource was created | POST responses |
| `204` | No Content | Success but nothing to return | DELETE responses |
| `206` | Partial Content | Only part of the resource is returned | Paginated or range requests |

#### 3xx — Redirection
The client needs to take further action, usually by following a redirect.

| Code | Name | Meaning |
|------|------|---------|
| `301` | Moved Permanently | Resource has permanently moved to a new URL |
| `302` | Found | Temporary redirect |
| `304` | Not Modified | Cached version is still valid; no need to re-download |

#### 4xx — Client Errors
The request was wrong. The problem is on the client side.

| Code | Name | Meaning | Testing Tip |
|------|------|---------|-------------|
| `400` | Bad Request | Malformed request syntax, invalid parameters | Test with missing required fields |
| `401` | Unauthorized | No credentials provided or credentials invalid | Test with missing/expired token |
| `403` | Forbidden | Authenticated but not allowed | Test with a user who lacks permission |
| `404` | Not Found | Resource does not exist | Test with a non-existent ID |
| `405` | Method Not Allowed | HTTP verb not supported on this endpoint | Test wrong method (DELETE on a read-only endpoint) |
| `409` | Conflict | Request conflicts with server state | Test creating a duplicate resource |
| `422` | Unprocessable Entity | Syntactically correct but semantically invalid | Test with invalid values (negative age, wrong email format) |
| `429` | Too Many Requests | Rate limit exceeded | Test rate limiting behaviour |

#### 5xx — Server Errors
The request may have been valid but the server failed to process it.

| Code | Name | Meaning | Testing Tip |
|------|------|---------|-------------|
| `500` | Internal Server Error | Generic server failure | Look for unhandled exceptions |
| `502` | Bad Gateway | Upstream server returned an invalid response | Infrastructure/proxy issues |
| `503` | Service Unavailable | Server temporarily overloaded or down | Test circuit breakers |
| `504` | Gateway Timeout | Upstream server didn't respond in time | Test timeouts in integration scenarios |

---

### 2.3 Request & Response Structure

Every HTTP interaction has two parts: a **request** (client → server) and a **response** (server → client).

#### HTTP Request Structure

```
METHOD /path HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer <token>

{
  "body": "goes here"
}
```

- **Request line**: method + path + HTTP version
- **Headers**: key-value metadata about the request
- **Body**: the payload (only for POST, PUT, PATCH — not GET or DELETE)

#### HTTP Response Structure

```
HTTP/1.1 200 OK
Content-Type: application/json
X-Request-Id: abc-123

{
  "id": 1,
  "name": "Kasun Perera"
}
```

- **Status line**: HTTP version + status code + reason phrase
- **Headers**: metadata about the response
- **Body**: the returned data (JSON, XML, HTML, etc.)

---

### 2.4 Headers

Headers carry metadata. These are the ones you will encounter most as an SDET.

#### Request Headers

| Header | Purpose | Example |
|--------|---------|---------|
| `Content-Type` | Format of the request body | `application/json` |
| `Accept` | Format the client wants in the response | `application/json` |
| `Authorization` | Authentication credentials | `Bearer eyJhbG...` |
| `X-Request-ID` | Unique ID for tracing the request | `X-Request-ID: abc-123` |
| `Cache-Control` | Caching instructions | `no-cache` |
| `User-Agent` | Identifies the client software | `PostmanRuntime/7.32` |

#### Response Headers

| Header | Purpose | Example |
|--------|---------|---------|
| `Content-Type` | Format of the response body | `application/json; charset=utf-8` |
| `X-RateLimit-Remaining` | How many requests you have left | `X-RateLimit-Remaining: 99` |
| `Location` | URL of newly created resource | `Location: /users/42` |
| `WWW-Authenticate` | Auth method required | `WWW-Authenticate: Bearer` |
| `Retry-After` | When to retry after a 429/503 | `Retry-After: 60` |

---

## 3. SOAP

### 3.1 What is SOAP?

SOAP (Simple Object Access Protocol) is a protocol for exchanging structured information using XML. It predates REST and is common in enterprise and financial systems.

Key characteristics:
- Uses **XML exclusively** for both requests and responses
- Always uses **POST** as the HTTP method (even for reads)
- Has a formal contract called a **WSDL** (Web Services Description Language) that describes all available operations
- Built-in **WS-Security** support — strong authentication and message integrity
- Errors are returned as **SOAP Faults** (not HTTP status codes)

### 3.2 SOAP Request Structure

Every SOAP request is wrapped in an **envelope** with a header and body.

```xml
POST /UserService HTTP/1.1
Host: api.example.com
Content-Type: text/xml; charset=utf-8
SOAPAction: "getUser"

<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope
  xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:usr="http://example.com/users">

  <soapenv:Header>
    <wsse:Security>
      <wsse:UsernameToken>
        <wsse:Username>testuser</wsse:Username>
        <wsse:Password>testpass</wsse:Password>
      </wsse:UsernameToken>
    </wsse:Security>
  </soapenv:Header>

  <soapenv:Body>
    <usr:GetUserRequest>
      <usr:UserId>12345</usr:UserId>
    </usr:GetUserRequest>
  </soapenv:Body>

</soapenv:Envelope>
```

#### SOAP Fault (error response)

```xml
<soapenv:Envelope>
  <soapenv:Body>
    <soapenv:Fault>
      <faultcode>soapenv:Client</faultcode>
      <faultstring>User not found</faultstring>
      <detail>
        <errorCode>USER_404</errorCode>
      </detail>
    </soapenv:Fault>
  </soapenv:Body>
</soapenv:Envelope>
```

### 3.3 When to use SOAP

SOAP is typically used in banking, healthcare, telecoms, and legacy enterprise systems — any domain where formal contracts, strong security, and auditability matter more than developer convenience.

---

## 4. REST

### 4.1 What is REST?

REST (Representational State Transfer) is an architectural style, not a protocol. It uses standard HTTP methods to perform operations on resources.

Key principles:
- **Stateless**: every request contains all the information needed; the server holds no session state
- **Resource-based**: everything is a resource with a unique URL (`/users/1`, `/orders/99`)
- **Uses HTTP verbs** to express intent (GET = read, POST = create, etc.)
- **Returns JSON** in modern APIs (XML in older ones)

### 4.2 REST Endpoints & CRUD

A standard RESTful resource follows this pattern:

| Operation | HTTP Method | Endpoint | Body Required? |
|-----------|------------|---------|----------------|
| List all | `GET` | `/users` | No |
| Get one | `GET` | `/users/{id}` | No |
| Create | `POST` | `/users` | Yes |
| Replace | `PUT` | `/users/{id}` | Yes (full object) |
| Update | `PATCH` | `/users/{id}` | Yes (changed fields only) |
| Delete | `DELETE` | `/users/{id}` | No |

### 4.3 REST Request & Response Examples

#### GET — fetch a user

```http
GET /users/42 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
Accept: application/json
```

Response (`200 OK`):

```json
{
  "id": 42,
  "name": "Kasun Perera",
  "email": "kasun@example.com",
  "role": "engineer",
  "createdAt": "2024-01-15T08:30:00Z"
}
```

#### POST — create a user

```http
POST /users HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "name": "Kasun Perera",
  "email": "kasun@example.com",
  "role": "engineer"
}
```

Response (`201 Created`):

```json
{
  "id": 42,
  "name": "Kasun Perera",
  "email": "kasun@example.com",
  "role": "engineer",
  "createdAt": "2025-04-14T10:00:00Z"
}
```

#### PATCH — update only the email

```http
PATCH /users/42 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
Content-Type: application/json

{
  "email": "kasun.new@example.com"
}
```

Response (`200 OK`):

```json
{
  "id": 42,
  "name": "Kasun Perera",
  "email": "kasun.new@example.com",
  "role": "engineer",
  "createdAt": "2025-04-14T10:00:00Z"
}
```

#### DELETE — remove a user

```http
DELETE /users/42 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```

Response (`204 No Content`) — empty body, just the status code.

### 4.4 Common REST Problems

**Overfetching**: The endpoint returns more data than the client needs.

```
GET /users/42
→ Returns 40 fields including billing, address, preferences
→ You only needed the name for a navbar display
```

**Underfetching (N+1 Problem)**: One endpoint doesn't return enough, so you need multiple calls.

```
GET /users/42          → returns user (1 call)
GET /users/42/posts    → returns posts (1 call)
GET /posts/1/comments  → (1 call per post)
GET /posts/2/comments  → (1 call per post)
... N more calls
```

GraphQL solves both of these problems.

---

## 5. GraphQL

### 5.1 What is GraphQL?

GraphQL is a query language for APIs developed by Facebook in 2012 and open-sourced in 2015. Unlike REST, it uses a single endpoint and lets the client specify exactly what data it needs.

Key characteristics:
- **Single endpoint**: always `POST /graphql`
- **Strongly typed schema**: every field, type, and relationship is defined up front
- **Client-driven**: the client declares its data requirements — the server fulfils them exactly
- **Three operation types**: `query` (read), `mutation` (write), `subscription` (real-time)
- **Introspection**: you can query the schema itself to discover what's available

### 5.2 Query — Reading Data

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    name
    email
    posts {
      title
      createdAt
    }
  }
}
```

Variables (sent alongside the query):

```json
{
  "id": "user_001"
}
```

Response:

```json
{
  "data": {
    "user": {
      "name": "Kasun Perera",
      "email": "kasun@example.com",
      "posts": [
        {
          "title": "My first post",
          "createdAt": "2025-01-10"
        }
      ]
    }
  }
}
```

### 5.3 Mutation — Writing Data

```graphql
mutation CreatePost($input: PostInput!) {
  createPost(input: $input) {
    id
    title
    author {
      name
    }
  }
}
```

Variables:

```json
{
  "input": {
    "title": "GraphQL is great",
    "body": "Here is why..."
  }
}
```

Response:

```json
{
  "data": {
    "createPost": {
      "id": "post_123",
      "title": "GraphQL is great",
      "author": {
        "name": "Kasun Perera"
      }
    }
  }
}
```

### 5.4 Subscription — Real-time Data

Subscriptions use WebSockets. The client sends a subscription query and the server pushes events as they happen.

```graphql
subscription OnNewMessage($roomId: ID!) {
  messageAdded(roomId: $roomId) {
    id
    text
    sender {
      name
    }
    sentAt
  }
}
```

The server then pushes events continuously:

```json
{
  "data": {
    "messageAdded": {
      "id": "msg_456",
      "text": "Hello!",
      "sender": { "name": "Asel" },
      "sentAt": "2025-04-14T10:30:00Z"
    }
  }
}
```

### 5.5 GraphQL Error Responses

GraphQL errors are **not** returned as 4xx or 5xx HTTP status codes. They are embedded in the response body under an `errors` array, while the HTTP status is still `200 OK`.

```json
{
  "data": null,
  "errors": [
    {
      "message": "User not found",
      "locations": [{ "line": 2, "column": 3 }],
      "path": ["user"],
      "extensions": {
        "code": "NOT_FOUND"
      }
    }
  ]
}
```

Partial errors are also possible — some fields resolve, others fail:

```json
{
  "data": {
    "user": {
      "name": "Kasun Perera",
      "posts": null
    }
  },
  "errors": [
    {
      "message": "Could not fetch posts: timeout",
      "path": ["user", "posts"]
    }
  ]
}
```

### 5.6 The HTTP 200 Trap

> This is the single most important thing for an SDET to know about GraphQL.

In REST, you assert on HTTP status codes: `200` = pass, `404` = fail, `500` = fail.

In GraphQL, **you cannot rely on the HTTP status code**. The server almost always returns `200 OK` even when something went wrong. You must **always inspect the response body**.

```
REST test logic:   assert statusCode == 200  →  enough
GraphQL test logic: assert statusCode == 200  →  NOT enough
                    assert res.errors is undefined  →  required
                    assert res.data is not null  →  required
```

---

## 6. API Comparison Table

| Feature | SOAP | REST | GraphQL |
|---------|------|------|---------|
| Data format | XML only | JSON, XML, etc. | JSON always |
| Endpoints | One per operation | One per resource | Single `/graphql` |
| HTTP method | POST only | GET, POST, PUT, PATCH, DELETE | POST (mostly) |
| Data fetching | Fixed | Fixed (over/underfetch risk) | Exact fields requested |
| Type system | Strict (WSDL/XSD) | Optional (OpenAPI/Swagger) | Built-in schema |
| Real-time | None built-in | Polling or SSE | Native subscriptions |
| Error handling | SOAP Faults in body | HTTP status codes | `errors` array in body (always HTTP 200) |
| Self-documenting | WSDL file | OpenAPI/Swagger (optional) | Introspection (built-in) |
| Best for | Banking, healthcare, enterprise | Most web/mobile apps, public APIs | Mobile apps, complex UIs, multiple clients |

---

## 7. Testing APIs — General Strategy

### 7.1 Testing Layers

Good API test coverage spans multiple layers:

1. **Contract testing** — does the API response match the agreed schema/spec?
2. **Functional testing** — does it return correct data for valid inputs?
3. **Negative testing** — does it handle invalid/missing inputs gracefully?
4. **Authentication testing** — does it reject unauthenticated requests?
5. **Authorisation testing** — can User A access User B's data? (privilege escalation)
6. **Performance testing** — does it respond within acceptable time under load?
7. **Security testing** — injection attacks, rate limiting, data exposure

### 7.2 Types of Test Cases

For each API endpoint or GraphQL operation, cover these categories:

| Category | What to test | Expected result |
|---------|-------------|-----------------|
| Happy path | Valid inputs, valid auth | `2xx`, correct data returned |
| Missing required fields | Omit a required body field | `400 Bad Request` (REST) or error in `errors[]` (GraphQL) |
| Invalid data types | Send string where integer expected | `400` or `422` |
| Non-existent resource | Request ID that doesn't exist | `404` (REST) or `NOT_FOUND` error (GraphQL) |
| Unauthorised | No auth header | `401` |
| Forbidden | Valid token but wrong role | `403` |
| Duplicate resource | Create same resource twice | `409` |
| Boundary values | Max length strings, zero, negative numbers | Varies — document expected behaviour |
| SQL/NoSQL injection | `' OR '1'='1` in string fields | `400` — input should be sanitised |
| Oversized payload | Send very large body | `413 Payload Too Large` |

---

## 8. Testing REST APIs

### 8.1 Postman — REST Setup

1. **Create a new collection** — group all endpoints for one API together
2. **Set up an environment** with variables:
   ```
   base_url   = https://api.example.com
   auth_token = (set via pre-request script or manually)
   user_id    = 42
   ```
3. **Create requests** using the environment variables:
   ```
   GET {{base_url}}/users/{{user_id}}
   Authorization: Bearer {{auth_token}}
   ```
4. **Write test scripts** in the Tests tab
5. **Run via Collection Runner** or Newman CLI

### 8.2 Common REST Assertions

```javascript
// Status code
pm.test("Status is 200", () => pm.response.to.have.status(200));
pm.test("Status is 201", () => pm.response.to.have.status(201));
pm.test("Status is 404", () => pm.response.to.have.status(404));

const res = pm.response.json();

// Field presence and types
pm.test("ID is a number",     () => pm.expect(res.id).to.be.a("number"));
pm.test("Name is a string",   () => pm.expect(res.name).to.be.a("string"));
pm.test("Email format valid", () => pm.expect(res.email).to.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/));
pm.test("Array not empty",    () => pm.expect(res.items).to.have.length.above(0));
pm.test("Has required keys",  () => pm.expect(res).to.have.keys(["id", "name", "email"]));

// Response time
pm.test("Response under 2s",  () => pm.expect(pm.response.responseTime).to.be.below(2000));

// Content-Type header
pm.test("Content-Type is JSON", () => pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json"));

// Store response value for chained requests
pm.environment.set("created_user_id", res.id);
```

---

## 9. Testing GraphQL APIs

### 9.1 GraphQL-Specific Test Cases

Beyond the standard API test cases, GraphQL has unique scenarios:

| Test | Why it matters |
|------|---------------|
| Assert `errors` is undefined on success | HTTP 200 is not enough — must check body |
| Assert `data` is not null on success | Partial failures return `data: null` |
| Assert `errors[0].message` on failure | Validate error messages are descriptive |
| Introspection disabled in production | Introspection exposes your entire schema to attackers |
| Deep/nested query rejection | `user → friends → friends → friends…` (10 levels) should be blocked |
| Query complexity limits | Very wide queries (100 fields) should be rate-limited or rejected |
| Batch query limits | Multiple operations in one request should respect rate limits |
| Subscription connects and receives events | WebSocket connection established, events arrive |

### 9.2 Apollo Sandbox Guide

Apollo Sandbox is the fastest way to explore a GraphQL API. No installation required.

**URL**: `studio.apollographql.com/sandbox`

**Setup steps:**

1. Paste your GraphQL endpoint in the top-left Endpoint field
2. Apollo auto-runs an introspection query and loads the schema
3. If the endpoint requires auth, click Headers and add:
   ```
   Authorization: Bearer your-token-here
   ```
4. Browse the schema in the left sidebar (book icon)
5. Click any field to add it to your query automatically
6. Use variables instead of hardcoded values in queries:
   ```graphql
   query GetUser($id: ID!) {
     user(id: $id) {
       name
       email
     }
   }
   ```
   Variables pane:
   ```json
   { "id": "user_001" }
   ```
7. Run with `Ctrl+Enter`

**Keyboard shortcuts:**

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Run query |
| `Ctrl+Space` | Trigger autocomplete |
| `Shift+Ctrl+P` | Prettify/format query |
| `Ctrl+F` | Search schema |

### 9.3 Postman — GraphQL Setup

1. Create a new HTTP request in Postman
2. Set method to `POST`
3. Enter your GraphQL endpoint URL
4. Go to **Body → select GraphQL** (not raw JSON)
5. Click **Use GraphQL Introspection** to load the schema
6. Write your query in the Query pane
7. Add variables in the GraphQL Variables pane
8. Set headers under the Headers tab:
   ```
   Authorization: Bearer {{auth_token}}
   Content-Type: application/json
   ```

Postman wraps your query automatically into the correct JSON format:
```json
{
  "query": "query GetUser($id: ID!) { user(id: $id) { name email } }",
  "variables": { "id": "user_001" }
}
```

> If introspection is disabled on the server, import the schema manually via APIs → Schema (SDL or JSON format).

### 9.4 Postman Test Scripts for GraphQL

```javascript
const res = pm.response.json();

// Always check these three for every GraphQL request
pm.test("HTTP status is 200",    () => pm.response.to.have.status(200));
pm.test("No GraphQL errors",     () => pm.expect(res.errors).to.be.undefined);
pm.test("Data is not null",      () => pm.expect(res.data).to.not.be.null);

// Field type assertions
pm.test("Name is a string",      () => pm.expect(res.data.user.name).to.be.a("string"));
pm.test("ID is a string",        () => pm.expect(res.data.user.id).to.be.a("string"));
pm.test("Posts is an array",     () => pm.expect(res.data.user.posts).to.be.an("array"));
pm.test("Array not empty",       () => pm.expect(res.data.user.posts).to.have.length.above(0));

// Value assertions
pm.test("Has required keys",     () => pm.expect(res.data.user).to.have.keys(["id", "name", "email"]));
pm.test("Response under 2s",     () => pm.expect(pm.response.responseTime).to.be.below(2000));

// Negative test — asserting error is present
pm.test("Error returned for invalid ID", () => {
  pm.expect(res.errors).to.be.an("array");
  pm.expect(res.errors[0].message).to.include("not found");
});
pm.test("Data is null on error", () => pm.expect(res.data).to.be.null);
```

### 9.5 Newman — CI/CD Integration

Newman is Postman's CLI runner. It lets you execute your Postman collections as part of a build pipeline.

**Installation:**

```bash
npm install -g newman
npm install -g newman-reporter-htmlextra  # optional — nice HTML reports
```

**Basic run:**

```bash
newman run my-graphql-tests.json \
  --environment staging.json
```

**With JUnit output (for Jenkins/GitHub Actions):**

```bash
newman run my-graphql-tests.json \
  --environment staging.json \
  --reporters cli,junit \
  --reporter-junit-export results/test-results.xml
```

**With HTML report:**

```bash
newman run my-graphql-tests.json \
  --environment staging.json \
  --reporters htmlextra \
  --reporter-htmlextra-export reports/report.html
```

**GitHub Actions example:**

```yaml
- name: Run API Tests
  run: |
    newman run collections/graphql-tests.json \
      --environment environments/staging.json \
      --reporters cli,junit \
      --reporter-junit-export test-results.xml

- name: Publish Test Results
  uses: dorny/test-reporter@v1
  with:
    name: API Tests
    path: test-results.xml
    reporter: java-junit
```

**Dynamic auth token via pre-request script:**

```javascript
pm.sendRequest({
  url: pm.environment.get("base_url") + "/auth/token",
  method: "POST",
  header: { "Content-Type": "application/json" },
  body: {
    mode: "raw",
    raw: JSON.stringify({
      username: pm.environment.get("test_user"),
      password: pm.environment.get("test_pass")
    })
  }
}, (err, res) => {
  const token = res.json().access_token;
  pm.environment.set("auth_token", token);
});
```

---

## 10. Tool Comparison: Apollo vs Postman

| | Apollo Sandbox | Postman |
|-|---------------|---------|
| **Best for** | Exploration, schema discovery | Automation, team collections, CI |
| **Installation** | None (browser-based) | Desktop app or web |
| **Account required** | No | Yes (free tier available) |
| **Schema browsing** | Excellent — first-class feature | Good — via introspection |
| **Test scripting** | No | Yes — JavaScript in Tests tab |
| **Environment variables** | Basic | Full support |
| **CI/CD integration** | No | Yes — via Newman CLI |
| **Team collaboration** | Share URL | Shared workspaces and collections |
| **Subscriptions** | Yes — WebSocket support built-in | Limited |

---

## 11. Recommended Workflow for SDETs

```
Step 1 — Explore (Apollo Sandbox)
  └── Paste endpoint URL
  └── Browse schema to discover all queries/mutations
  └── Draft queries, confirm happy path response shapes
  └── Identify all fields and their types for assertions

Step 2 — Automate (Postman)
  └── Create a Collection per API/service
  └── Set up Environments: dev, staging, prod
  └── Paste validated queries from Apollo
  └── Write test scripts for:
        - Happy path (data present, types correct)
        - Negative cases (errors array, null data)
        - Auth (401 for missing token, 403 for wrong role)
        - Performance (response time under threshold)

Step 3 — Integrate (Newman + CI)
  └── Export Collection and Environment files
  └── Commit to the same Git repo as your codebase
  └── Add Newman step to CI pipeline
  └── Gate deployments on test pass
  └── Publish JUnit/HTML reports to your test dashboard
```

---

## 12. Quick Reference Cheatsheets

### 12.1 HTTP Status Codes Cheatsheet

```
2xx  Success
  200  OK               — standard success
  201  Created           — POST created a resource
  204  No Content        — DELETE succeeded, no body

4xx  Client Error
  400  Bad Request       — malformed input
  401  Unauthorized      — missing or bad credentials
  403  Forbidden         — authenticated but not allowed
  404  Not Found         — resource does not exist
  409  Conflict          — duplicate or state conflict
  422  Unprocessable     — valid syntax, invalid semantics
  429  Too Many Requests — rate limit hit

5xx  Server Error
  500  Internal Error    — generic server failure
  502  Bad Gateway       — upstream failure
  503  Service Unavail.  — server overloaded or down
  504  Gateway Timeout   — upstream timed out
```

### 12.2 Postman GraphQL Assertions Cheatsheet

```javascript
const res = pm.response.json();

// Core 3 — always include these
pm.test("HTTP 200",        () => pm.response.to.have.status(200));
pm.test("No errors",       () => pm.expect(res.errors).to.be.undefined);
pm.test("Data not null",   () => pm.expect(res.data).to.not.be.null);

// Type checks
pm.expect(res.data.user.name).to.be.a("string");
pm.expect(res.data.user.age).to.be.a("number");
pm.expect(res.data.users).to.be.an("array");

// Value checks
pm.expect(res.data.users).to.have.length.above(0);
pm.expect(res.data.user).to.have.keys(["id", "name", "email"]);
pm.expect(res.data.user.email).to.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);

// Performance
pm.expect(pm.response.responseTime).to.be.below(2000);

// Error scenario
pm.expect(res.errors).to.be.an("array");
pm.expect(res.errors[0].message).to.include("not found");
```

### 12.3 GraphQL Operation Types Cheatsheet

```graphql
# READ — query
query OperationName($var: Type!) {
  fieldName(arg: $var) {
    field1
    field2
    nestedObject {
      nestedField
    }
  }
}

# WRITE — mutation
mutation OperationName($input: InputType!) {
  mutationField(input: $input) {
    returnedField1
    returnedField2
  }
}

# REAL-TIME — subscription (over WebSocket)
subscription OperationName($id: ID!) {
  eventName(id: $id) {
    eventField1
    eventField2
  }
}
```

---

## 13. Public APIs for Practice

| API | Type | URL | Auth needed? | Good for |
|-----|------|-----|-------------|---------|
| Star Wars API (SWAPI) | GraphQL | `swapi-graphql.netlify.app/.netlify/functions/index` | No | GraphQL queries, nested data |
| Rick and Morty API | GraphQL | `rickandmortyapi.com/graphql` | No | Pagination, filtering |
| GitHub API | REST + GraphQL | `api.github.com` | Yes (free token) | Real-world REST and GraphQL |
| JSONPlaceholder | REST | `jsonplaceholder.typicode.com` | No | REST CRUD, quick experiments |
| Reqres | REST | `reqres.in` | No | Auth flows, user CRUD |
| httpbin | REST | `httpbin.org` | No | HTTP method and header testing |
| OpenWeatherMap | REST | `openweathermap.org/api` | Yes (free key) | Real API with real data |

---

*Last updated: April 2025*
*Author: Personal reference — feel free to contribute and expand*
