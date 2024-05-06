import paho.mqtt.client as mqtt
import binascii
import os
import datetime

# MQTT 伺服器設定
mqtt_server = "mqtt.meshtastic.org"  # 更換成您的 MQTT 伺服器地址
mqtt_port = 1883  # 根據您的伺服器設定可能需要更改
mqtt_user = "meshdev"  # 如果您的伺服器需要認證
mqtt_password = "large4cats"  # 如果您的伺服器需要認證
# 連接成功回調函數
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("msh/TW/2/e/#")


def on_message(client, userdata, msg):
    try:
        # 分割主题并获取设备ID，假定设备ID位于第五个部分
        topic_parts = msg.topic.split('/')
        if len(topic_parts) >= 5:
            device_id = topic_parts[5]  # 设备ID在第五个部分
            directory = './log'
            filename = os.path.join(directory, f'{device_id}.txt')

            # 确保日志目录存在
            if not os.path.exists(directory):
                os.makedirs(directory)

            # 打开文件并写入日志
            with open(filename, 'a') as file:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                payload_hex = binascii.hexlify(msg.payload).decode('ascii')
                payload_length = len(msg.payload)
                log_entry = f"{current_time} Topic: {msg.topic}\nPayload (hex): {payload_hex}\nPayload length in bytes: {payload_length}\n\n"
                print(f"Log entry written to {filename}")
                print(log_entry)
                file.write(log_entry)

        # 继续打印消息到控制台
        print(f"Topic: {msg.topic}")
        print(f"Payload (hex): {binascii.hexlify(msg.payload).decode('ascii')}")
        print(f"Payload length in bytes: {len(msg.payload)}")

    except Exception as e:
        print("Error while processing message:", str(e))
        print(f"Topic: {msg.topic}")
        print(f"Raw Payload (hex): {binascii.hexlify(msg.payload).decode('ascii')}")
        print(f"Payload length in bytes: {len(msg.payload)}")

# 建立 MQTT 客戶端實例
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(mqtt_user, mqtt_password)
client.connect(mqtt_server, mqtt_port, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Disconnecting from broker...")
    client.disconnect()  # Properly disconnect from the broker