from pymongo.mongo_client import MongoClient
uri = "mongodb+srv://admin-ritushree:Mo4gS9UnLrFY1J0Y@cluster0.s6k4ce2.mongodb.net/?appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri)
db=client.Blogging #to create a database
blog_collection=db["blog"]
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)