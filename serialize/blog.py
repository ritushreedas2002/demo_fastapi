#serialise to json for all the get requests
#doc is the comming data from the database

#one blog
def decodeBlog(doc)->dict:
    return {
        "_id":str(doc["_id"]),
        "title":doc["title"],
        "content":doc["content"],
        "date":doc["date"],
        "author":doc["author"],
        "tags":doc["tags"] ,
        "date":doc["date"]
    }


#all blogs
def decodeAllBlog(doc)->list:
    return [decodeBlog(i) for i in doc]