import {TableList} from './tablelist.js';

document.addEventListener('DOMContentLoaded', () => {
  if ( document.querySelector(".this-user-only") ) {
    showActiveTab('mywine');
  } else {
    showActiveTab('recipes');
  }
})

const recipe_list_template = Handlebars.compile(document.querySelector('#recipe_list').innerHTML);

var searchParams = {};
if ( document.querySelector(".this-user-only") ) {
  searchParams.thisUserOnly = 'true';
}
var recipeList = new TableList({
  tableSelector: '#recipe-table',
  rowSelector: '.recipe-row',
  listUrl: '/api/recipelist',
  searchParams: searchParams,
  itemUrl: '/recipe',
  listTemplate: recipe_list_template,
  responseName: 'recipes',
  dateName: 'create_date',
});