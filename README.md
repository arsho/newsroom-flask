Newsroom
========

![Final List](Screenshot/Phase4/dashboard.png)

A web application for storing and managing news stories.

## Milestones

### - [x] Phase 1 (Completed)

   - Necessary package installation
   
   - Database creation
   
   - Sign up and login system for users

   - A page to list all stored news

   - A page to create new news

### - [x] Phase 2 (Completed)

   - Add JSON format for each news

   - Update story list page to include JSON link

### - [x] Phase 3 (Completed)
 
   - Add date field in news form

   - Modify database design
   
   - Add XML format for each news

   - Update story list page to include XML link

### - [x] Phase 4 (Completed)

   - Add edit and delete functinoalities for each news

   - Delete function should include confirmation alert
   
## Software Requirements

The following environment are used to develop the application:

- **OS** : Windows 8.1 (64 bit)
- **IDE** : PyCharm Professional (Version: 2017.2.3)
- **Server** : XAMPP (Version 3.2.2)
- **Python** : 3.6.2 (64 bit)
- **MySQL** : 10.1.21-MariaDB

### Necessary Package Installation

- Install virtual environment

		$ python -m venv newsroom_venv

- Activate virtual environment (Change it based on your OS)

		$ newsroom_venv\Scripts\activate.bat

- Install necessary packages included in requirements.txt

		$ pip install -r webapp\requirements.txt

In CMD, the above commands are executed like below:

![Package Installation](Screenshot/Phase1/install_package.png)		
		
### Database Configuration

- Open CMD/Terminal/X-term and login as mysql root user. 
Then create a database user `newsroom_db_admin` with password `newsroom_db_password`, 
main database, test database and grant all privileges to the user as shown below:

```
$ mysql -u root
mysql> CREATE USER 'newsroom_db_admin'@'localhost' IDENTIFIED BY 'newsroom_db_password';
mysql> CREATE DATABASE newsroom_db;
mysql> GRANT ALL PRIVILEGES ON newsroom_db . * TO 'newsroom_db_admin'@'localhost';
mysql> CREATE DATABASE newsroom_test_db;
mysql> GRANT ALL PRIVILEGES ON newsroom_test_db . * TO 'newsroom_db_admin'@'localhost';
```

This may look like this

![Main Database Configuration](Screenshot/Phase1/database_cmd.png)		
		
![Test Database Configuration](Screenshot/Phase1/database_test_cmd.png)				
		
- Activate virtual environment (if not activated)

		$ newsroom_venv\Scripts\activate.bat

- Change directory to webapp

		$ cd webapp

- Check MySQL configuration in `config.py` using own MySQL username, password and database name. 

- Check test MySQL configuration in `tests.py` using own MySQL username, password and database name. 

- To create the database run `db_create.py`. Run only after first configuration. 

		$ python db_create.py

- To track down the schema changes of database, I have used migration technique.
Execute `db_upgrade.py` to upgrade the database to the latest revision. 
This script should run after every modification in database schema.

		$ python db_migrate.py

The relationship between table looks like below in phpMyAdmin

![Updated Database](Screenshot/Phase4/database.png)		

		
### To Run the Application

- Activate virtual environment (if not activated)

		$ newsroom_venv\Scripts\activate.bat

- Run the `application.py`

		$ python application.py

		
### Unit testing

- Ensure that you have created test database as mentioned above

- Activate virtual environment (if not activated)

		$ newsroom_venv\Scripts\activate.bat

- Run the `tests.py`

		$ python tests.py

![Unittests](Screenshot/Phase4/unittests.png)		
		
### What is this repository for?

- Quick summary
- Version Controlling
- Screenshot enlisting of each phase (See attached Screenshot folder)
- [Issue Tracking](https://bitbucket.org/arsho/newsroom/issues)


### Phase 1 Output

- Registration page for new user

![Registration Demo](Screenshot/Phase1/registration.png)

- Login page for existing user

![Login Demo](Screenshot/Phase1/login.png)

- Home page for logged in user

![Dashboard Demo](Screenshot/Phase1/dashboard.png)

- Add news page for adding new news to database

![Add news Demo](Screenshot/Phase1/add_news.png)

- News details page for single news

![News details Demo](Screenshot/Phase1/news_details.png)

- XSS check in address bar using custom error page

![XSS Demo](Screenshot/Phase1/xss.png)

- Database table from phpMyAdmin

![Table Demo](Screenshot/Phase1/database_table.png)

### Phase 2 Output

- Sample news in HTML format

![HTML Format](Screenshot/Phase2/html_format.png)

- Sample news in JSON format

![JSON Format](Screenshot/Phase2/json_format.png)


### Phase 3 Output

- Listing the news with both HTML, JSON and XML format with pagination

![HTML, JSON, XML List Demo](Screenshot/Phase3/list.png)

- Added date in add news form. 
Updated the model and then migrated the database using `python db_migrate.py` inside the virtual environment.

![Added date in form](Screenshot/Phase3/add_news_date.png)

- Sample news in HTML format with date

![HTML Format with date](Screenshot/Phase3/html_format_date.png)

- Sample news in XML format

![XML Format](Screenshot/Phase3/xml_format.png)

- Dashboard can be accessible with or without login. But to add news login is mandatory.

![Open dashboard](Screenshot/Phase3/open_dashboard.png)

- Strong validation in applied all forms. Here is an example of registration form validation.

![Registration validation](Screenshot/Phase3/registration_validation.png)

### Phase 4 Output

- Listing the news with both HTML, JSON and XML format with pagination and edit and delete functionalities

![Final List](Screenshot/Phase4/dashboard.png)

- Edit option of a news.

![Edit option](Screenshot/Phase4/edit.png)

- Delete news after confirmation

![Delete option](Screenshot/Phase4/confirmation_delete.png)