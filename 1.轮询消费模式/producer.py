import pika




credentials = pika.PlainCredentials(
    username = 'guest',
    password = 'guest',
)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host = '127.0.0.1', # MQ地址(本机)
        port = 5672, # 端口号,注意是5672,不是15672
        virtual_host = '/', # 虚拟主机
        credentials = credentials, # 用户名/密码
    )
)

channel = connection.channel()

channel.queue_declare(
    queue='queue_name_test', # 队列名
    durable=True, # 使队列持久化
)

channel.basic_publish(
    exchange='',
    routing_key='queue_name_test', # 告诉rabbitmq将消息发送到 queue_name_test 队列中
    body="Hello RabbitMQ, I'm first task ", # 发送消息的内容
    properties=pika.BasicProperties( delivery_mode=2,) # 消息持久化
)

channel.basic_publish(
    exchange='',
    routing_key='queue_name_test', # 告诉rabbitmq将消息发送到 queue_name_test 队列中
    body="Hello RabbitMQ, I'm second task ", # 发送消息的内容
    properties=pika.BasicProperties( delivery_mode=2,) # 消息持久化
)

channel.basic_publish(
    exchange='',
    routing_key='queue_name_test', # 告诉rabbitmq将消息发送到 queue_name_test 队列中
    body="Hello RabbitMQ, I'm third task ", # 发送消息的内容
    properties=pika.BasicProperties( delivery_mode=2,) # 消息持久化
)

channel.basic_publish(
    exchange='',
    routing_key='queue_name_test', # 告诉rabbitmq将消息发送到 queue_name_test 队列中
    body="Hello RabbitMQ, I'm fourth task ", # 发送消息的内容
    properties=pika.BasicProperties( delivery_mode=2,) # 消息持久化
)

channel.basic_publish(
    exchange='',
    routing_key='queue_name_test', # 告诉rabbitmq将消息发送到 queue_name_test 队列中
    body="Hello RabbitMQ, I'm fifth task ", # 发送消息的内容
    properties=pika.BasicProperties( delivery_mode=2,) # 消息持久化
)

print("派送任务到队列中...")
connection.close()