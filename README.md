# ESP32-S3

  以32位单片机为主控制器，利用智能小车为底座，采用喷雾与紫外灯两种消杀方式，分手动遥控与自动巡线两种工作模式，手动部分利用APP与wify遥控，自动部分利用红外循迹规划路线。
  加入人脸识别功能作为设备的开关。摄像头可对人脸进行特征提取。上电后设备进入待机状态，摄像头开始工作，当检测到预先录入的人脸后，设备才能进入工作模式。
  
  手动遥控以及自动巡线两种工作模式的设计。使用者在设备进入工作状态后可首先利用APP遥控设备移动，当调整到铺设有黑线的正确的位置后，在APP中将工作模式更改为自动循迹模式，设备即可沿黑线进行移动消杀。同样，使用者也可将自动模式改为手动模式。

