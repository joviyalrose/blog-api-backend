# Blog API Backend

## Blog API (GraphQL)

A lightweight blog service providing basic post and comment management through GraphQL.

### Features
- **createPost** — Create a blog post with `title`, `description`, `publish_date`, and `author`
- **updatePost** — Update post attributes using its ID
- **createComment** — Add a comment linked to a post
- **deleteComment** — Delete a comment by ID
- **posts** — Retrieve all posts along with their comments
- **post(id)** — Retrieve a single post with its comments

### How to Run
1. Clone the repository
2. Install dependencies using `pip install -r requirements.txt`
3. Run the application using `python3 blog_api.py` 
4. Access the API endpoints via browser or Postman

### Query format:
Create a Post
```
mutation {
  createPost(
    title: "Sample Post",
    description: "Example description",
    publish_date: "2025-12-06",
    author: "Joviyal"
  ) {
    post {
      id
      title
      author
    }
  }
}
```
Fetch Posts
```
query {
  posts {
    id
    title
    author
    comments {
      id
      text
    }
  }
}
```
**Note:**  
The application uses `db_1.json` as a lightweight JSON datastore.  
All API test data (posts and comments) is persisted here for simplicity and transparency during evaluation.

### GraphQL Endpoint:
http://127.0.0.1:5000/graphql

## Project Structure 

```
blog-api-backend/
├── blog_api.py
├── db_1.json
├── requirements.txt
└── README.md
```

