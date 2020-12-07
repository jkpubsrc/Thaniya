#!/usr/bin/python3


import json

import mysql.connector




s = input()

data = json.loads(s)

dbName = data["dbName"]
dbUserName = data["dbUserName"]
dbPassword = data["dbPassword"]
dbPort = data["dbPort"]



con = None
try:
	con = mysql.connector.connect(host="localhost", port=dbPort, database=dbName, user=dbUserName, passwd=dbPassword)

	sqlQuery = "SELECT SUM(data_length) FROM information_schema.tables WHERE table_schema = '" + dbName + "';"

	cursor = con.cursor()
	cursor.execute(sqlQuery)
	records = cursor.fetchall()
	assert cursor.rowcount == 1

	nEstimatedSize = -1
	for row in records:
		nEstimatedSize = row[0]
		break

	print(nEstimatedSize)

finally:
	if con and con.is_connected():
		cursor.close()
		con.close()


