import {TableList} from './tablelist.js';

document.addEventListener('DOMContentLoaded', () => {
  showActiveTab('mywine');
})

const recipe_list_template = Handlebars.compile(document.querySelector('#recipe_list').innerHTML);
const brew_list_template = Handlebars.compile(document.querySelector('#brew_list').innerHTML);

var searchParams = {thisUserOnly: 'true'};
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

var brewList = new TableList({
  tableSelector: '#brew-table',
  rowSelector: '.brew-row',
  listUrl: '/api/brewlist',
  searchParams: searchParams,
  itemUrl: '/brew',
  listTemplate: brew_list_template,
  responseName: 'brews',
  dateNames: ['updated', 'started'],
});
