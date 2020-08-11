# Home Wine eXchange

## Overview
This project has two purposes.
1. It's my submission for the final project of the CS50W Harvard - EdX course.
2. I have wished on several occasions that something like this exists and may
subsequently launch it as a website.

The heart of the website is an interactive home wine recipe app that simplifies
the task of creating a home wine recipe to reproduce the key component levels of a
desired wine style.

## What is different to other CS50W projects?
* Wine-style and ingredient database
* Winemaking calculations
* Highly interactive recipe builder
* Chart display
* Drag and drop
* Anonymous and logged in users
* Display quantities in units set in user profile

## How does complexity compare to other CS50W projects?
This project is significantly more complex.

Most of the complexity is in the recipe app. To brew a balanced wine, the ingredients
need the suitable quantities of 4 components: sugar, acid, tannin and non-fermentable soluable solids.
To formulate a recipe, the user first chooses the desired wine style and volume to produce.
The recipe app calculates and displays a chart showing the targets of the 4 components
and the levels achieved by the chosen ingredients. As soon as the user changes ingredients or
quantities the app immediately recalculates and updates the display so that the user can
interact with it - adding, removing and adjusting - 
immediately seeing the effect on the 4 components compared
to the target levels. Additionally the user can drag and drop ingredients to change the 
order they are displayed in the recipe. This is all implemented in Javascript as a single
web page on the client making the app highly responsive since there are no 
communication or server latencies. The layout uses bootstrap rows and columns so that 
the app can be used even on small mobile devices.

Other features adding to the complexity
* anonymous users can use the site including the recipe app, but cannot save recipes
* recipe list + column headings clickable to sort by heading
* a user can set the units used for weight and volume
* a data migration imports wine style and ingredient data simplifying deployment 
* admin site can manage users, wine styles, ingredients and recipes
* data models are ready for additional features - see [Future Additions](#future-additions)

## Demo
I will add a link here to a screencast demo once it's up and running.

## Files
In this list to avoid clutter I have omitted the files that are similar in many Django projects. 
It focuses instead on the files that contain code or data specific to this project.

| File                       | Dir               | Content/Purpose             |
| -------------------------- | ----------------- | --------------------------- |
| db.sqlite3                 | .                             | The SQLite database
| import.py                  | .                             | Data importer - for future use
| ingredients.dat            | imports                       | Ingredient data from http://www.homewineprogram.com/
| methods.txt                | imports                       | Ingredient preparation methods
| wines.txt                  | imports                       | Wine style data
| admin.py                   | recipe                        | Admin site config code
| measures.py                | recipe                        | Solid and liquid measurement unit objects
| models.py                  | recipe                        | Models for database tables
| views.py                   | recipe                        | HTML creation and data access
| 0004_auto_20200616_2008.py | recipe/migrations             | Import ingredient data
| 0006_auto_20200617_1402.py | recipe/migrations             | Import wine-style data
| account.css                | recipe/static                 | Styling for account management pages
| base.css                   | recipe/static                 | Styling of webpage header
| newrecipe.js, .css         | recipe/static                 | New recipe form code and styling
| profile.js                 | recipe/static                 | Profile page code
| recipe.js, .css            | recipe/static                 | Recipe app code and styling
| recipes.js, .css           | recipe/static                 | Recipe list code and styling
| icon.xcf, .ico             | recipe/static                 | HomeWineX icon GIMP source and ICO file
| logo.xcf, .png             | recipe/static                 | HomeWineX logo GIMP source and PNG file
| base.html                  | recipe/templates/recipe       | Content of webpage header
| base_login.html            | recipe/templates/recipe       | Base for pages associated with login
| newrecipe.html             | recipe/templates/recipe       | Form to start a new recipe
| profile.html               | recipe/templates/recipe       | User profile page
| recipe.html                | recipe/templates/recipe       | Template for recipe app
| recipes.html               | recipe/templates/recipe       | Template for list of recipes
| login.html                 | recipe/templates/registration | Login page
| registration.html          | recipe/templates/registration | Registration page

## Features
### Implemented features
| Feature                                     | Technology                  |
| -----------------------------------------   | --------------------------- |
| Registration/Login/logout/Profile           | Django/SQL database         |
| Ingredient database                         | Django/SQL database         |
| Wine style database                         | Django/SQL database         |
| Admin site management                       | Python, Django              |
| Recipe builder, layout                      | Javascript, Bootstrap       |
| Recipe builder, add ingredient              | Javascript                  |
| Recipe builder, change quantity             | Javascript                  |
| Recipe builder, remove ingredient           | Javascript                  |
| Recipe builder, drag and drop ingredients   | Javascript, Sortable.js     |
| Recipe builder, chart totals vs. targets    | Javascript, Chart.js        |
| Recipe builder, save                        | Javascript, Python, Django  |
| Recipe list                                 | Javascript, Python, Django  |
| "My Wine" view                              | Javascript, Python, Django  |
| Display weights and volumes in chosen units | Javascript                  |
| Read-only view for anonymous users          | Javascript, Python, Django  |
| Home / introduction                         | HTML                        |
| Website activity view                       | Javascript, Python, Django  |
| Recipe brew logging                         | Javascript, Python, Django  |

### Future additions
| Feature                                     | Technology                  |
| -----------------------------------------   | --------------------------- |
| Recipe private/public control               | Javascript, Python, Django  |
| Recipe review and rating                    | Javascript, Python, Django  |
| Change password                             | Django/SQL database         |
| About + acknowledgements                    | HTML                        |
| Help                                        | HTML                        |
| Protect registration from bots              | ReCaptcha                   |
| Recipe: save as new                         | Javascript                  |

### Todo
* units: selection per ingredient
* units: default amount in database, choose appropriate units
* recipe: edit - only author or admin
* recipe: drag, don't allow drag from ingredient name - too easy to hit accidentally
* cookie warning
* recipe: store versions to avoid change to existing brews
* recipe: see ingredient props while viewing list
* recipe: on mobile dnd works only once
* recipe: add cancel button
* brew: edit / delete existing comment
