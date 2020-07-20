const ingredient_template = Handlebars.compile(document.querySelector('#ingredient').innerHTML);
const new_ingredient_template = Handlebars.compile(document.querySelector('#new_ingredient').innerHTML);
const ingredient_totals_template = Handlebars.compile(document.querySelector('#ingredient_totals').innerHTML);
const style_template = Handlebars.compile(document.querySelector('#style').innerHTML);
const style_info_template = Handlebars.compile(document.querySelector('#style_info').innerHTML);

class Converter {
  constructor(data) {
    this.units = data.units;    // array of tuples (id, string), where id is same as index
    this.conv = data.conv;      // array of conv factors indexed by id
  }

  convert(value, fromUnit, toUnit) {
    return value * this.conv[toUnit] / this.conv[fromUnit];
  }

  toString(unit) {
    return this.units[unit][1];
  }
}

var ingredientColours = [
  'rgba(255,0,0,0.2)',
  'rgba(255,100,0,0.2)',
  'rgba(255,200,0,0.2)',
  'rgba(100,255,0,0.2)',
  'rgba(0,255,100,0.2)',
  'rgba(0,100,255,0.2)',
  'rgba(0,0,255,0.2)',
  'rgba(100,0,255,0.2)',
];

var ingredientBorderColours = [
  'rgba(255,0,0,0.4)',
  'rgba(255,100,0,0.4)',
  'rgba(255,200,0,0.4)',
  'rgba(100,255,0,0.4)',
  'rgba(0,255,100,0.4)',
  'rgba(0,100,255,0.4)',
  'rgba(0,0,255,0.4)',
  'rgba(100,0,255,0.4)',
];

var recipe;
var ingredients;
var styles;
var liquid;
var solid;
var totals;
var descrLineHeight;
var barChart;
var profile;
var graphVisible = true;

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

  // update displayed URL - it might have the newrecipe URL still
  page_url = 'recipe?' + new URLSearchParams({id: id}).toString();
  history.pushState({'url': 'recipe', 'id': id}, page_url, page_url);

  // Set actions for name and volume inputs
  document.querySelector('#recipe-name').oninput = () => {
    showSaveButton();
    hideSavedStatus();
  };
  document.querySelector('#volume').oninput = () => {
    recipe.volume_l = document.querySelector('#volume').value;
    updateAfterChange();
  };

  // Set description size and add action for description input
  descr = document.querySelector("#recipe-descr");
  descrLineHeight = descr.scrollHeight;   // HTML/CSS is set to 1 row, no padding
  setDescrSize();
  document.querySelector("#recipe-descr").oninput = () => {
    setDescrSize();
    showSaveButton();
    hideSavedStatus();
  };

  // Add action for Save button
  try {
    document.querySelector("#save-button").onclick = saveRecipe;
  }
  catch(err) {
  }

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
  liquid = new Converter(data.liquid);
  solid = new Converter(data.solid);
  profile = data.profile;

  // If starting a new recipe, get the basic data from the HTML elements already
  // created.
  if ( recipe.id < 0 ) {
    recipe.name = document.querySelector('#recipe-name').innerHTML;
    recipe.volume_l = document.querySelector('#volume').value;
    recipe.descr = document.querySelector('#recipe-descr').innerHTML;
    recipe.style = document.querySelector('#recipe-style').dataset.style_id;
    recipe.ingredients = [];
  }

  if ( profile ) {
    // Set recipe volume to the chosen liquid units. Value from backend is always
    // index zero in the converter.
    volume_el = document.querySelector('#volume');
    volume_el.value = liquid.convert(volume_el.value, 0, profile.liquid_large_units).toFixed(1);
    unit_el = document.querySelector('#volume-unit');
    unit_el.innerHTML = liquid.toString(profile.liquid_large_units);

    // Qty unit string to chosen solid and liquid units.
    unit_el = document.querySelector('#qty-unit');
    liquidStr = liquid.toString(profile.liquid_large_units);
    solidStr = solid.toString(profile.solid_large_units);
    unit_el.innerHTML = `(${solidStr} ${liquidStr})`;
  }

  showStyle();
  showIngredients();
  showGraph();
}

function showStyle() {
  style = getStyleData();
  document.querySelector('#recipe-style').innerHTML = style_template({style: style});
  document.querySelector('#style-info').innerHTML = style_info_template({style: style});
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
        ingr = calcIngredientAttrs(ingredient, use, recipe.volume_l);
        ingr_el.innerHTML += ingredient_template({ingredient: ingr, index: i});
      }
    });
    i++;
  });

  // Ingredient background colours
  i = 0;
  document.querySelectorAll('.ingredient-name').forEach( el => {
    el.style.backgroundColor = i < ingredientColours.length? ingredientColours[i] : 'rgba(0,0,0,0.2)',
    el.style.borderColor = i < ingredientBorderColours.length? ingredientBorderColours[i] : 'rgba(0,0,0,0.4)',
  i++;
  });
  el = document.querySelector('.adacid-label');
  el.style.backgroundColor = ingredientColours[ingredientColours.length-1];
  el.style.borderColor = ingredientBorderColours[ingredientBorderColours.length-1];

  // Set totals
  totals = calcTotalAttrs();
  document.querySelector('#ingredient-totals').innerHTML = ingredient_totals_template({legend: 'TOTALS', totals: totals});

  // Set actions for remove buttons
  ingr_el.querySelectorAll('.remove-button').forEach( el => { 
    el.onclick = (ev) => {
      // Remove the ingredient from the array and updates the page.
      recipe.ingredients.splice(ev.target.dataset.index, 1);
      updateAfterChange();
      return false;
    }
  });

  // Create the drag and drop list
  ingredientSortable = Sortable.create(ingr_el, {
    handle: '.handle', // handle's class
    animation: 150,
    onEnd: dropIngredient,
  });
  
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
      qty_kg: 1.0,
      order: recipe.ingredients.length,
    });
    updateAfterChange();
    return false;
  };
}

function dropIngredient(ev) {
  if (ev.oldDraggableIndex != ev.newDraggableIndex) {
    // In recipe, remove from old position and insert in new position,
    // then renumber the order sequence.
    removed = recipe.ingredients.splice(ev.oldDraggableIndex, 1);
    recipe.ingredients.splice(ev.newDraggableIndex, 0, removed[0]);
    order = 0;
    recipe.ingredients.forEach( ingredient => {
      ingredient.order = order;
      order++;
    });

    // In HTML elements, renumber the order sequence.
    order = 0;
    document.getElementsByName("ingredient_order[]").forEach( el => {
      el.value = order;
      order++;
    });

    showSaveButton();
  }
}

function makeVisibleModalChart() {
  var oldX = 0, oldY = 0;

  document.querySelector('#chart-block').style.visibility = "hidden";
  document.querySelector('#modal-chart-block').style.visibility = "visible";
  document.querySelector('#modal-chart-shadow').style.visibility = "visible";
  document.querySelector('.graph-button').style.visibility = "hidden";
  document.querySelector('.close-button').onclick = hideGraph;
  document.querySelector('#chart-handle').onmousedown = dragGraphDown;
  document.querySelector('#chart-handle').ontouchstart = dragGraphDown;
  if ( window.innerWidth > window.innerHeight ) {
    document.querySelector('#modal-chart-block').classList.remove("portrait");
    document.querySelector('#modal-chart-shadow').classList.remove("portrait");
  } else {
    document.querySelector('#modal-chart-block').classList.add("portrait");
    document.querySelector('#modal-chart-shadow').classList.add("portrait");
  }    
  return document.querySelector('#modal-chart-container canvas').getContext('2d');

  function dragGraphDown(ev) {
    ev.preventDefault();
    if ( Object.prototype.toString.call(ev) === "[object MouseEvent]") {
      x = ev.clientX;
      y = ev.clientY;
      document.onmousemove = dragGraphMove;
      document.onmouseup = dragGraphUp;
    } else {
      x = ev.touches[0].clientX;
      y = ev.touches[0].clientY;
      document.ontouchmove = dragGraphMove;
      document.ontouchend = dragGraphUp;
    }
    oldX = x;
    oldY = y;
  }

  function dragGraphMove(ev) {
    if ( Object.prototype.toString.call(ev) === "[object MouseEvent]") {
      ev.preventDefault();
      x = ev.clientX;
      y = ev.clientY;
    } else {
      x = ev.touches[0].clientX;
      y = ev.touches[0].clientY;
    }
    newX = oldX - x;
    newY = oldY - y;
    dragEl = document.querySelector('#modal-chart-block');
    dragShadowEl = document.querySelector('#modal-chart-shadow');
    dragEl.style.top = (dragEl.offsetTop - newY) + "px";
    dragEl.style.left = (dragEl.offsetLeft - newX) + "px";
    dragShadowEl.style.top = (dragEl.offsetTop - newY) + "px";
    dragShadowEl.style.left = (dragEl.offsetLeft - newX) + "px";
    oldX = x;
    oldY = y;
  }
  
  function dragGraphUp() {
    document.onmousemove = null;
    document.onmouseup = null;
    document.ontouchmove = null;
    document.ontouchend = null;
  }
}

function makeVisibleChart() {
  document.querySelector('#modal-chart-block').style.visibility = "hidden";
  document.querySelector('#modal-chart-shadow').style.visibility = "hidden";
  document.querySelector('#chart-block').style.visibility = "visible";
  document.querySelector('.graph-button').style.visibility = "hidden";
  return document.querySelector('#chart-block canvas').getContext('2d');
}

function hideGraph() {
  document.querySelector('#modal-chart-block').style.visibility = "hidden";
  document.querySelector('#modal-chart-shadow').style.visibility = "hidden";
  document.querySelector('#chart-block').style.visibility = "hidden";
  document.querySelector('.graph-button').style.visibility = "visible";
  graphVisible = false;
  document.querySelector('.graph-button').onclick = forceShowGraph;
}

function forceShowGraph() {
  graphVisible = true;
  showGraph();
}

function showGraph() {
  if ( !graphVisible ) {
    return;
  }

  // Set graph display for mobile or desktop devices
  if ( window.innerWidth < 768
        || window.innerHeight < 768 ) {
    // Mobile
    ctx = makeVisibleModalChart();
  } else {
    // Desktop
    ctx = makeVisibleChart();
  }

  if ( barChart ) {
    barChart.destroy();
  }

  Chart.defaults.global.defaultFontSize = 11;
  Chart.defaults.global.legend.display = false;

  chartData =  {
    type: 'bar',
    data: {
      labels: ['Sugar', 'Acid', 'Tannin', 'Solids'],
      datasets: [      {
        label: 'target',
        stack: 'target',
        backgroundColor: 'rgba(255, 128, 255, 0.5)',
        borderColor: 'rgba(255, 128, 255, 0.7)',
        borderWidth: 1,
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
        text: '% Comparison to Target Values',
        fontSize: 12
      },
      animation: {
        duration: 0
      },
      scales: {
        yAxes: [{
            ticks: {
                beginAtZero: true
            }
        }]
      },
      responsive: true,
      maintainAspectRatio: false
    }
  };

  // Add ingredient data
  i = 0;
  document.querySelectorAll('.ingredient-data').forEach( ingr_row => {
    chartData.data.datasets.push({
      label: ingr_row.querySelector('.ingredient-name').value,
      stack: 'recipe',
      backgroundColor: i < ingredientColours.length? ingredientColours[i] : 'rgba(0,0,0,0.2)',
      borderColor: i < ingredientBorderColours.length? ingredientBorderColours[i] : 'rgba(0,0,0,0.4)',
      borderWidth: 1,
      data: calcChartData({
        sugar: parseFloat(ingr_row.querySelector('.sugar').innerHTML),
        acid: parseFloat(ingr_row.querySelector('.acid').innerHTML),
        tannin: parseFloat(ingr_row.querySelector('.tannin').innerHTML),
        solids: parseFloat(ingr_row.querySelector('.solids').innerHTML),
        }, style),
    });
    i++;
  });

  // Add additional acid from fermentation
  chartData.data.datasets.push({
    label: 'Acid from fermentation',
    stack: 'recipe',
    backgroundColor: ingredientColours[ingredientColours.length-1],
    borderColor: ingredientBorderColours[ingredientBorderColours.length-1],
    borderWidth: 1,
    data: calcChartData({
      sugar: 0,
      acid: 1.5,
      tannin: 0,
      solids: 0,
      }, style),
  });

  barChart = new Chart(ctx, chartData);  
}

function calcChartData(values, style) {
  return [
    (100*values.sugar/style.sugar).toFixed(0),
    (100*values.acid/style.acid).toFixed(0),
    (100*values.tannin/style.tannin).toFixed(0),
    (100*values.solids/style.solu_solid).toFixed(0),
  ];
}

function updateQty(ev) { 
  // Set the values in the existing elements rather than rebuilding HTML,
  // so that the UI runs smoothly making it a more interactive experience.

  showSaveButton();
  hideSavedStatus();

  qty_kg = ev.target.value;
  use = recipe.ingredients[ev.target.dataset.index];
  use.qty_kg = qty_kg;

  // Update values for this ingredient
  ingredients.forEach( ingredient => {
    if ( use.ingredient_id == ingredient.id ) {
      ingr = calcIngredientAttrs(ingredient, use, recipe.volume_l);

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
  acid = 1.5;     // Produced during fermenation
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

function calcIngredientAttrs(ingredient, use, volume_l) {
  // Convert qty to chosen units
  if ( profile ) {
    if (ingredient.liquid == 1000) {
      qty = liquid.convert(use.qty_kg, 0, profile.liquid_large_units);
    } else {
      qty = solid.convert(use.qty_kg, 0, profile.solid_large_units);
    }
  } else {
    qty = parseFloat(use.qty_kg);
  }

  return {
    id: ingredient.id,
    name: ingredient.name,
    variety: ingredient.variety,
    order: use.order,
    qty: qty.toFixed(2),
    sugar: (use.qty_kg * ingredient.sugar / volume_l / 2.64).toFixed(0),
    acid: (use.qty_kg * ingredient.acid / volume_l).toFixed(2),
    tannin: (use.qty_kg * ingredient.tannin / volume_l).toFixed(2),
    solids: (use.qty_kg * ingredient.solu_solid / volume_l).toFixed(2),
    redness: (use.qty_kg * ingredient.redness / volume_l).toFixed(1),
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

function setDescrSize() {
  descr = document.querySelector('#recipe-descr');
  lines = Math.floor(descr.scrollHeight / descrLineHeight);

  if (lines < 1) {
    lines = 1;
  }
  if (lines > 4) {
    lines = 4;
  }
  descr.rows = lines;
}

function saveRecipe() {
  const request = new XMLHttpRequest();
  request.open('POST', `/recipe`);
  const data = new FormData(document.forms.namedItem("recipe-form"));

  request.onload = () => {
    if (request.status == 200) {
      hideSaveButton();
      showSavedStatus();
    }
  };
  
  csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send(data);
  return false;
}

function updateAfterChange() {
  showSaveButton();
  hideSavedStatus();
  showIngredients();
  showGraph();
}

function showSaveButton() {
  try {
    document.querySelector('#save-button').style.visibility = "visible"
  }
  catch(err) {
  }
}


function hideSaveButton() {
  try {
    document.querySelector('#save-button').style.visibility = "hidden"
  }
  catch(err) {
  }
}

function showSavedStatus() {
  try {
    document.querySelector('#save-status').style.visibility = "visible"
    document.querySelector('#save-status').classList.add("fade");
  }
  catch(err) {
  }
}

function hideSavedStatus() {
  try {
    document.querySelector('#save-status').style.visibility = "hidden"
    document.querySelector('#save-status').classList.remove("fade");
  }
  catch(err) {
  }
}
