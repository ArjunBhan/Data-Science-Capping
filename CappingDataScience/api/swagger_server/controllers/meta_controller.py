import connexion
import six

from swagger_server.models.null_result import NullResult  # noqa: E501
from swagger_server import util

from swagger_server import cur, conn # Database 


def meta_nulls_table_name_get(tableName):  # noqa: E501
    """Get all a count of nulls in a table

    Returns the amount of nulls and row count for a table # noqa: E501

    :param tableName: table name to get information for
    :type tableName: str

    :rtype: List[NullResult]
    """

    # First ensure they are asking for a valid table.
    # This is essential to avoid a SQL injection. We can't use query params
    # (and if we can please let me know how to use query params for things
    # like table names). We need to make sure they can't have anything
    # but our table name as input.
    try:
        cur.execute("SELECT COUNT(*) FROM information_schema.tables " +
                    "WHERE table_schema = 'public' AND table_type = 'BASE TABLE' " +
                    "AND table_name = %s", [tableName])
        if cur.fetchone()[0] == 0:
            return "Not valid table", 400
    except:
        conn.rollback()
        return "Database error", 500        
    
    # Get column names of table
    try:
        cols = []
        cur.execute("SELECT column_name FROM information_schema.columns " +
                    "WHERE table_name = %s", [tableName])
        for i in cur.fetchall():
            cols.append(i[0])
    except:
        conn.rollback()
        return "Database error", 500        

    
    # Get count of rows in table (Building the tableName string should give
    # you a SQL INJECTION red flag)! It is okay in this case, read above comment.
    try:
        cur.execute("SELECT COUNT(*) FROM " + tableName)
        num_rows = cur.fetchone()[0]

        # Get null count per each column.
        num_rows_null_cols = []
        for col in cols:
            cur.execute("SELECT COUNT(*) FROM " + tableName + " WHERE " +
                        col + " IS NULL")
            num_rows_null_cols.append(cur.fetchone()[0])

            # Get null count for any column.
            cur.execute("SELECT COUNT(*) FROM " + tableName +
                        " WHERE NOT (" + tableName + " IS NOT NULL)")
            any_null_count = cur.fetchone()[0]            
    except:
        conn.rollback()
        return "Database error", 500        
    
    return NullResult(num_rows, cols, num_rows_null_cols, any_null_count)


def meta_tables_get():  # noqa: E501
    """Get all of the table names

     # noqa: E501


    :rtype: List[str]
    """
    tableNames = []
    try:
        # https://stackoverflow.com/questions/14730228/postgresql-query-to-list-all-table-names
        cur.execute("SELECT table_name FROM information_schema.tables " +
                    "WHERE table_schema = 'public' AND table_type = 'BASE TABLE'");
        for i in cur.fetchall():
            tableNames.append(i[0])
    except:
        conn.rollback()
        return "Database error", 500        
    
    return tableNames
