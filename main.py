import sensor, image, time ,car#导入模块
from pyb import Pin, Timer
sensor.reset()
sensor.set_pixformat(sensor.RGB565)#设置颜色格式
sensor.set_framesize(sensor.QQQVGA)#设置分辨率
sensor.skip_frames(time = 200)
sensor.set_auto_gain(False)#关闭自动增益
sensor.set_auto_whitebal(False)#关闭白平衡
sensor.set_auto_exposure(False,21000)#关闭自动曝光设置为手动曝光
tim = Timer(4, freq=1000)#设置pwm引脚频率
Bline = (0, 22, -18, 15, -7, 35)#巡线LAB采样值
Runroi = ( 0, 0, 80, 20 )#巡线检测区域
yvanroi = ( 20, 0, 40, 60 )#判圆环区域
Errors = 0#偏差
LastErrors = 0#上次偏差
Kp =3#比例系数
Kd = 10#微分系数
Center = 40#摄像头巡线中值
PID = 0#pid输出量
DErrors = 0#两次偏差变化率
ValueL = 150#左电机速度
ValueR = 150#右电机速度
clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()#拍摄一幅图片进入缓存
    img = img.lens_corr(1.8)#镜头畸变矫正，使之更贴近现实
    for blob in img.find_blobs([Bline],roi=Runroi,merge=True):#色块检测函数，返回检测到的色块相关的值并存入blob中
    #详情链接：https://docs.singtown.com/micropython/zh/latest/openmvcam/library/omv.image.html?highlight=find_blobs#image.find_blobs
        img.draw_rectangle(blob.rect())#在缓存中的图片内画方框，便于上位机查看识别情况
        Errors = blob.cx() - Center#pid偏差计算
        DErrors = Errors - LastErrors#微分项需要的两次偏差的差
        PID = Errors*Kp + DErrors*Kd#pid计算
        LastErrors = Errors#将本次偏差保存，用于微分系数的计算
        #print(PID)
    for yvan in img.find_circles(threshold = 2300, x_margin = 10, y_margin = 10, r_margin = 10,#检测圆形并返回相关信息
                r_min = 2, r_max = 50, r_step = 2):#threshold为检测敏感阈值，阈值越大越不容易误判，但不敏感，越小检测越准确但容易误判
        img.draw_circle(yvan.x(), yvan.y(), yvan.r(), color = (255, 0, 0))#在缓存中的图片内画方框，便于上位机查看识别情况
        if(yvan.y()>35):#当圆y轴方向大于某值时，停车充电，当单片机调试时卡死，建议先屏蔽本函数
#            car.run(80,80)
#            time.sleep(500)
            car.run(0,0)#停车
            time.sleep(3000)#充电时间设置，注意易导致单片机卡死

#    car.run(ValueL+PID,ValueR-PID)
    car.run(ValueR-PID,ValueL+PID)#差速后发向电机pwm
  #  print(ValueL+PID)
#作者@Mao叔叔啊 青岛恒星科技学院 2020.9.7
#苏卡不列队 曹春秋 梁锦华 王福震
