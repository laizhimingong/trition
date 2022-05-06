import redis
pool =redis.ConnectionPool(host='127.0.0.1',port=6379,password='',max_connections=1000)
conn= redis.Redis(connection_pool=pool)
keys=conn.keys()
print(keys)