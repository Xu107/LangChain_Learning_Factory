#Python redis 基本用法
# redis是一个键值对数据库，类似于持久化的python字典
import redis
from time import sleep

# 1.创建连接到 Redis 的客户端
client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# host: Redis 服务器的主机地址，默认是 localhost。
# port: Redis 服务的端口，默认是 6379。
# db: 使用的 Redis 数据库编号，Redis 默认有 16 个数据库（0-15），db=0 表示使用第 0 个数据库。

# 测试连接
try:
    client.ping()
    print("连接成功！")
except redis.ConnectionError:
    print("连接失败！")

# 2.设置一个键值对
client.set('name','Alice')
#获取键的值
name=client.get('name')
print(name,type(name))
#Alice <class 'str'>

# 设置键值对并为其设置过期时间（单位：秒）
client.setex('session',1,'session_data')# 1秒后过期

# 检查键是否存在（EXISTS）
exists=client.exists("session")
print(exists)# 如果存在，返回 1；如果不存在，返回 0
#输出1
sleep(2)
exists=client.exists("session")
print(exists)# 如果存在，返回 1；如果不存在，返回 0
#输出0

# 3.哈希操作
# Redis 中的哈希（Hash）类型可以存储多个键值对（类似于 Python 中的字典），可以用来存储更复杂的结构。
client.hset('user:1000','name','Bob')
client.hset('user:1000','age',30)
name=client.hget('user:1000','name')
print(name)
#Bob

#获取哈希中所有字段和值
user_info=client.hgetall('user:1000')
print(user_info)
#{'name': 'Bob', 'age': '30'}

# 4.列表操作
# Redis 中的 列表（List） 可以用作队列或栈。
# 向列表添加元素（LPUSH / RPUSH）:
# 从左边添加元素
client.delete('queue')#删除整个hash表
client.lpush('queue','task1','task2','task3')
client.rpush('queue','task4','task5')
#获取列表中元素
task=client.lrange('queue',0,-1)
print(task)
#['task3', 'task2', 'task1', 'task4', 'task5']
#从左边弹出元素
task=client.lpop('queue')
print(task,type(task))
#task3 <class 'str'>
task=client.rpop('queue')
print(task,type(task))
#task5 <class 'str'>
print(client.lrange('queue',0,-1))

# 5.集合操作
# Redis 中的 集合（Set） 是无序且不重复的元素集合。
# 添加元素（SADD）:
client.sadd('languages','C++','Python','Java')#第一个为name(id)，后面为value
# 查看集合数量
languages=client.smembers('languages')
print(languages,type(languages),[lang for lang in languages])
#{'Python', 'Java', 'C++'} <class 'set'> ['Python', 'Java', 'C++']
#判断元素是否在集合中（SISMEMBER）:
is_member=client.sismember('languages','Python')
print(is_member)

# 6.有序集合操作
# Redis 中的 有序集合（Sorted Set） 是集合的一种扩展，每个成员都有一个关联的分数。
client.zadd('leaderboard',{'Alice':10,'Bob':20,'Chester':15})
# 查看有序集合中的元素（按分数排序）
leaderboard =client.zrange('leaderboard',0,-1,withscores=True)
print(leaderboard,type(leaderboard))
# 获取分数最高的两个成员
top_2_leaderboard=client.zrange('leaderboard',0,1,withscores=True)
print(top_2_leaderboard)

# 7.事务操作
# Redis 支持事务，允许你将多个命令封装为一个原子操作。
pipe = client.pipeline()
pipe.set('a', 10)#set操作是覆盖写，如果原先已经存在则覆盖原值
pipe.set('b', 20)
pipe.incr('a')#自增1
pipe.execute()  # 执行事务
print(client.get('a'))#11


# Redis 客户端在使用完毕后，建议关闭连接：
client.close()