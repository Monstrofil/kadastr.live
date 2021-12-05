# Introduction

This project is not what you think it is.

[DZK](https://dzk.gov.ua/) developers might not even know about this project, it does not
use data from [data.land.gov.ua](https://data.land.gov.ua/). 
Don't use data as an official source of information.

The only initial goal was to collect parcel addresses for the
[OSM](https://www.openstreetmap.org/) project.

There are no plans to do something with data or setup regular updates, 
author could give you whatever raw data you want.

![Map, the best map ever](/static/main_page.png)

# Installation

    pip install -r requirements.txt
    
Fill cadastr/.env file with postgresql database credentials 
(ask author using email to provide you read-only access to database)

Example:

    KADASTR_DB_USER=login
    KADASTR_DB_PASSWORD=password

Run it as regular django website.

# Editing map style

Use [maputnik](https://maputnik.github.io/editor/) as WYSIWYG editor
for vector_style.json style located in `static` folder.

# Missing parts

Lots of logic that works with land.gov.ua is still hidden because author
is too lazy to remove all credentials and secrets from code. One day either it will be
published or I'll accidentally publish it with all passwords compromised.

# Contacts

You can contact author using Issues on GitHub or using telegram: Monstrofil.