import sqlite3

def updateEmpStatusRecords():
    try:
        sqliteConnection = sqlite3.connect('db.sqlite3')
        if sqliteConnection:
            print("Connected to SQLite successfully")
        else:
            print("Not Connect")
        cursor = sqliteConnection.cursor()
        employee_data = cursor.execute("select * from employee_master")
        print("employee Data = ",employee_data)
        list_query = []
        
        for row in employee_data:
            p_id = str(row[0])
            relieving_date = row[4]
            status = 'Relieve'
            if relieving_date:
                # print("Employee_id = ",p_id,"Relieving Date = ",relieving_date,'Status = ',status)
                sqlite_update_query = "UPDATE employee_master SET status='%s' WHERE relieving_date IS NOT NULL;" % (status)
                print("Query = ",sqlite_update_query)
                list_query.append(sqlite_update_query)
                
        print("UPDATE QUERY = ",list_query)
        
        for i,query in enumerate(list_query):
            print("Four Query = ",query)
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

updateEmpStatusRecords()
        