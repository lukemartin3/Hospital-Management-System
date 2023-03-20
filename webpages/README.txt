Web developement has been shifted over using XAMPP Apache (3.3.0), which allows for local web application development.
XAMPP allows us to connect our web application to pre-existing MySQL DB, while also giving us an Admin UI for local MySQL db.

Instructions:

After downloading XAMPP (https://www.apachefriends.org/) 8.2.0

In order to connect to a pre-existing local MySQL server:
Modify Apache Module by clicking on Config for the Apache Module. 
- Click phpMyAdmin (config.inc.php)
- Change user and pw to your DB user (for default case, user should be 'root' and pw should be [given root pw])
- For full admin control, also change controluser to your given db user.
- Restart Apache 

Changing localhost web application root directory
Modyify Apache Module by clicking on config for Apache Module
- Click Apache (Httpd.conf)
- Find Find tag : DocumentRoot "C:/xampp/htdocs"
- Edit Tag to : DocumentRoot "C:\[your Directory]\swe_project\webpages"
- Edit < Directory "C:/[Your Directory]" >

You should now be able to see web pages when you enter http://localhost/login.php or any http://localhost/[webpage.html/php]
