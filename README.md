# Hotel_Reservation

CS4125 project: Systems Analysis and Design
Team 23241

### design patterns implemented:
- factory
- decorator
- state

Generate hotel:
```
python3 manage.py generate_hotel "hotel name" numOfRooms
```
Delete hotel and rooms:
```
python3 manage.py delete_hotel "hotel name"
```

Run on Windows
```
python3 -m venv ./venv
venv\Scripts\activate
pip install django-paypal
python3 manage.py runserver
```
