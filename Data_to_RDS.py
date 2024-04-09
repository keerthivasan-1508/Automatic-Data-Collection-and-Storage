import json
import requests
import psycopg2

def lambda_handler(event, context):
    api_url = 'http://api.open-notify.org/iss-now.json' 
    response = requests.get(api_url)
    json_data=response.json()
    
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        port=5432,
        dbname='postgres',
        user='',
        password='guvi1234',
        host='database-2.czku0sa6evsh.us-east-1.rds.amazonaws.com'
    )
    cursor = conn.cursor()
    
    try:
        cursor.execute("""CREATE TABLE space_station( message text, latitude float, longitude float, timestamp bigint )""")
        print("table creation is successful..")
    except:
        print("table already exists..")
    conn.commit()

    # Insert data into PostgreSQL table
    try:
        cursor.execute("INSERT INTO space_station (message, latitude, longitude, timestamp) VALUES (%s, %s, %s, %s)",
                       (json_data['message'], json_data['iss_position']['latitude'],
                        json_data['iss_position']['longitude'], json_data['timestamp']))
        conn.commit()
        print("Data inserted successfully!")
    except psycopg2.Error as e:
        print("Error inserting data:", e)
    finally:
        cursor.close()
        conn.close()
