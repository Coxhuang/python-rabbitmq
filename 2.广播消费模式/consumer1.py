import pika
import time

auth = pika.PlainCredentials(
    username='guest',
    password='guest',
) # 用户名 / 密码
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        '127.0.0.1', # RabbitMQ 地址
        5672, # 端口号
        '/', # 虚拟主机
        auth, # 验证
    )
) # 链接RabbitMQ
channel = connection.channel() # 创建RabbitMQ通道

channel.queue_declare(
    queue='queue_name_test', # 消费对列名
    durable=True, # 持久化
)


def callback(ch, method, properties, body):
    print("消费者1:  %r" % body)
    time.sleep(5)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # send ack to rabbit

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue='queue_name_test', # 对列名
    auto_ack=True, # 自动回应
    on_message_callback=callback, # 回调消息
)

channel.start_consuming()

