# Home Wine eXchange

## Overview
This project has two purposes.
1. It's my submission for Project 4 of the CS50W Harvard - EdX course.
2. I have wished on several occasions that something like this exists.

The heart of the website is an interactive home wine recipe builder.
To start a new recipe the user selects the desired wine style and volume 
and then proceeds to add ingredients to acheive the desired style.
The recipe builder uses wine-style and ingredient data to give real-time feedback
as ingredients and quantities are changed allowing the user to experiment and
create a recipe with the desired qualities.

## Demo
I will add a link here to a screencast demo once it's up and running.

## Files
I will add a description of files here.

## Main Features
| Feature                                     | Technology                  | Status   |
| -----------------------------------------   | --------------------------- | -------- |
| Registration/Login/logout/Profile           | Django/SQL database         | Pre-release |
| Ingredient database                         | Django/SQL database         | Pre-release |
| Wine style database                         | Django/SQL database         | Pre-release |
| Admin site management                       | Python, Django              | Pre-release |
| Recipe builder                              | Javascript, Bootstrap, Chart.js | Pre-release |
| Recipe storage and list                     | Javascript, Python, Django  | Pre-release |
| Display weights and volumes in chosen units | Javascript                  | Todo        |
| Recipe brew logging                         | Javascript, Python, Django  | Todo        |
| Recipe review and rating                    | Javascript, Python, Django  | Todo        |
| Website activity view                       | Javascript, Python, Django  | Todo        |
| "My Wine" view                              | Javascript, Python, Django  | Todo        |

## ToDo
The is a list of small items to be done in addition to the "Todo" features above.
* protect private recipe access on backend
* read-only view for anonymous users
* format recipe builder for small mobile device
* protect registration from bots
* show liquids in liquid units