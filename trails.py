import os
import pymongo
if os.path.exists("env.py"):
    import env


MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "TrailMixer"
COLLECTION = "trails"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB: %s") % e


def show_menu():
    print("")
    print("1. Add a trail")
    print("2. Find a trail by name")
    print("3. Edit a trail")
    print("4. Delete a trail")
    print("5. Exit")

    option = input("Enter option: ")
    return option


def get_record():
    print("")
    first = input("Enter first name > ")
    last = input("Enter last name > ")

    try:
        doc = coll.find_one({"first": first.lower(), "last": last.lower()})
    except:
        print("Error accessing the database")

    if not doc:
        print("")
        print("Error! No results found.")

    return doc


def add_record():
    print("")
    title = input("Enter trail title > ")
    address = input("Enter address > ")
    description = input("Enter description > ")
    difficulty = input("Enter difficulty > ")
    directions = input("Enter directions > ")
    elevation = input("Enter elevation > ")
    image = input("Upload image > ")
    length = input("Enter length > ")
    time = input("Enter time taken > ")
    type = input("Enter type of trail > ")

    new_doc = {
        "title": trail.title(),
        "address": trail.address(),
        "description": description,
        "difficulty": difficulty,
        "directions": directions,
        "elevation": elevation,
        "image": image,
        "length": length
        "time": time,
        "type": type,
    }

    try:
        coll.insert(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the database")


def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            print("You have selected option 2")
        elif option == "3":
            print("You have selected option 3")
        elif option == "4":
            print("You have selected option 4")
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid option")
        print("")


conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()