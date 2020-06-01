==================================================
更新了针对中国的Carnet （endpoint）
有些API的soap POST request版本更新了
认证需要两条POST
额外追加了一点汉语现实

        [opc@shifengcentos carnet]$ carnet status
        ---- Vehicle information -------------------
          Model: VW PASSAT Wag. CLBMT 162 D6F (2018)
          Color: Pure White
          LicensePlate: 辽Bxxxxx
          Platform: MIBOCU_MQB

        ---- Account Information -------------------
        AccountID: xxxxxx
        Subscription: 2017-11-01T15:55:21.599+08:00
        VIN: xxxxxxxx
        TCUID: xxxxxxxxxxxxxx

        ---- Main Status ---------------------------
          Mileage: 24637 Km

          Fuel/燃油:   27/66 L
          Range/续航:    280 Km

          Outside Temperature/车外温度: 18.85 °C

          Location/坐标: (38.877749, 121.525999)
          Altitude/海拔: 20m
          Course/航向：42°
                    http://www.latlong.net/c/?lat=38.877749&long=121.525999


----未完成功能-----
1.Car Detail 的信息其实有很多，还没解析好，不知道什么格式比较友好
2.目前还没有更新原来作者的 发送指令到车的那些POST， 肯定是不能用的

----进阶工作------
1。 谁能提供一下 车POST 信息的Endpoint，或者谁能破解一些VW的carnet 的车端的功能。
 用VCDS 可以修改 车的Endponit ，但是他的格式是这样的：
    vw.cn.p.tos.htichina.net
 这个显然会被车再次解析的，不知道 Car 真正的post 的url 是什么，如果能够截获car post 的内容的话，
 指向一个自己的云服务器，那样能够的到车的信息会更多。
 目前的信息功能有限。





carnet: A implementation of the VW car-net® api
==================================================

The latest VW vehicles include car-net® connectivity
to access your car information from the web and
a mobile app.

This is a library and cli tool to access the
same api from the comfort of your cli, and easily
integrate it with other systems. Do you want to
track and map your vehicle locations? Do you want
to receive alarms when the battery is full or too
low? There are endless possibilities! Let me know
how you use this library!

See the cli in action:

```
$ carnet setup
Account ID: 11111111
PIN: 1111
Verifying credentials...
Success!
---- Vehicle information -------------------
  Model: VW eGolf (2016)
  Color: Pacific Blue Metallic
  VIN:   XXXXXXXXXXX
  TCUID: XXXXXXXXXXX

---- Owner information ---------------------
  Phone: 5550000000
  Email: foo@bar.com

$ carnet status
---- Vehicle information -------------------
  Model: VW eGolf (2016)
  Color: Pacific Blue Metallic
  VIN:   XXXXXXXXXXX
  TCUID: XXXXXXXXXXX

---- Owner information ---------------------
  Phone: 5550000000
  Email: foo@bar.com

---- Main Status ---------------------------
  Mileage: 265 Km

  Battery:  80%
  Range:    144 Km
  Charging: connected, charging  (1h 35m untill full)

  Location: (37.8197, -122.4786)
            http://www.latlong.net/c/?lat=37.8197&long=-122.4786
```

And how to use the API:

```python
from carnet import Api

api = Api(account_id, pin)
status = api.status()
lat = status['VehicleLocation']['Latitude']
lon = status['VehicleLocation']['Longitude']
```

Feature Support
---------------

Right now the implementation is rather limited:
Only read-access to vehicle information and status
is implemented.

The pairing exchange is also implemented, but
I didn't have time to start implementing any
actions. Any help and pull requests are greatly
appreciated.

Security Considerations
-----------------------

This project started motivated by my curiosity
about how secure secure was the api.

I must confess that the findings are not very
encouraging:
- Authentication is done with a sequencial account
  id and a 4-digit pin, which is totally insufficient
  for any decent security.
- Authentication seems to be done via IP. After
  authenticating, you can call to status with
  totally different transaction_ids and it works.
- There is a pairing mechanism that seems to
  be used for the more sensible operations (like
  unlock the car, turn lights, claxon...) BUT
  there is access to a lot of information
  without the pairing, including phone and
  email of the owner, location of the car and
  much more, which opens the door to social
  attacks.

I have already contacted the company that runs
this service and will let them know about my
findings and suggestions.

Install
-------

It requires python3. To install run:

```
</path/to/python3> setup.py install
```


