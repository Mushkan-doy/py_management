import sqlite3

def updateMultipleRecords():
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        if sqliteConnection:
            print("Connected to SQLite successfully")
        else:
            print("Not Connect")
        cursor = sqliteConnection.cursor()
        project_data = cursor.execute("select * from project_master")
        
        list_query = []
        
        for row in project_data:
            p_id = str(row[0])
            project_end_date = row[1].split()
            end_date = project_end_date[0]
            
            project_start_date = row[10].split()
            start_date = project_start_date[0]
            
            print("ID = ",p_id,type(p_id)," ","Start_Date = ",start_date," ","End_Date = ",end_date)

            sqlite_update_query = "UPDATE project_master SET project_start_date='%s',project_end_date='%s' WHERE id= '%s' ;" % (start_date,end_date,p_id)
            list_query.append(sqlite_update_query)
            
        print("UPDATE QUERY = ",list_query)
        
        for i, query in enumerate(list_query):
            cursor.execute(query)
        
        sqliteConnection.commit()
        print("Total", cursor.rowcount, "Records updated successfully")
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update multiple records of sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

updateMultipleRecords()
