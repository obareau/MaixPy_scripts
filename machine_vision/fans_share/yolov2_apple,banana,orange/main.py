import sensor
import image
import lcd
import KPU as kpu

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_hmirror(0)
sensor.run(1)
task = kpu.load("/sd/yolov2.kmodel")
with open("anchors.txt","r") as f:
    anchor_txt=f.read()
    L = [float(i) for i in anchor_txt.split(",")]
    anchor=tuple(L)
a = kpu.init_yolo2(task, 0.6, 0.3, 5, anchor)
with open("classes.txt","r") as f:
    labels_txt=f.read()
    labels = labels_txt.split(",")
while True:
    img = sensor.snapshot()
    if code := kpu.run_yolo2(task, img):
        for i in code:
            a=img.draw_rectangle(i.rect(),(0,255,0),2)
            a = lcd.display(img)
            for i in code:
                lcd.draw_string(
                    i.x() + 45,
                    i.y() - 5,
                    f"{labels[i.classid()]} " + '%.2f' % i.value(),
                    lcd.WHITE,
                    lcd.GREEN,
                )

    else:
        a = lcd.display(img)
a = kpu.deinit(task)