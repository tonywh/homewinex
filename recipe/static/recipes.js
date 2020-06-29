const recipe_list_template = Handlebars.compile(document.querySelector('#recipe_list').innerHTML);

document.addEventListener('DOMContentLoaded', () => {
  getRecipeList('name');
})

function getRecipeList(order) {
  const request = new XMLHttpRequest();
  url = '/recipelist?' + new URLSearchParams({order: order}).toString();
  request.open('GET', url);
  request.onload = showRecipeList;
  csrftoken = Cookies.get('csrftoken');
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send();
}

function showRecipeList(ev) {
  request = ev.target;
  const data = JSON.parse(request.responseText);
  
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
