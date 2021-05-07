# DMV Appointment Booker

The purpose of this program is to automate the process of booking a DMV appointment.
Drivers License, State ID, and Learners Permits appointments can take several months to book due to the increasingly high demand.
Openings can occur randomly but are few and far between, and will often be sniped within a few minutes of freeing up.

This script will automatically check relevant locations for openings and automatically book them.
It will run until a valid appointment is found, or until manually terminated (otherwise it will run forever).
A "valid" appointment indicates that it occurs before your current appointment
(if you don't have one, it will find the earliest possible)
and that it is before 2:45 PM (as this time or later isn't valid for a lot of types of appointments).

## Setup instructions:

Start by cloning this repository. All the relevant files should be in one directory.

Next, install the appropriate Selenium webdriver depending on your browser of choice.
Make sure the webdriver is in your PATH.
Links to various browers, along with further installation instructions can be found
[here](https://selenium-python.readthedocs.io/installation.html#drivers).

Then make sure you have the appropriate packages installed, by running these commands in your terminal:
```
$ pip install selenium
$ pip install keyboard
```
Though, the program should import these automatically if they aren't already installed.

Finally, fill in the user data in `data.txt` with your first name, last name, and phone number (the first three lines).
These are at minimum required to appropriately book an appointment, or the code will not run properly.
The rest of the lines in this file contain information current appointment data;
if you don't currently have an appointment just leave these blank.
If you wish to fill in your appointment data, make sure to preserve the format:
spell out the month in full (e.g. September), and write time in standard form with timezone (e.g. 12:30 PM)

## Usage:

Execute the program by running `appointment_booker.py` in an IDE of choice,
or by using this command line in your terminal:
```
$ python appointment_booker.py
```

If an appointment is found and booked, confirmation data will be saved to the text file.

**Optional parameters:** you can parse through the code and change a few constants if desired.\
`BROWSER` : this determines which browser to use. Make sure this matches the webdriver you installed.
Default is Firefox.\
`FILE_PATH` : the file path that contains user data and current appointment data.
Just make sure if you rename or move this file, use the correct path. Default is `data.txt`.\
`FIRST_ONLY` : if set to True (default), only the first available appointment for a certain location will be checked.
This is recommended when appointments are sparse.
Otherwise all possible valid appointments will be checked.
This is recommended when there may be a number of available appointments, though this is rare.\
`LATEST_TIME` : if set to True (default False), the latest time for any specific valid date will be booked.
This is recommended if you want to avoid early morning appointments.
Otherwise, the first (earliest) available appointment will be booked.\
`SAVE_AS_PDF` : if set to True (default), a PDF confirmation of the appointment will be saved upon booking.
This will be saved to your default save location (e.g. your Documents folder).
May not work depending on your OS or browser; designed for use with Windows and Firefox.