# SWE_Project

## Reset Password Function
If you plan on testing the reset-password functions mail capabilities, you must do the following:
    1. Login to Gmail using:
        > User: swe.team09@gmail.com
        > Password: MyTeam09!
        > NOTE: The account has 2-Factor Authentication setup, so contact Abrahm to get your code. 
    2. Once in Gmail, navigate to https://myaccount.google.com/apppasswords and setup an App Password. 
    3. Once you have setup an App Password, change the following line in app.py:
        > app.config['MAIL_PASSWORD'] = YOUR-APP-PASSWORD
    4. Now, you should be able to run the reset-password function with all of its capabilities. 