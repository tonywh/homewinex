const ingredient_template = Handlebars.compile(document.querySelector('#ingredient').innerHTML);
const new_ingredient_template = Handlebars.compile(document.querySelector('#new_ingredient').innerHTML);

var recipe;

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
  console.log(url);
  request.open('GET', url);
  request.onload = showRecipe;
  csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send();
}

function showRecipe(ev) {
  request = ev.target;
  const data = JSON.parse(request.responseText);

  // Keep a copy of the recipe to allow us to build it then submit it
  recipe = data.recipe;

  // If starting a new recipe, get the basic data from the HTML elements already
  // created.
  if ( recipe.id < 0 ) {
    recipe.name = document.querySelector('#recipe-name').innerHTML;
    recipe.volume = document.querySelector('#recipe-volume').innerHTML;
    recipe.descr = document.querySelector('#recipe-descr').innerHTML;
    recipe.ingredients = [];
  }

  // Create an ingredient line for each ingredient in the recipe
  document.querySelector("#ingredients").innerHTML = "";
  recipe.ingredients.forEach( id => {
    // data.ingredients.forEach( d_ingredient => {
    //   if ( id == d_ingredient.id ) {
    //     ingr = {
    //       name: ingredient.name,
    //       qty: ingredient.qty,    // kg, or l
    
    //     };
    //     break;
    //   }
    // });

  });

  // Create new ingredient input selector and button
  document.querySelector('#ingredient-select').innerHTML = new_ingredient_template({ingredients: data.ingredients});
  document.querySelector('#new_ingr_select').oninput = (ev) => {
    document.querySelector('#new_ingr_button').disabled = (ev.target.value == -1);
    return true;
  };
  document.querySelector('#new_ingr_button').onclick = () => {
//    recipe.ingredients.push({id: name: })
  };
}
