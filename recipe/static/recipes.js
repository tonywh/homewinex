import {TableList} from './tablelist.js';

document.addEventListener('DOMContentLoaded', () => {
  showActiveTab('recipes');
})

const recipe_list_template = Handlebars.compile(document.querySelector('#recipe_list').innerHTML);

var searchParams = {};
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