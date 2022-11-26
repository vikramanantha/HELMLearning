# Vikram Anantha
# Mar 9 2021
# Adding / Editing Tags
# HELM Learning

# Project Continuous

from helper_functions import *
cnx, cursor = start()
class_name = input("Classes to add tags for? ")
cursor.execute("SELECT id FROM classes WHERE short_name = '{}'".format(class_name))
try:
    class_id = cursor.fetchall()[0][0]
except:
    print("There is no such class!")
    quit()
    

print("Here is a list of all tags\n")
cursor.execute("SELECT id, tag FROM tags")
tags = cursor.fetchall()
for i in tags:
    print(" {} | {} ".format(*i))
print("\nType the number of the tag (or type !new to create a new tag)")
for i in range(5):
    tag_num = input("¬¬ ")
    if tag_num == "!new":
        tag_name = input("What is the tag called? ")
        tag_name = tag_name[0].upper() + tag_name[1:].lower()
        cursor.execute("INSERT into tags (tag) VALUES ('{}')".format(tag_name))
        cursor.execute("SELECT id FROM tags WHERE tag = '{}'".format(tag_name))
        tag_num = cursor.fetchall()[0][0]
        cursor.execute("INSERT into classes_to_tags (class_id, tag_id) VALUES ('{}', '{}')".format(class_id, tag_num))
        continue
    if tag_num == "":
        break
    input("Connect class {} with tag {}?".format(class_id, tag_num))
    cursor.execute("INSERT into classes_to_tags (class_id, tag_id) VALUES ('{}', '{}')".format(class_id, tag_num))


stop(cnx, cursor)