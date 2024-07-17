from fastapi import APIRouter
from models.blog import BlogModel,UpdateBlogModel
from config.config import blog_collection
import datetime
from serialize.blog import decodeAllBlog,decodeBlog
from bson import ObjectId
blog_root=APIRouter()


#post request
@blog_root.post("/new/blog")
def NewBlog(doc:BlogModel):
    doc=dict(doc)#convert doc to dictionary
    current_date=datetime.datetime.today()
    doc["date"]=current_date
    res=blog_collection.insert_one(doc)
    print(res)

    doc_id=res.inserted_id #res contains the id of the inserted document

    return {"message":"New Blog Created","doc_id":str(doc_id)}

@blog_root.get("/blog")
def AllBlog():
    all_blog=blog_collection.find()
    return decodeAllBlog(all_blog)

@blog_root.get("/blog/{id}")
def indiv_blog(id:str):
    blog=blog_collection.find_one({"_id":ObjectId(id)})
    return decodeBlog(blog)


@blog_root.put("/blog/{id}")
def update(id:str,doc:UpdateBlogModel):
    doc=dict(doc)
    blog=blog_collection.update_one({"_id":ObjectId(id)},{"$set":doc})
    return {"message":"Blog Updated"}


# update blog 
@blog_root.patch("/update/{_id}")
def UpdateBlog(_id: str , doc:UpdateBlogModel):
    req = dict(doc.model_dump(exclude_unset=True))  #in the response  dump all the null values
    blog_collection.find_one_and_update(
       {"_id" : ObjectId(_id) } ,
       {"$set" : req}
    )

    return {
        "status" : "ok" ,
        "message" : "blog updated successfully"
    }


@blog_root.delete("/blog/{id}")
def delete(id:str):
    blog=blog_collection.delete_one({"_id":ObjectId(id)})
    return {"message":"Blog Deleted"}   

