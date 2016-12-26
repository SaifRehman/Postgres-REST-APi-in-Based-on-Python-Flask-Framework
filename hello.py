from flask import Flask, jsonify,request,abort
import os
import psycopg2
import json
import binascii
app = Flask(__name__)
port = int(os.getenv("PORT", 64781))
'''
################### This is for populating  table  ##########################
'''
@app.route('/Post', methods=['POST'])
def Post():
	if not request.json or not 'x' in request.json:
		abort
	if not request.json or not 'y' in request.json:
		abort
	if not request.json or not 'z' in request.json:
		abort
	if not request.json or not 'a' in request.json:
		abort
	x = request.json['x']
	y = request.json['y']
	z = request.json['z']
	a = request.json['a']
	try:
		conn = psycopg2.connect(database="dbname", user="username", password="password", host="10.72.6.143", port="5432")
		cur = conn.cursor()
		cur.execute("""INSERT INTO tablename (x, y, z,a)VALUES (%s, %s, %s, %s);""",(x, y, z,a))#sanitization prepared statement
		conn.commit()
		conn.close()
		return "Successfully inserted"
	except Exception as error:
		return error

@app.route('/CheckLogin', methods=['POST'])
def CheckLogin():
	if not request.json or not 'username' in request.json:
		abort
	username = request.json['username']
	try:
		conn = psycopg2.connect(database="database", user="user", password="passdword", host="10.72.6.143", port="5432")
		cur = conn.cursor()
		cur.execute(""" SELECT count(*) AS count FROM tablename where username = %s ;""",(username,))
		conn.commit()
		for row in cur.fetchall():
			count = row
			count = count[0]
			count = str(count)
			print count
		conn.close()
		return str(count)
	except Exception as error:
		return error

'''
################### GET request to get all user info  ##########################
'''
@app.route('/Get', methods=['GET'])
def Get():
	try:
		conn = psycopg2.connect(database="database", user="username", password="password", host="10.72.6.143", port="5432")
		cur = conn.cursor()
		cur.execute(""" SELECT * FROM userinfo ;""")
		conn.commit()
		columns = ('x', 'y', 'z','a')
		results = []
		for row in cur.fetchall():
			results.append(dict(zip(columns, row)))
		conn.close()
		return jsonify({'userinfo': results})
	except Exception as error:
		return error
@app.route('/GetByPost', methods=['POST'])
def GetByPost():
	if not request.json or not 'username' in request.json:
		abort
	username = request.json['username']
	try:
		conn = psycopg2.connect(database="database", user="username", password="password", host="10.72.6.143", port="5432")
		cur = conn.cursor()
		cur.execute(""" SELECT * FROM tablename WHERE username = %s;""",(username,))
		columns = ('x', 'y', 'z')
		conn.commit()
		results = []
		for row in cur.fetchall():
			results.append(dict(zip(columns, row)))
		conn.close()
		return jsonify({'userinfo': results})
	except Exception as error:
		return error
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
