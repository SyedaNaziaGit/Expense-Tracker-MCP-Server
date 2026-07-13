import os
from fastmcp import FastMCP
import sqlite3

#database path name for sqlite3
DB_PATH = os.path.join(os.path.dirname(__file__),"expenses_db")

#to name the categories and sub categories for our expenses we have json file path
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__),"categories.json")

#initialize database -
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
            """
        )
        

#call initialize db
init_db()

#creating fastmcp server instance
mcp = FastMCP(name ="Expense Tracker")

#--------------------- Adding Tools to MCP Server Here ---------------
#1. tool to add expense
@mcp.tool
def add_expense(date,amount,category,subcategory="",note =""):
    ''' Add a new expense to DB'''
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status":"ok","id":cursor.lastrowid}

#2.tool to list all expenses
@mcp.tool
def list_expenses(startdate,enddate):
    """
    Listing all  expense entries between startdate to enddate
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (startdate, enddate)
        )
        cols = [d[0] for d in cursor.description]
        return  [dict(zip(cols, r)) for r in cursor.fetchall()]

#3. tool to summarize 
@mcp.tool
def summarize(startdate,enddate,category=None):
    '''Summarize expenses by category for that date range.'''
    with sqlite3.connect(DB_PATH) as conn:
        query = conn.execute(
           """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """ 
        )
        params = [startdate,enddate]
        
        #on basis of category
        if category:
            query += " AND category = ?"
            params.append(category)
        query += " GROUP BY category ORDER BY category ASC"

        cursor = conn.execute(query, params)
        cols = [d[0] for d in cursor.description]
        return [dict(zip(cols, r)) for r in cursor.fetchall()]
    
#adding resource to claude
@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run() 
    #running mcp server
