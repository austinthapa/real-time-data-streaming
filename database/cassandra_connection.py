import logging
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthenticator
from cassandra.policies import DCAwareRoundRobinPolicy

def create_cassandra_connection():
    """
    Create a Cassandra connection.
    
    Returns:
        cassandra.cluser.Session or None
    """
    try:
        cluster = Cluster(['localhost'],
                          port=9042,
                          load_balancing_policy=DCAwareRoundRobinPolicy())
        session = cluster.connect()
        logging.info(f"Cassandra connection set up successfully")
        return session
    except Exception as e:
        logging.error(f"Error occured during cassandra connection: {e}")
        return None

def create_keyspace(session):
    """
    Create the 'user_logs' keyspace if it does not exist.
    
    Args:
        session (cassandra.cluster.Session)
    Returns
        str: The name of the keyspace if created or existed, else None
    """
    try:
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS user_logs WITH REPLICATION = {
                'class': 'SimpleStrategy',
                'replication_factor': '1'
            }             
        """)
        logging.info("Successfully created keyspace user_logs")
        return "user_logs"
    except Exception as e:
        logging.error(f"Error creating keyspace: {e}")
        return None
    
def create_tables(session, keyspace):
    """
    Create the user-related logs in the specified keyspace
    
    Args:
        session (cassandra.cluster.Session)
        
    Returns:
        bool: True if all tables are created successfully, False otherwise
    """
    session.set_keyspace(keyspace)
    try:
        session.execute("""
            CREATE TABLE IF NOT EXISTS user_session_logs (
                user_id UUID, 
               session_id UUID, 
               login_time TIMESTAMP, 
               logout_time TIMESTAMP,
               duration TEXT,
               device TEXT, 
               os TEXT,
               browser TEXT,
               location TEXT,
               ip_address TEXT,
               PRIMARY KEY(user_id, session_id))             
        """)
        logging.info(f"Successfully created user_session_logs table")
        
        session.execute("""
            CREATE TABLE IF NOT EXISTS user_auth_logs (
                user_id UUID,
                session_id UUID,
                timestamp TIMESTAMP,
                ip_address TEXT,
                device TEXT,
                success TEXT,
                failure_reason TEXT,
                PRIMARY KEY(user_id, session_id)
            )
        """)
        logging.info('Successfully created user_auth_logs table')
        
        session.execute("""
            CREATE TABLE IF NOT EXISTS user_activity_logs (
            user_id UUID,
            session_id UUID,
            event_type TEXT,
            timestamp TIMESTAMP,
            url TEXT,
            device TEXT,
            location TEXT,
            event_category TEXT,
            page_id UUID,
            content_id TEXT,
            action_taken TEXT,
            PRIMARY KEY(user_id, session_id))
        """)
        logging.info("Successfully created user_activity_logs table")
        return True
    except Exception as e:
        logging.info(f'Unexpected error occured during table creation: {e}')
        return None
    