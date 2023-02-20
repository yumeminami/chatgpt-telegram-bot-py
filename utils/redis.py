import redis

redis_client = None

def InitRedis():
    global redis_client
    redis_client = redis.Redis(host='localhost', port=6379, db=0,password='frM991103')
    return redis_client


def SetRedis(key, value):
    redis_client.set(key, value)

def GetRedis(key):
    return redis_client.get(key)