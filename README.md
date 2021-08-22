## :small_blue_diamond: Objective 
Building a mobile and web compatible web application that enables patients and physicians get in reach easily.
## :small_blue_diamond: Features

* Account management for both physicians and patients 
  - Create account,login and update account details
  - Phyicians to be able to respond to appointment requests
  - Physicians can also be able to track records of appointments they avail for
  - Patients to be able to keep a record of appointments they make
                                                    
* Physicians may toggle between times when they are online - available and when they are offline - not available for appointments
* Patients to be able to see physicians around them and the approximate distance between them and their precise locations
* Patients to be able to send appointment requests 
* Physicians to manage appointment requests via their portals

## :small_blue_diamond: Accomplished
:heavy_check_mark: Authentication - Registration,Login,logout and account details update functionality<br/>
:heavy_check_mark: View available physicians<br/>
:heavy_check_mark: Physician online and offline status toggle<br/>
:heavy_check_mark: Distance approximation between the physician and the patient using **Geoclue** and **geopy** libraries<br/>
> Distance approximation is however not accurate at all :warning:

### :small_blue_diamond: Requirements ,Packages used and Installation
Download and install Python, for this tutorial I'll be using Python 3.8.5, make sure to check the box Add Python to PATH on the installation setup screen
 
### :small_blue_diamond: Installation
          
Navigate to your current project directory for this case it will be **Physician-Request-Web-App**. <br>
          
### 1 .Fork ,Clone the repo and Create an environment :pushpin:
          
Depending on your operating system,make a virtual environment to avoid messing with your machine's primary dependencies
          
**Windows**
          
```
git clone https://github.com/{your-GitHub-username}/Physician-Request-Web-App.git
cd Physician-Request-Web-App
py -3 -m venv venv
```
          
**macOS/Linux**
          
```
git clone https://github.com/{your-GitHub-username}/Physician-Request-Web-App.git
cd Physician-Request-Web-App
python3 -m venv venv
```

### 2 .Activate the environment :pushpin:
          
**Windows** 

```venv\Scripts\activate```
          
**macOS/Linux**

```. venv/bin/activate```
or
```source venv/bin/activate```

### 3 .Install the requirements :pushpin:

Applies for windows/macOS/Linux

```pip install -r requirements.txt```
### 4 .Migrate/Create a database

Applies for windows/macOS/Linux

```python manage.py```

### 5. Run the application :pushpin:

**For linux and macOS**
Make the run file executable by running the code

```chmod 777 run```

Then start the application by executing the run file

```./run```

**On windows**
```
set FLASK_APP=main
flask run
```
The run file incase missing,create a new file name it **run** then add the following :point_down: ;

```FLASK_APP=main.py FLASK_DEBUG=1 FLASK_ENV=development flask run``` </br></br>
![medoc](https://user-images.githubusercontent.com/57575260/127542252-424c7c69-326d-4863-82ab-1c2f86a981d4.png)


</br></br></br>
<div align="center"><h1>Happy Open Source and Coding :+1: </h1></div>
<p align="center"> <a href="https://twitter.com/dev_elie" target="blank"><img src="https://img.shields.io/twitter/follow/dev_elie?logo=twitter&style=for-the-badge" alt="dev_elie" /></a> </p>


