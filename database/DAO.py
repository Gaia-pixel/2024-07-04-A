from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT year(s.`datetime`) as y
                        FROM sighting s 
                        ORDER BY y DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row['y'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape as s
                        FROM sighting s 
                        WHERE year(s.`datetime`) = %s
                                and s.shape <> "" 
                        ORDER BY s.shape ASC
                                """
            cursor.execute(query, (anno, ))

            for row in cursor:
                result.append(row['s'])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(anno, forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.*
                    FROM sighting s 
                    WHERE s.shape = %s
                            and year(s.`datetime`) = %s
                                    """
            cursor.execute(query, (forma, anno))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllArchi(anno, forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t1.id as s1, t2.id as s2
                        FROM (SELECT s.id, s.state, s.`datetime`
                                FROM sighting s 
                                WHERE s.shape = %s
                                        and year(s.`datetime`) = %s) t1, 
                             (SELECT s.id, s.state, s.`datetime`
                                FROM sighting s 
                                WHERE s.shape = %s
                                        and year(s.`datetime`) = %s) t2
                        WHERE t1.state = t2.state
                                and t1.`datetime` < t2.`datetime`
                                        """
            cursor.execute(query, (forma, anno, forma, anno))

            for row in cursor:
                result.append((row['s1'], row['s2']))
            cursor.close()
            cnx.close()
        return result