const ingredient_template = Handlebars.compile(document.querySelector('#ingredient').innerHTML);
const new_ingredient_template = Handlebars.compile(document.querySelector('#new_ingredient').innerHTML);
const ingredient_totals_template = Handlebars.compile(document.querySelector('#ingredient_totals').innerHTML);
const style_template = Handlebars.compile(document.querySelector('#style').innerHTML);

var recipe;
var ingredients;
var styles;
var totals;

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

  // Keep a copy of the data to allow us to build the recipe locally.
  recipe = data.recipe;
  ingredients = data.ingredients;
  styles = data.styles;

  // If starting a new recipe, get the basic data from the HTML elements already
  // created.
  if ( recipe.id < 0 ) {
    recipe.name = document.querySelector('#recipe-name').innerHTML;
    recipe.volume = document.querySelector('#recipe-volume').innerHTML;
    recipe.descr = document.querySelector('#recipe-descr').innerHTML;
    recipe.ingredients = [];
  }

  showStyle();
  showIngredients();
  showGraph();
}

function showStyle() {
  style = getStyleData();
  document.querySelector('#recipe-style').innerHTML = style_template({style: style});
  document.querySelector('#style-targets').innerHTML = ingredient_totals_template({legend: 'TARGETS', totals: style});
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

  // Set totals
  totals = calcTotalAttrs();
  document.querySelector('#ingredient-totals').innerHTML = ingredient_totals_template({legend: 'TOTALS', totals: totals});

  // Set actions for qty changes
  ingr_el.querySelectorAll('.qty').forEach( el => { el.oninput = updateQty });

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

function showGraph() {
  Chart.defaults.global.defaultFontSize = 16;
  ctx = document.querySelector('#wine-chart').getContext('2d');
  var myBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Sugar', 'Acid', 'Tannin', 'Solids'],
      datasets: [{
        label: 'recipe',
        backgroundColor: 'rgb(255, 225, 128)',
        borderColor: 'rgb(255, 225, 128)',
        data: [
          100*totals.sugar/style.sugar,
          100*totals.acid/style.acid,
          100*totals.tannin/style.tannin,
          100*totals.solids/style.solu_solids
        ]
      },
      {
        label: 'target',
        backgroundColor: 'rgb(255, 128, 255)',
        borderColor: 'rgb(255, 128, 255)',
        data: [
          100,
          100,
          100,
          100
        ]
      }]
    },
    options: {
      title: {
        display: true,
        text: '% Comparison to Target Values'
      },
      animation: {
        duration: 0
      }
    }
  });  
}

function updateQty(ev) { 
  // Set the values in the existing elements rather than rebuilding HTML,
  // so that the UI runs smoothly making it a more interactive experience.

  qty_kg = ev.target.value;
  use = recipe.ingredients[ev.target.dataset.index];
  use.qty_kg = qty_kg;

  // Update values for this ingredient
  ingredients.forEach( ingredient => {
    if ( use.ingredient_id == ingredient.id ) {
      ingr = calcIngredientAttrs(ingredient, use.qty_kg, recipe.volume_l);

      ingr_row = ev.target.closest('.ingredient-data');
      ingr_row.querySelector('.qty').innerHTML = ingr.qty_kg;
      ingr_row.querySelector('.sugar').innerHTML = ingr.sugar;
      ingr_row.querySelector('.acid').innerHTML = ingr.acid;
      ingr_row.querySelector('.tannin').innerHTML = ingr.tannin;
      ingr_row.querySelector('.solids').innerHTML = ingr.solids;
      ingr_row.querySelector('.redness').innerHTML = ingr.redness;
    }
  });

  // Update totals
  totals = calcTotalAttrs();
  totals_row = document.querySelector('#ingredient-totals');
  totals_row.querySelector('.sugar').innerHTML = totals.sugar;
  totals_row.querySelector('.acid').innerHTML = totals.acid;
  totals_row.querySelector('.tannin').innerHTML = totals.tannin;
  totals_row.querySelector('.solids').innerHTML = totals.solids;
  totals_row.querySelector('.redness').innerHTML = totals.redness;

  // Update graph
  showGraph();
};

function calcTotalAttrs() {
  sugar = 0;
  acid = 0;
  tannin = 0;
  solids = 0;
  redness = 0;
  document.querySelectorAll(".ingredient-data").forEach( ingr_row => {
    sugar += parseFloat(ingr_row.querySelector('.sugar').innerHTML);
    acid += parseFloat(ingr_row.querySelector('.acid').innerHTML);
    tannin += parseFloat(ingr_row.querySelector('.tannin').innerHTML);
    solids += parseFloat(ingr_row.querySelector('.solids').innerHTML);
    redness += parseFloat(ingr_row.querySelector('.redness').innerHTML);
  });
  return {
    sugar: sugar.toFixed(0),
    acid: acid.toFixed(2),
    tannin: tannin.toFixed(2),
    solids: solids.toFixed(2),
    redness: redness.toFixed(1),
  };
}

function calcIngredientAttrs(ingredient, qty_kg, volume_l) {
  return {
    name: ingredient.name,
    variety: ingredient.variety,
    qty: parseFloat(qty_kg).toFixed(2),
    sugar: (qty_kg * ingredient.sugar / volume_l / 2.64).toFixed(0),
    acid: (qty_kg * ingredient.acid / volume_l).toFixed(2),
    tannin: (qty_kg * ingredient.tannin / volume_l).toFixed(2),
    solids: (qty_kg * ingredient.solu_solid / volume_l).toFixed(2),
    redness: (qty_kg * ingredient.redness / volume_l).toFixed(1),
  };
}

function getStyleData() {
  result =  {
    sugar: (0).toFixed(0),
    acid: (0).toFixed(2),
    tannin: (0).toFixed(2),
    solids: (0).toFixed(2),
  };
  styles.forEach( style => {
    if ( style.id == recipe.style ) {
      result = Object.assign({}, style);
      result.sugar = (result.alcohol * 7.5).toFixed(0);
      result.acid = result.acid.toFixed(2);
      result.tannin = result.tannin.toFixed(2);
      result.solids = result.solu_solid.toFixed(2);
    }
  });
  return result;
}