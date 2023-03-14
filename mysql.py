import MySQLdb

# Create a connection to the MySQL database
mydb = MySQLdb.connect(
  host="localhost",
  user="root",
  password="selva2002",
  database="haus"
)
mycursor = mydb.cursor()

# Read the binary data from the file
with open('img4.jpg', 'rb') as file:
    new_data = file.read()
    print(new_data)
# Define the update query
sql = "UPDATE builder SET image = %s WHERE id = %s"

# Set the values to insert into the query
val = (new_data, 3)  # Replace 1 with the ID of the row you want to update

# Execute the query with the values
mycursor.execute(sql, val)

# Commit the changes
mydb.commit()

# Print the number of records affected
print(mycursor.rowcount, "record(s) affected")