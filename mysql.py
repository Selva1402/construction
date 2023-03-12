with open('F:/castle/static/img3.jpg', 'rb') as file:
    new_image_data = file.read()
import MySQLdb

# Connect to the database
cnx = MySQLdb.connect(user='root', password='selva2002',
                              host='localhost', database='haus')

# Prepare the UPDATE statement
update_query = "UPDATE builder SET image = %s WHERE id = %s"

# Execute the UPDATE statement with the new image data
cursor = cnx.cursor()
cursor.execute(update_query, (new_image_data, 1))
cnx.commit()