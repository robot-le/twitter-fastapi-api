# Good old twitter

The microblog app with text only posts, lists of likes and nothing extra.

- version = v1
- prefix = /api/v1

### Auth
todo: put auth to separate service

**POST /auth/login**
- Description: Obtain an authentication JWT token
- Request body:
  - username
  - password
- Response: JWT token

**DELETE /auth/logout**
- Description: Invalidate the authentication JWT token
- Response: Success or failure message

**POST ? GET /auth/reset-password**
- Description: Reset user password
- Request body:
  - email
- Response: Success or failure message

**POST /auth/refresh-token**
- Description: Refresh JWT token

### Users
**GET /users/{user_id}**
- Description: Retrieve user details
- Response: User object

**GET /users**
- Description: Retrieve a list of users
- Query params:
  - page (optional)
  - limit (optional, max=100)
- Response: Array of user objects

**GET /users/{user_id}/followers**
- Description: Retrieve followers of the specified user
- Query params:
  - page (optional)
  - limit (optional, max=100)
- Response: Array of user objects

**GET /users/{user_id}/following**
- Description: Retrieve users followed by the specified user
- Query params:
  - page (optional)
  - limit (optional, max=100)
- Response: Array of user objects

**POST /users**
- Description: Create a new user
- Request body:
  - username
  - email
  - password
- Response: Created user object

**PATCH /users/{user_id}**
- Description: Update user information
- Request body:
  - fields to update
- Response: Updated user object

**DELETE /users/{user_id}**
- Description: Delete a user
- Response: Success or failure message

**POST /users/{user_id}/follow**
- Description: Follow a user
- Response: Success or failure message

**POST /users/{user_id}/unfollow**
- Description: Unfollow a user
- Response: Success or failure message

**GET /users/{user_id}/posts**
- Description: Retrieve posts created by the specified user
- Query params:
  - page (optional)
  - limit (optional, max=100)
- Response: Array of post objects

**GET /users/{user_id}/liked**
- Description: Retrieve posts, liked by specified user
- Query params:
  - page (optional)
  - limit (optional, max=100)
- Response: Array of post objects

### Posts
**GET /posts/{post_id}**
- Description: Retrieve a specific post
- Response: Post object

**DELETE /posts/{post_id}**
- Description: Delete a specific post
- Response: Success or failure message

**POST /posts**
- Description: Create a new post
- Request body:
  - body
- Response: Created post object

**POST /posts/{post_id}/repost**
- Description: Repost the post
- Response: Success or failure message

todo: delete repost?

**POST /posts/{post_id}/like**
- Description: Like the post (add to liked list)
- Response: Success or failure message

**DELETE /posts/{post_id}/like**
- Description: Remove like from the post
- Response: Success or failure message

### Feeds
**GET /explore**
- Description: Retrieve posts from users not followed by the current user
- Query params:
  - page (optional)
  - limit (optional, max=100)

**GET /search**
- Description: Search for posts or users
- Query params:
  - q (required) - Query string
  - entity (optional, default='posts') - Entity to search, either 'posts' or 'users'

**GET /feed**
- Description: Retrieve the current user's feed (posts from followed users)
- Query params:
  - page (optional)
  - limit (optional, max=100)

### Messages
todo: put messages to separate service with chats, and other stuff

**POST /messages/{user_id}**
- Description: Send a message to the specified user
- Request body:
  - message
- Response: Success or failure message

**GET /messages/{user_id}**
- Description: Retrieve all messages from the specified user
- Query params:
  - page (optional)
  - limit (optional, max=100)
- Response: Array of message objects
