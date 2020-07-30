const ingredient_template = Handlebars.compile(document.querySelector('#ingredient').innerHTML);
const style_template = Handlebars.compile(document.querySelector('#style').innerHTML);

import * as utils from './utils.js';

var brew;
var recipe;
var ingredients;
var profile;
var style;

document.addEventListener('DOMContentLoaded', () => {
  buildBrewApp();
})

function buildBrewApp() {
  // Get brew info
  brew = {};
  brew.id = document.querySelector('#brew').dataset.brew_id;
  brew.size_l = document.querySelector('#volume').innerHTML;
  
  // Make first tab active
  showTab(document.querySelector('#tabs .nav-link').dataset.name);

  // Set the tab onclick listeners
  document.querySelectorAll('#tabs .nav-link').forEach( item => {
    item.onclick = function() {
      showTab( this.dataset.name );
    };
  });
  
  // Get recipe and ingredient list
  var recipe_id = document.querySelector('#recipe').dataset.recipe_id;
  const request = new XMLHttpRequest();
  var url = '/recipedetail?' + new URLSearchParams({id: recipe_id}).toString();
  request.open('GET', url);
  request.onload = showRecipe;
  var csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send();
}

function showRecipe(ev) {
  var request = ev.target;
  const data = JSON.parse(request.responseText);

  // Keep a copy of the data for later.
  recipe = data.recipe;
  ingredients = data.ingredients;
  utils.setUtilProfile(data);
  profile = data.profile;

  if ( profile ) {
    // Set brew volume to the chosen liquid units. Value from backend is always
    // index zero in the converter.
    var volume_el = document.querySelector('#volume');
    volume_el.innerHTML = utils.liquid.convert(volume_el.innerHTML, 0, profile.liquid_large_units).toFixed(1);
    var unit_el = document.querySelector('#volume-unit');
    unit_el.innerHTML = utils.liquid.toString(profile.liquid_large_units);

    // Qty unit string to chosen solid and liquid units.
    unit_el = document.querySelector('#qty-unit');
    var liquidStr = utils.liquid.toString(profile.liquid_large_units);
    var solidStr = utils.solid.toString(profile.solid_large_units);
    unit_el.innerHTML = `(${solidStr} ${liquidStr})`;
  }

  style = utils.getStyleData(recipe.style);
  document.querySelector('#recipe-style').innerHTML = style_template({style: style});

  // Create an ingredient line for each ingredient in the recipe
  // This is O(N*N). If this becomes a performance issue change it
  // to a sorted list of ingredients and implement a binary search
  // to achieve O(N*logN).
  var ingr_el = document.querySelector("#ingredients");
  ingr_el.innerHTML = "";
  recipe.ingredients.forEach( use => {
    ingredients.forEach( ingredient => {
      if ( use.ingredient_id == ingredient.id ) {
        var ingr = utils.calcIngredientAttrs(ingredient, use, recipe.volume_l, profile);
        ingr.qty = ingr.qty * brew.size_l / recipe.volume_l;
        ingr_el.innerHTML += ingredient_template({ingredient: ingr});
      }
    });
  });

  // Set totals and targets
  var totals = utils.calcTotalAttrs(".ingredient-data");
  totals.name = 'TOTALS';
  ingr_el.innerHTML += ingredient_template({ingredient: totals});
  var targets = Object.assign({}, style);
  targets.name = 'TARGETS';
  ingr_el.innerHTML += ingredient_template({ingredient: targets});

  // Show method

  getLog();
}

function getLog() {
  
  document.querySelectorAll('.log-form textarea').forEach( el => el.oninput = enableSubmit );
  document.querySelectorAll('.log-form button').forEach( el => el.onclick = saveLog );
}

function showLog(ev) {
  // display the log entries
  var request = ev.target;
  const data = JSON.parse(request.responseText);

  console.log(data);

  // Set the functions to enable and process the submit buttons 
  document.querySelectorAll('.log-form textarea').forEach( el => el.oninput = enableSubmit );
  document.querySelectorAll('.log-form button').forEach( el => el.onclick = saveLog );
}

function showTab(name) {
  // Make all tabs inactive except the selected tab
  document.querySelectorAll('#tabs .nav-link').forEach( item => {
    if ( item.dataset.name == name ) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });

  // Display the selected tab content and undisplay all the rest
  document.querySelectorAll('.tab-detail').forEach( item => {
    if ( item.dataset.name == name ) {
      item.style.display = "inline";
    } else {
      item.style.display = "none";
    }
  });

}

function enableSubmit(ev) {
  // Enable if there is log content to submit
  ev.target.parentElement.querySelector('button').disabled = ev.target.value.length == 0;
}

function saveLog(ev) {
  const request = new XMLHttpRequest();
  request.open('POST', `/brewlog`);
  const data = new FormData(ev.target.parentElement);

  request.onload = showLog;
  
  var csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send(data);
  return false;
}
