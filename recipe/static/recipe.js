const ingredient_template = Handlebars.compile(document.querySelector('#ingredient').innerHTML);
const new_ingredient_template = Handlebars.compile(document.querySelector('#new_ingredient').innerHTML);

var recipe;
var ingredients;

document.addEventListener('DOMContentLoaded', () => {
  buildRecipeApp();
})

function enableSave() {
  disabled = true;

  // Enable if there is a modified text input
  document.querySelectorAll('.form-control').forEach( input => {
    if ( input.dataset.value != input.value ) {
      disabled = false;
    }
  });

  // Enable if there is a modified radio button input
  document.querySelectorAll('.custom-control-input').forEach( radio => {
    if ( radio.checked ) {
      if ( radio.closest('.form-group').dataset.value != radio.value ) {
        disabled = false;
      }
    }
  });

  document.querySelector('.submit').disabled = disabled;

  return true;
}

function buildRecipeApp() {
  id = document.querySelector('#recipe_id').value;

  // Get recipe and ingredient list
  const request = new XMLHttpRequest();
  url = '/recipedetail?' + new URLSearchParams({id: id}).toString();
  request.open('GET', url);
  request.onload = showRecipe;
  csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send();
}

function showRecipe(ev) {
  request = ev.target;
  const data = JSON.parse(request.responseText);

  // Keep a copy of the recipe and available ingredients to allow us to build
  // then submit.
  recipe = data.recipe;
  ingredients = data.ingredients;

  // If starting a new recipe, get the basic data from the HTML elements already
  // created.
  if ( recipe.id < 0 ) {
    recipe.name = document.querySelector('#recipe-name').innerHTML;
    recipe.volume = document.querySelector('#recipe-volume').innerHTML;
    recipe.descr = document.querySelector('#recipe-descr').innerHTML;
    recipe.ingredients = [];
  }

  showIngredients();
}

function showIngredients() {
  // Create an ingredient line for each ingredient in the recipe
  // This is O(N*N). If this becomes a performance issue change it
  // to a sorted list of ingredients and implement a binary search
  // to achieve O(N*logN).
  ingr_el = document.querySelector("#ingredients");
  ingr_el.innerHTML = "";
  i = 0;
  recipe.ingredients.forEach( use => {
    ingredients.forEach( ingredient => {
      if ( use.ingredient_id == ingredient.id ) {
        ingr = calcIngredientAttrs(ingredient, use.qty_kg, recipe.volume_l);
        ingr_el.innerHTML += ingredient_template({ingredient: ingr, index: i});;
      }
    });
    i++;
  });

  // Set actions for qty changes
  el = ingredient_template({ingredient: ingr});
  i = 0;
  ingr_el.querySelectorAll('.qty').forEach( el => {
    el.oninput = (ev) => { 
      qty_kg = ev.target.value;
      use = recipe.ingredients[ev.target.dataset.index];
      use.qty_kg = qty_kg;
      ingredients.forEach( ingredient => {
        if ( use.ingredient_id == ingredient.id ) {
          ingr = calcIngredientAttrs(ingredient, use.qty_kg, recipe.volume_l);

          // Set the values in the existing elements rather than rebuilding HTML,
          // so that the UI runs smoothly making it a more interactive experience.
          ingr_row = ev.target.closest('.ingredient-table');
          ingr_row.querySelector('.qty').innerHTML = ingr.qty_kg;
          ingr_row.querySelector('.sugar').innerHTML = ingr.sugar;
          ingr_row.querySelector('.acid').innerHTML = ingr.acid;
          ingr_row.querySelector('.tannin').innerHTML = ingr.tannin;
          ingr_row.querySelector('.solids').innerHTML = ingr.solids;
          ingr_row.querySelector('.redness').innerHTML = ingr.redness;
        }
      });
  
    };
    i++;
  });

  // Create new ingredient input selector and button
  document.querySelector('#ingredient-select').innerHTML = new_ingredient_template({ingredients: ingredients});
  document.querySelector('#new_ingr_select').oninput = (ev) => {
    document.querySelector('#new_ingr_button').disabled = (ev.target.value == -1);
    return true;
  };
  document.querySelector('#new_ingr_button').onclick = () => {
    // Adds new ingredient to the array and updates the page.
    recipe.ingredients.push({
      ingredient_id: document.querySelector('#new_ingr_select').value,
      qty_kg: 1.0
     });
     showIngredients();
     return false;
  };
}

function calcIngredientAttrs(ingredient, qty_kg, volume_l) {
  return {
    name: ingredient.name,
    qty: parseFloat(qty_kg).toFixed(2),
    sugar: (qty_kg * ingredient.sugar / volume_l / 2.64).toFixed(0),
    acid: (qty_kg * ingredient.acid / volume_l).toFixed(2),
    tannin: (qty_kg * ingredient.tannin / volume_l).toFixed(2),
    solids: (qty_kg * ingredient.solu_solid / volume_l).toFixed(2),
    redness: (qty_kg * ingredient.redness / volume_l).toFixed(1),
  };
}
