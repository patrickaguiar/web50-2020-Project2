# web50/2020 Project2 #
## Design an eBay-like e-commerce auction site that will allow users to post auction listings, 
place bids on listings, comment on those listings, and add listings to a “watchlist.” ##

An exemple of the web50 course project2. Here we've designed a mobile friendly auctions web application that allows users to **sell products online, 
buy products online, add products to a watchlist, make comments about other people products, and a lot more.**

In order to make this website done, we've just used Django and Bootstrap4.
To run this application in your machine, you need to

- Download this repository
- Open your commandline and update the database 

```
python manage.py makemigrations auction
python manage.py migrate
```

- Start the application

```
python manage.py runserver
```

- Open the link command line gives to you in your web browser. 

### Architecture ###
Besides Django usual models, we used tree constructors in order to make our application readable:
DataGetter - A class responsable for taking data from models 
DataSetter - A class responsable for setting data to models
Views - Functions responsable for manipulate and validate data and display the templates 

### If you want to colaborate, he're a list of things that I believe could help: ###
- [] Security Improvements: Set Security Standarts for Passwords, set a minimun time interval between each login attempt
- [] Translate 
- [] Separate DataGetter, DataSetter and views in diferent files and make sure that they just doing their responsabilities
- [] Test the application
- [] Implement javascript in order to make the application more human friendly
- [] Design improvements
- [] Connect the application to a real payment API
- [] Improve this list 
