# NuFlights Technical Assessment — Joviyal Rose A.

This repository contains my completed solutions for the NuFlights technical assignments.  
Both tasks were implemented using Python, Flask, and GraphQL, with a focus on clarity, correctness, and simplicity.

---

## Assignment 1 — Blog API (GraphQL)

A lightweight blog service providing basic post and comment management through GraphQL.

### Features
- **createPost** — Create a blog post with `title`, `description`, `publish_date`, and `author`
- **updatePost** — Update post attributes using its ID
- **createComment** — Add a comment linked to a post
- **deleteComment** — Delete a comment by ID
- **posts** — Retrieve all posts along with their comments
- **post(id)** — Retrieve a single post with its comments

### How to Run

- source .venv/bin/activate
- python3 blog_api.py

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


## Assignment 2 — XML Query Service (GraphQL)
A simple GraphQL interface to query values from an XML document shaped according to the OrderViewRS.xsd schema.
A sample XML file is included under sample_xml/.

### Features:
1. rawXml — Returns the complete XML document as a string.
2. queryXml(path, attribute)
3. Accepts a dot-separated path to any element in the XML.
4. Optionally extracts attribute values.
5. Works with nested and repeated XML structures.

### How to Run:

- source .venv/bin/activate
- python3 xml_query_service.py

### Query format:
Query nested XML elements
```
query {
  queryXml(path: "OrderViewRS.Response.Orders.Order.Customer.Name") {
    result
    note
  }
}
```
Query XML attributes
```
query {
  queryXml(
    path: "OrderViewRS.Response.Orders.Order",
    attribute: "OrderID"
  ) {
    result
    note
  }
}
```

### GraphQL Endpoint:
http://127.0.0.1:5000/graphql

## Project Structure 

```
NuFlights_Assessment_Joviyal/
├── blog_api.py
├── xml_query_service.py
├── db_1.json
├── requirements.txt
├── sample_xml/
│   └── OrderViewRS_sample.xml
└── README.md
```

