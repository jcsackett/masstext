MassText 0.2
============

**Author: j.c.sackett (j.c.sackett@gmail.com) (@jaycee)**

## About

MassText is a simple django application that interfaces with Twilio to provide a mass texting utility.

It was thrown together in a night to provide its capabilities for a small group at PyCon 2010.

Development is planned to continue; it's pretty bare bones now.

## Setup

MassText is a django app, and can be installed simply by dropping it into your django project and adding it to INSTALLED_APPS. It exposes one view, **masstext**, which handles the interface between twilio and the application.

You also need to setup your twilio account sms url to point at _<yourdomain>/masstext_. But then, you had already figured that out, hadn't you?

## Usage

Once set up, you can use it simply by creating a user and a phonenumber model in the admin for each person you want on the masstext. And text message sent by any use to the twilio number will then be sent to every other user.
