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
| Feature                                     | Technology                  | Status      |
| -----------------------------------------   | --------------------------- | ----------- |
| Registration/Login/logout/Profile           | Django/SQL database         | Pre-release |
| Ingredient database                         | Django/SQL database         | Pre-release |
| Wine style database                         | Django/SQL database         | Pre-release |
| Admin site management                       | Python, Django              | Pre-release |
| Recipe builder, layout                      | Javascript, Bootstrap       | Pre-release |
| Recipe builder, add ingredient              | Javascript                  | Pre-release |
| Recipe builder, change quantity             | Javascript                  | Pre-release |
| Recipe builder, remove ingredient           | Javascript                  | Pre-release |
| Recipe builder, drag and drop ingredients   | Javascript, Sortable.js     | Pre-release |
| Recipe builder, chart totals vs. targets    | Javascript, Chart.js        | Pre-release |
| Recipe builder, save                        | Javascript, Python, Django  | Pre-release |
| Recipe list                                 | Javascript, Python, Django  | Pre-release |
| "My Wine" view                              | Javascript, Python, Django  | Pre-release |
| Display weights and volumes in chosen units | Javascript                  | Pre-release |
| Read-only view for anonymous users          | Javascript, Python, Django  | Pre-release |
| Recipe private/public control               | Javascript, Python, Django  | Todo        |
| Recipe brew logging                         | Javascript, Python, Django  | Todo        |
| Recipe review and rating                    | Javascript, Python, Django  | Todo        |
| Website activity view                       | Javascript, Python, Django  | Todo        |
| Change password                             | Django/SQL database         | Todo        |
| About + acknowledgements                    | HTML                        | Todo        |
| Home / introduction                         | HTML                        | Todo        |
| Help                                        | HTML                        | Todo        |

## ToDo
The is a list of small items to be done in addition to the "Todo" features above.
* protect registration from bots - do this for deployment
* recipe: save as new