from sqlalchemy import create_engine, MetaData

# Connection
meta = MetaData()
engine = create_engine('mysql+pymysql://[DB_USER_PASSWORD]:[DB_USERNAME]@[HOST_IP]:[HOST_PORT]/[DB_NAME]')
conn = engine.connect()

