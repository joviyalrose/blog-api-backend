
import json
import os
from flask import Flask, request, jsonify
import graphene
from nanoid import generate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db_1.json")   # persistent JSON file for posts/comments

if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        json.dump({"posts": [], "comments": []}, f, indent=2)
def read_db():
    with open(DB_PATH, "r") as f:
        return json.load(f)

def write_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)

# GraphQL Types written here
class CommentType(graphene.ObjectType):
    id = graphene.ID()
    postId = graphene.ID()
    text = graphene.String()
    author = graphene.String()

class PostType(graphene.ObjectType):
    id = graphene.ID()
    title = graphene.String()
    description = graphene.String()
    publish_date = graphene.String()
    author = graphene.String()
    comments = graphene.List(CommentType)
class Query(graphene.ObjectType):
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.ID(required=True))

    def resolve_posts(root, info):
        db = read_db()
        posts = db["posts"]
        comments = db["comments"]
        result = []
        for p in posts:
            p_copy = p.copy()
            # attach comments that belong to this post
            p_copy["comments"] = [c for c in comments if c["postId"] == p["id"]]
            result.append(p_copy)
        return result

    def resolve_post(root, info, id):
        db = read_db()
        p = next((x for x in db["posts"] if x["id"] == id), None)
        if not p:
            return None
        p_copy = p.copy()
        p_copy["comments"] = [c for c in db["comments"] if c["postId"] == id]
        return p_copy
class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        publish_date = graphene.String()
        author = graphene.String()

    post = graphene.Field(PostType)

    def mutate(root, info, title, description=None, publish_date=None, author=None):
        db = read_db()
        pid = generate(size=8)
        post = {
            "id": pid,
            "title": title,
            "description": description or "",
            "publish_date": publish_date or "",
            "author": author or ""
        }
        db["posts"].append(post)
        write_db(db)
        post["comments"] = []
        return CreatePost(post=post)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        publish_date = graphene.String()
        author = graphene.String()

    post = graphene.Field(PostType)

    def mutate(root, info, id, title=None, description=None, publish_date=None, author=None):
        db = read_db()
        p = next((x for x in db["posts"] if x["id"] == id), None)
        if not p:
            raise Exception("Post not found")
        if title is not None: p["title"] = title
        if description is not None: p["description"] = description
        if publish_date is not None: p["publish_date"] = publish_date
        if author is not None: p["author"] = author
        write_db(db)
        p_copy = p.copy()
        p_copy["comments"] = [c for c in db["comments"] if c["postId"] == id]
        return UpdatePost(post=p_copy)

class CreateComment(graphene.Mutation):
    class Arguments:
        postId = graphene.ID(required=True)
        text = graphene.String(required=True)
        author = graphene.String()

    comment = graphene.Field(CommentType)
    def mutate(root, info, postId, text, author=None):
        db = read_db()
        # ensure post exists
        if not any(p["id"] == postId for p in db["posts"]):
            raise Exception("Post not found")
        cid = generate(size=8)
        comment = {"id": cid, "postId": postId, "text": text, "author": author or ""}
        db["comments"].append(comment)
        write_db(db)
        return CreateComment(comment=comment)

class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    ok = graphene.Boolean()
    def mutate(root, info, id):
        db = read_db()
        before = len(db["comments"])
        db["comments"] = [c for c in db["comments"] if c["id"] != id]
        write_db(db)
        return DeleteComment(ok=len(db["comments"]) < before)

class Mutation(graphene.ObjectType):
    createPost = CreatePost.Field()
    updatePost = UpdatePost.Field()
    createComment = CreateComment.Field()
    deleteComment = DeleteComment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, auto_camelcase=False)

# Flask app and endpoints are written here
app = Flask(__name__)

@app.route("/graphql", methods=["POST"])
def graphql_endpoint():
    payload = request.get_json(force=True)
    query = payload.get("query")
    variables = payload.get("variables")
    result = schema.execute(query, variable_values=variables)
    response = {}
    response["data"] = result.data if result.data is not None else None
    if result.errors:
        errors_out = []
        for err in result.errors:
            err_obj = {"message": str(err)}
            try:
                if hasattr(err, "locations") and err.locations:
                    err_obj["locations"] = [ {"line": loc.line, "column": loc.column} for loc in err.locations ]
            except Exception:
                pass
            try:
                if hasattr(err, "path") and err.path:
                    err_obj["path"] = err.path
            except Exception:
                pass
            errors_out.append(err_obj)
        response["errors"] = errors_out

    return jsonify(response)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Blog GraphQL API running. POST GraphQL to /graphql"})

if __name__ == "__main__":
    app.run(debug=True, port=4000)
