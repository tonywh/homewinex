const recipe_list_template = Handlebars.compile(document.querySelector('#recipe_list').innerHTML);

document.addEventListener('DOMContentLoaded', () => {
  if ( document.querySelector(".this-user-only") ) {
    showActiveTab('mywine');
  } else {
    showActiveTab('recipes');
  }

  // Default sort order is 'name' in the first column. 
  // Style the heading to reflect this
  th = document.querySelector('th');
  th.style.fontStyle = 'italic';
  th.style.fontSize = '1.1em';

  getRecipeList('name');
})

function getRecipeList(order) {
  const request = new XMLHttpRequest();
  if ( document.querySelector(".this-user-only") ) {
    url = '/api/recipelist?' + new URLSearchParams({order: order, thisUserOnly: "true"}).toString();
  } else {
    url = '/api/recipelist?' + new URLSearchParams({order: order}).toString();
  }
  request.open('GET', url);
  request.onload = showRecipeList;
  csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send();
}

function showRecipeList(ev) {
  request = ev.target;
  const data = JSON.parse(request.responseText);

  // Convert create dates to locale specific format
  data.recipes.forEach( recipe => {
    d = new Date(recipe.create_date);
    recipe.create_date = d.toLocaleDateString();
  });

  document.querySelectorAll('.recipe-row').forEach( row => { row.remove(); });
  document.querySelector("#recipe-table").innerHTML += recipe_list_template({recipes: data.recipes});

  // Set on click actions for headings
  document.querySelectorAll('th').forEach( heading => {
    heading.onclick = setSortOrder;
  });

  // Set on click actions for rows
  document.querySelectorAll('.recipe-row').forEach( row => {
    row.onclick = (ev) => {
      url = '/recipe?' + new URLSearchParams({id: ev.currentTarget.dataset.recipe_id}).toString();
      window.location.href = url;
    };
  });
}

function setSortOrder() {
  document.querySelectorAll('th').forEach( heading => {
    heading.style.fontStyle = 'normal';
    heading.style.fontSize = '1em';
  });

  this.style.fontStyle = 'italic';
  this.style.fontSize = '1.1em';
  getRecipeList(this.dataset.order);
}
