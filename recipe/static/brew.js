const ingredient_template = Handlebars.compile(document.querySelector('#ingredient').innerHTML);
const style_template = Handlebars.compile(document.querySelector('#style').innerHTML);
const logentry_template = Handlebars.compile(document.querySelector('#logentry').innerHTML);

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
  
  // Make requested tab active or first tabif none requested
  var tab = document.querySelector('#initial-tab').dataset.name;
  if (!tab) {
    tab = document.querySelector('#tabs .nav-link').dataset.name;
  }

  showTab(tab);
  setUrl(tab);

  // Set the tab onclick listeners
  document.querySelectorAll('#tabs .nav-link').forEach( item => {
    item.onclick = function(ev) {
      ev.preventDefault();
      pushUrl(this.dataset.name);
      showTab(this.dataset.name);
      setUrl(this.dataset.name);

      window.onpopstate = (ev) => {
        console.log(ev);
        showTab(ev.state.tab, 0)
      };    
    };
  });
  
  // Get recipe and ingredient list
  var recipe_id = document.querySelector('#recipe').dataset.recipe_id;
  const request = new XMLHttpRequest();
  var url = '/api/recipe?' + new URLSearchParams({id: recipe_id}).toString();
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
  // findIngredient to use a sorted list and binary search.
  var ingr_el = document.querySelector("#ingredients");
  ingr_el.innerHTML = "";
  recipe.ingredients.forEach( use => {
    var ingr = utils.calcIngredientAttrs(findIngredient(use.ingredient_id), use, recipe.volume_l, profile);
    ingr.qty = ingr.qty * brew.size_l / recipe.volume_l;
    ingr_el.innerHTML += ingredient_template({ingredient: ingr});
  });

  // Set totals and targets
  var totals = utils.calcTotalAttrs(".ingredient-data");
  totals.name = 'TOTALS';
  ingr_el.innerHTML += ingredient_template({ingredient: totals});
  var targets = Object.assign({}, style);
  targets.name = 'TARGETS';
  ingr_el.innerHTML += ingredient_template({ingredient: targets});

  // Show method

  // Get recipe and ingredient list
  getLog();
}

function getLog() {
  const request = new XMLHttpRequest();
  var url = '/api/brewlog?' + new URLSearchParams({brew_id: brew.id}).toString();
  request.open('GET', url);
  request.onload = showLog;
  var csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send();
}

function showLog(ev) {
  // display the log entries
  var request = ev.target;
  const data = JSON.parse(request.responseText);

  var log_el = document.querySelector("#log-entries");
  log_el.innerHTML = "";
  data.log.forEach( logEntry => {
    var d = new Date(logEntry.datetime);
    logEntry.datetime = d.toLocaleDateString();
    logEntry.comments.forEach( comment => {
      var d = new Date(comment.datetime);
      comment.datetime = d.toLocaleDateString();
    });
    log_el.innerHTML += logentry_template({logEntry: logEntry});
  });

  // Set the function of the add comment buttons and forms
  document.querySelectorAll('.comment-button').forEach( el => el.onclick = showCommentForm );
  document.querySelectorAll('.comment-form textarea').forEach( el => el.oninput = enableSubmit );
  document.querySelectorAll('.comment-form button').forEach( el => el.onclick = saveComment );

  // Set the log entry textarea heights
  document.querySelectorAll('.log-text').forEach( el => {
    el.style.height = "";
    el.style.height = el.scrollHeight + 3 + "px";
  });
  
  // Can the user modify this brew log?
  if (document.querySelector('.log-entry-button')) {

    // Set the log entry edit and delete functions
    document.querySelectorAll('.log-edit').forEach( el => el.onclick = editLogEntry );
    document.querySelectorAll('.log-delete').forEach( el => el.onclick = deleteLogEntry );

    // Set the function and display of the add log entry button and form
    document.querySelector('.log-entry-button').onclick = showNewLogEntryForm;
    document.querySelector('.log-entry-button').hidden = false;
    document.querySelector('.new-log-form').hidden = true;
    document.querySelector('.new-log-form textarea').value = "";

    // Set the functions to enable and process the save and cancel buttons 
    document.querySelectorAll('.log-form textarea').forEach( el => el.oninput = enableSubmit );
    document.querySelectorAll('.log-form .save-button').forEach( el => el.onclick = saveLog );
    document.querySelectorAll('.log-form .cancel-button').forEach( el => el.onclick = cancelLog );
    document.querySelectorAll('.log-form textarea').forEach( el => el.oninput = enableSubmit );
    document.querySelector('.new-log-form textarea').oninput = enableSubmit;
    document.querySelector('.new-log-form button').onclick = saveLog;
  }  
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

  // Set the log entry textarea heights
  document.querySelectorAll('.log-text').forEach( el => {
    el.style.height = "";
    el.style.height = el.scrollHeight + 3 + "px";
  });

}

function setUrl( name ) {
  var page_url = 'brew?' + new URLSearchParams({id: brew.id, tab: name}).toString();
  document.title = "HomeWineX - Brew: " + name;
  history.replaceState({'url': 'brew', 'id': brew.id, 'tab': name}, document.title, page_url);
}

// function pushUrl( name ) {
//   var page_url = 'brew?' + new URLSearchParams({id: brew.id, tab: name}).toString();
//   document.title = "HomeWineX - Brew: " + name;
//   history.pushState({'url': 'brew', 'id': brew.id, 'tab': name}, document.title, page_url);
// }

function pushUrl( name ) {
  history.pushState({'url': 'brew', 'id': brew.id, 'tab': name}, document.title, document.location);
}

function showNewLogEntryForm(ev) {
  var form = document.querySelector('.new-log-form')
  form.hidden = false;
  ev.target.hidden = true;
  window.scrollTo(0,document.body.scrollHeight);
  form.querySelector('textarea').focus();

  return false;
}

function editLogEntry(ev) {
  var form = ev.target.closest('.log-entry').querySelector('form');
  form.querySelector('textarea').readOnly = false;
  form.querySelector('.save-button').hidden = false;
  form.querySelector('.cancel-button').hidden = false;
  form.querySelector('textarea').focus();
  return false;
}

function deleteLogEntry(ev) {
  if (confirm("Delete Log entry?")) {
    const request = new XMLHttpRequest();
    request.open('POST', `/api/brewlogdelete`);
    const data = new FormData(ev.target.closest('.log-entry').querySelector('form'));

    request.onload = showLog;
    
    var csrftoken = Cookies.get('csrftoken');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.send(data);
  }

  return false;
}

function showCommentForm(ev) {
  var form = ev.target.parentElement.querySelector('form')
  form.hidden = false;
  ev.target.hidden = true;
  form.querySelector('textarea').focus();
  return false;
}

function enableSubmit(ev) {
  // Enable if there is log content to submit
  ev.target.parentElement.querySelector('button').disabled = ev.target.value.length == 0;
}

function saveLog(ev) {
  const request = new XMLHttpRequest();
  request.open('POST', `/api/brewlog`);
  const data = new FormData(ev.target.parentElement);

  request.onload = showLog;
  
  var csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send(data);
  return false;
}

function cancelLog() {
  getLog();
}

function saveComment(ev) {
  const request = new XMLHttpRequest();
  request.open('POST', `/api/brewcomment`);
  const data = new FormData(ev.target.parentElement);

  request.onload = showLog;
  
  var csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send(data);
  return false;
}

function findIngredient(id) {
  // Linear search because the set of ingredients is very small
  var result = null;
  ingredients.forEach( ingredient => {
    if ( id == ingredient.id ) {
      result = ingredient;
    }
  });
  return result;
}
