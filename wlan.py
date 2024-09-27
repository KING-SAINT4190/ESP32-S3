import time
from machine import Pin ,SoftI2C,Timer,PWM
from utime import sleep# ---- 添加 --------
import network
from umqttsimple import MQTTClient
import esp_ai,time
import sensor,tftlcd
from HCSR04 import HCSR04     #子文件夹下的调用方式




left1_pin  = 47  
left2_pin   = 3
right1_pin  = 48
right2_pin  = 38
left3_pin = 39
left4_pin = 40
right3_pin = 41
right4_pin= 42
Distance = 0
status=0
status2=0

infared_1 = Pin(1,Pin.IN)
infared_2 = Pin(2,Pin.IN)
infared_3 = Pin(7,Pin.IN)

trig = Pin(15,Pin.OUT)
echo = Pin(45,Pin.IN)
HC=HCSR04(trig,echo)
cam = sensor.OV2640()
cam.reset()
cam.set_framesize(sensor.VGA) #240*240分辨率
cam.set_hmirror(1) #后置摄像头模式




def motor_setup():
    global motro_left1
    global motro_left2
    global motro_right1     
    global motro_right2
    global motro_left3
    global motro_left4
    global motro_right3
    global motro_right4
    
    
        
    motro_left1 = PWM(Pin(left1_pin), freq=20000, duty=0)  # 创建motor pwm对象，设置为输出模式 
    motro_left2 = PWM(Pin(left2_pin),freq=20000, duty=0)
    motro_right1 = PWM(Pin(right1_pin),freq=20000, duty=0)   
    motro_right2 = PWM(Pin(right2_pin),freq=20000, duty=0)
    motro_left3 = PWM(Pin(left3_pin), freq=20000, duty=0)
    motro_left4= PWM(Pin(left4_pin), freq=20000, duty=0)
    motro_right3= PWM(Pin(right3_pin), freq=20000, duty=0)
    motro_right4 = PWM(Pin(right4_pin), freq=20000, duty=0)
    
 #方向函数
def turn_left():
    motro_left1.duty(780) # 输出高电平
    motro_left2.duty(0)
    motro_right2.duty(810) # 输出高电平
    motro_right1.duty(0)
    motro_left3.duty(0) # 输出高电平
    motro_left4.duty(780)
    motro_right3.duty(810) # 输出高电平
    motro_right4.duty(0)
def turn_right():
    motro_left2.duty(780) # 输出高电平
    motro_left1.duty(0)
    motro_right1.duty(780) # 输出高电平
    motro_right2.duty(0)
    motro_left3.duty(780) # 输出高电平
    motro_left4.duty(0)
    motro_right3.duty(0) # 输出高电平
    motro_right4.duty(780)

def slow_forward():
    motro_left2.duty(780) # 输出高电平
    motro_left1.duty(0)
    motro_left3.duty(780)
    motro_left4.duty(0)
    motro_right2.duty(810) # 输出高电平
    motro_right1.duty(0)
    motro_right3.duty(810)
    motro_right4.duty(0)
def backward():
    motro_left1.duty(780) # 输出高电平
    motro_left2.duty(0)
    motro_left4.duty(780)
    motro_left3.duty(0)
    motro_right1.duty(780) # 输出高电平
    motro_right2.duty(0)
    motro_right4.duty(780)
    motro_right3.duty(0)
    
    
def stop():
    motro_left1.duty(0) # 输出高电平
    motro_left2.duty(0)
    motro_right1.duty(0) # 输出高电平
    motro_right2.duty(0)
    motro_left3.duty(0) # 输出高电平
    motro_left4.duty(0)
    motro_right3.duty(0) # 输出高电平
    motro_right4.duty(0)

def turn_left2():
    motro_left2.duty(780) # 输出高电平
    motro_left1.duty(0)
    motro_right1.duty(0) # 输出高电平
    motro_right2.duty(680)
    motro_left3.duty(780) # 输出高电平
    motro_left4.duty(0)
    motro_right3.duty(680) # 输出高电平
    motro_right4.duty(0)

def turn_right2():
    motro_left2.duty(780) # 输出高电平
    motro_left1.duty(0)
    motro_right1.duty(0) # 输出高电平
    motro_right2.duty(680)
    motro_left3.duty(780) # 输出高电平
    motro_left4.duty(0)
    motro_right3.duty(680) # 输出高电平
    motro_right4.duty(0)


def tracing():#红外循迹
    slow_forward()
    if infared_3.value()==1 and infared_1.value()==0:
        turn_left2()
        
    elif infared_3.value()==0 and infared_1.value()==1:
        turn_right2()
        
    else:
        slow_forward()
        

    
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('606', '606hxd11081821')
        i = 1
        while not wlan.isconnected():
            print("正在链接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())




def sub_cb(topic, msg): # 回调函数，收到服务器消息后会调用这个函数
    global status
    global status2

    print(topic, msg)
    # ---- 添加 --------
    if topic.decode("utf-8") == "move" and msg.decode("utf-8") == "on" and status==1 and status2==0:
        slow_forward()
    if topic.decode("utf-8") == "move" and msg.decode("utf-8") == "off"and status==1 and status2==0 :
        stop()
    if topic.decode("utf-8") == "right" and msg.decode("utf-8") == "on" and status==1 and status2==0:
        turn_right()
    if topic.decode("utf-8") == "right" and msg.decode("utf-8") == "off"and status==1 and status2==0 :
        stop()
    if topic.decode("utf-8") == "left" and msg.decode("utf-8") == "on" and status==1 and status2==0:
        turn_left()
    if topic.decode("utf-8") == "left" and msg.decode("utf-8") == "off" and status==1 and status2==0:
        stop()
    if topic.decode("utf-8") == "down" and msg.decode("utf-8") == "on" and status==1 and status2==0:
        backward()
    if topic.decode("utf-8") == "down" and msg.decode("utf-8") == "off"and status==1 and status2==0:
        stop()   
    if topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "on":
        led_pin.value(1)
    elif topic.decode("utf-8") == "ledctl" and msg.decode("utf-8") == "off":
        led_pin.value(0)
    if topic.decode("utf-8") == "moshi1" and msg.decode("utf-8") == "off":
        status2 = 0
    elif topic.decode("utf-8") == "moshi1" and msg.decode("utf-8") == "on":
        status2 = 1
        



    # ---- 添加 --------
def fun(tim):
    global Distance
    Distance = 10-HC.getDistance() #测量距离




# 1. 联网
motor_setup()

do_connect()
tim = Timer(1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) #周期1s

# 2. 创建mqt
c = MQTTClient("umqtt_client", "192.168.31.116")  # 建立一个MQTT客户端
c.set_callback(sub_cb)  # 设置回调函数

c.connect()  # 建立连接
c.subscribe(b"ledctl")
c.subscribe(b"move")# 监控ledctl这个通道，接收控制命令
c.subscribe(b"right")
c.subscribe(b"left")
c.subscribe(b"down")
c.subscribe(b"moshi1")

trig = Pin(15,Pin.OUT)
echo = Pin(45,Pin.IN)
HC=HCSR04(trig,echo)
# ---- 添加 --------
# 3. 创建LED对应Pin对象
led_pin = Pin(46, Pin.OUT)
# ---- 添加 --------
b = esp_ai.face_recognition()
b.start()

while True:
    c.check_msg()
    c.publish(b'vvvv',str(Distance))
    
     #录入人脸，返回 ID 编号。没有的话返回 None
       
    value = b.recognize()
    if value :
        print(value[0])   
    
        if value[0]==0:
            status=1
    if status2==1:
        tracing()
    if status2==0:
        stop()
    