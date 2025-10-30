import os
import mysql.connector
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

def get_db_connection(database_name=None):
   
    try:
        connection_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
        }
        
   
        if database_name:
            connection_config['database'] = database_name
            
        connection = mysql.connector.connect(**connection_config)
        return connection
            
        
        
    except mysql.connector.Error as e:
        print(f"Database Connection Failed: {e}")
        return None

def create_database():
    """
    Create the database if it doesn't exist
    """
    connection = get_db_connection()  
        
    if connection is None:
        print("Failed to connect to MySQL server")
        return False
    
    cursor = None
    try:
        cursor = connection.cursor()
          
        create_database_query = "CREATE DATABASE IF NOT EXISTS image_analysis"
        cursor.execute(create_database_query)
        connection.commit()
        
        print("----------------------------------------------------------------")
        print("Successfully Created Database: image_analysis or already exists")
        print("----------------------------------------------------------------")
        
        return True
    
    except mysql.connector.Error as e:
        print(f"Error Creating Database: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    
def create_table():
    """
    Create the table in the image_analysis database
    """
    connection = get_db_connection('image_analysis')  
    
    if connection is None:
        print("Failed to connect to image_analysis database")
        return False
    
    cursor = None
    try:
        cursor = connection.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            average_brightness FLOAT NOT NULL,
            brightest_value FLOAT NOT NULL,
            darkest_value FLOAT NOT NULL,
            processed_image_path VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        
        print("--------------------------------------------------------------")
        print("Successfully created table: analysis_results or already exists")  
        print("--------------------------------------------------------------")
        return True

    except mysql.connector.Error as e:
        print(f"Database Initialization failed: {e}")
        return False
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        
def insert_analysis_result(
    filename: str,
    average_brightness: float,
    brightest_value: float,
    darkest_value: float,
    processed_img_path: str
) -> bool:
    """
    Insert analysis result into the database
    """
    connection = get_db_connection('image_analysis')  # Connect to specific database
    if connection is None:
        return False

    cursor = None
    try:
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO analysis_results 
        (filename, average_brightness, brightest_value, darkest_value, processed_image_path)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            filename,
            average_brightness,
            brightest_value,
            darkest_value,
            processed_img_path
        ))
        
        connection.commit()

        print("----------------------------------------------------")
        
        print(f"Successfully inserted data into analysis_results: "
              f"({filename}, {average_brightness}, {brightest_value}, {darkest_value}, {processed_img_path})")
        
        print("-----------------------------------------------------")

        return True

    except mysql.connector.Error as e:
        print(f"Insert Failed: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_analysis_result(limit: int = 50): 
    """
    Get analysis results from database
    """
    connection = get_db_connection('image_analysis')  # Connect to specific database
    
    if connection is None:
        return []
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        
        select_query = """
        SELECT id, filename, average_brightness, brightest_value, 
               darkest_value, processed_image_path, created_at
        FROM analysis_results 
        ORDER BY created_at DESC 
        LIMIT %s
        """
        
        cursor.execute(select_query, (limit,))
        results = cursor.fetchall()
        
        formatted_result = []  
        
        for row in results:
            formatted_result.append({
                "id": row["id"],
                "filename": row["filename"],
                "average_brightness": float(row["average_brightness"]),
                "brightest_value": float(row["brightest_value"]),
                "darkest_value": float(row["darkest_value"]),
                "processed_image_path": row["processed_image_path"],
                "created_at": row["created_at"].isoformat() if row["created_at"] else None
            })
          
        print("----------------------------------")  
        print("Successfully fetched from Database")  
        print("----------------------------------")
        
        return formatted_result  
    
    except mysql.connector.Error as e:
        print(f"Query Failed: {e}")
        return []
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


create_database()
create_table()
    
