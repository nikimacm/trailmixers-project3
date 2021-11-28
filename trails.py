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
    title = input("Enter trail title > ")
    address = input("Enter address > ")

    try:
        doc = coll.find_one({"title": first.lower(), "address": last.lower()})
    except:
        print("Error accessing the database")

    if not doc:
        print("")
        print("Error! No results found.")

    return doc


def add_record():
    print("")
    trail_title = input("Enter trail title > ")
    trail_address = input("Enter address > ")
    trail_description = input("Enter description > ")
    trail_difficulty = input("Enter difficulty > ")
    trail_directions = input("Enter directions > ")
    trail_elevation = input("Enter elevation > ")
    trail_image = input("Upload image > ")
    trail_length = input("Enter length > ")
    trail_time = input("Enter time taken > ")
    trail_type = input("Enter type of trail > ")

    new_doc = {
        "trail_title": title.lower(),
        "trail_address": address.lower(),
        "trail_description": description,
        "trail_difficulty": difficulty,
        "trail_directions": directions,
        "trail_elevation": elevation,
        "trail_image": image,
        "trail_length": length,
        "trail_time": time,
        "ttrail_ype": type
    }

    try:
        coll.insert(new_doc)
        print("")
        print("Document inserted")
    except:
        print("Error accessing the database")


def find_record():
    doc = get_record()
    if doc:
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())


def edit_record():
    doc = get_record()
    if doc:
        update_doc = {}
        print("")
        for k, v in doc.items():
            if k != "_id":
                update_doc[k] = input(k.capitalize() + " [" + v + "] > ")

                if update_doc[k] == "":
                    update_doc[k] = v

        try:
            coll.update_one(doc, {"$set": update_doc})
            print("")
            print("Document updated")
        except:
            print("Error accessing the database")


def delete_record():
    doc = get_record()
    if doc:
        print("")
        for k, v in doc.items():
            if k != "_id":
                print(k.capitalize() + ": " + v.capitalize())

        print("")
        confirmation = input("Is this the document you want to delete?\nY or N > ")
        print("")

        if confirmation.lower() == "y":
            try:
                coll.remove(doc)
                print("Document deleted!")
            except:
                print("Error accessing the database")
        else:
            print("Document not deleted")


def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            edit_record()
        elif option == "4":
            delete_record()
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid option")
        print("")


conn = mongo_connect(MONGO_URI)
coll = conn[DATABASE][COLLECTION]
main_loop()