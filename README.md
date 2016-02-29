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

  Battery:  82%
  Charging: off
  Range:    146 Km

  Location: (37.8197, -122.4786)
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
