from rq import Worker, Queue
from redis import Redis

redis_conn = Redis()
queue = Queue(connection=redis_conn)
worker = Worker([queue], connection=redis_conn)

if __name__ == '__main__':
    worker.work()