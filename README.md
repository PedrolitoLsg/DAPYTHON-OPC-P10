# OPCP10


![image](https://user-images.githubusercontent.com/84906663/150554334-871922c6-85e9-4006-936a-39a9e3572986.png)

SoftDesk is the 10th Project of the [OPC training](https://openclassrooms.com/fr/paths/518-developpeur-dapplication-python). It consitutes of a [DRF API](https://www.django-rest-framework.org/) allowing users to create projects and discuss about it by creating issues and comments.


## Setup:

clone the project
install required libraries:
```
pipenv install -r requirements.txt
```

navigate to projet10:
```
cd projet10
```

launch server:
```
python manage.py runserver
```




## How to Use:

Check the [API documentation](https://documenter.getpostman.com/view/18880001/UVRBnm9E) to understand endpoints and their use.
Communication is done through the use of json and the [simplejwt token (5.00)](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/#) is used for authentication.
