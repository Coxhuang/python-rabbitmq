[TOC]


# RabbitMQ

> 关于python的队列，内置的有两种，一种是线程queue，另一种是进程queue，但是这两种queue都是只能在同一个进程下的线程间或者父进程与子进程之间进行队列通讯，并不能进行程序与程序之间的信息交换，这时候我们就需要一个中间件，来实现程序之间的通讯。

> Mac安装RabbitMQ 🍺🍺👉  https://blog.csdn.net/Coxhuang/article/details/89765797

> Python队列Queue使用 🍺🍺👉  https://blog.csdn.net/Coxhuang/article/details/89764188

## #0 Blog

https://blog.csdn.net/Coxhuang/article/details/89786760

## #1 环境

```
Python3.7.3
pika==1.0.1 # pika的版本不同,提供方法的参数名有变化
```

## #2 开始

### #2.1 轮询模式

> 此模式下，发送队列的一方把消息存入mq的指定队列后，若有消费者端联入相应队列，即会获取到消息，并且队列中的消息会被消费掉。
若有多个消费端同时连接着队列，则会已轮询的方式将队列中的消息消费掉。

> 生产者

```
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
    body='Hello RabbitMQ!', # 发送消息的内容
    properties=pika.BasicProperties( delivery_mode=2,) # 消息持久化
)
print("发送...")
connection.close()

```

> 消费者

```
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
    print("消费者:  %r" % body)

channel.basic_consume(
    queue='queue_name_test', # 对列名
    auto_ack=True, # 自动回应
    on_message_callback=callback, # 回调消息
)
time.sleep(5) # 模拟消费时间
print("消费者")
channel.start_consuming()

```

**运行生产者**

![20190502222720-image.png](https://raw.githubusercontent.com/Coxhuang/yosoro/master/20190502222720-image.png)

---

![20190502225315-image.png](https://raw.githubusercontent.com/Coxhuang/yosoro/master/20190502225315-image.png)



#### # 模拟轮询模式


> 生产者生产5个任务到队列中

```
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
```

> 消费者(新建3个消费者py文件,分别运行消费者程序)


```
# 消费者1
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
    print("消费者:  %r" % body)
    time.sleep(5) # 模拟消费时间

channel.basic_consume(
    queue='queue_name_test', # 对列名
    auto_ack=True, # 自动回应
    on_message_callback=callback, # 回调消息
)

print("我是消费者1")
channel.start_consuming()

```

```
# 消费者2 
... # 同消费者1 
... # 同消费者1 
def callback(ch, method, properties, body):
    print("消费者:  %r" % body)
    time.sleep(5) # 模拟消费时间
```
```
# 消费者3 
... # 同消费者1 
... # 同消费者1 
def callback(ch, method, properties, body):
    print("消费者:  %r" % body)
    time.sleep(5) # 模拟消费时间
```

![20190503110939-image.png](https://raw.githubusercontent.com/Coxhuang/yosoro/master/20190503110939-image.png)

---

![20190503111007-image.png](https://raw.githubusercontent.com/Coxhuang/yosoro/master/20190503111007-image.png)

---

![20190503111014-image.png](https://raw.githubusercontent.com/Coxhuang/yosoro/master/20190503111014-image.png)

---

![20190503111019-image.png](https://raw.githubusercontent.com/Coxhuang/yosoro/master/20190503111019-image.png)

---

> 轮询模式:公平分配任务给消费者,不考虑消费者的消费能力


### #2.2 广播模式

> 在多consumer的情况下，默认rabbitmq是轮询发送消息的，但有的consumer消费速度快，有的消费速度慢，为了资源使用更平衡，引入ack确认机制。consumer消费完消息后会给rabbit发送ack，一旦未ack的消息数量超过指定允许的数量，则不再往该consumer发送，改为发送给其他consumer。

#### # 模拟广播模式

- 生产者代码不变

- 消费者

```
# 插入如下代码
...
def callback(ch, method, properties, body):
    print("消费者2:  %r" % body)
    time.sleep(10) # 模拟消费者消费能力
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
...
```

> 消费者1消费能力: 1秒一个

> 消费者2消费能力: 10秒一个

> 消费者3消费能力: 15秒一个

---

![20190503114152-image.png](https://raw.githubusercontent.com/Coxhuang/yosoro/master/20190503114152-image.png)

---

![20190503124102-image.png](https://raw.githubusercontent.com/Coxhuang/yosoro/master/20190503124102-image.png)

---

![20190503124133-image.png](https://raw.githubusercontent.com/Coxhuang/yosoro/master/20190503124133-image.png)







---


## # 报错

### #1 

```
# error
pika.exceptions.AMQPConnectionError
```
```
# RabbitMQ地址写错
```

### #2 


```
# error
TypeError: basic_consume() got multiple values for argument 
```


```
pika版本不同
当前pika==1.0.1
basic_consume的参数名发生改变,应该为如下格式:
channel.basic_consume(
    queue='queue_name_test', # 对列名
    auto_ack=False, # 自动回应
    on_message_callback=callback, # 回调消息
)
```








