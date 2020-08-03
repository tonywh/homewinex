/*
 * Class that works with a HTML table sortable by headings,
 * and rows hyperlink to individually identified items.
 */
export class TableList {

  constructor(data) {
    this.tableSelector = data.tableSelector;// table selector
    this.listTemplate = data.listTemplate;  // list template
    this.rowSelector = data.rowSelector;    // row selector
    this.listUrl = data.listUrl;            // search url
    this.searchParams = data.searchParams;  // list of additional constant search parameters
    this.responseName = data.responseName;  // Name of the list in the response data
    this.dateNames = data.dateNames;        // The name of date variable to be localised
    this.itemUrl = data.itemUrl;            // url to get an item's page

    document.addEventListener('DOMContentLoaded', () => {

      // Default is to sort by the first column. 
      var th = document.querySelector(this.tableSelector + ' th');
      th.style.fontStyle = 'italic';
      th.style.fontSize = '1.1em';
      this.getList(th.dataset.order);
    })
  }

  getList(order) {
    const request = new XMLHttpRequest();
    this.searchParams.order = order;
    var url = this.listUrl + '?' + new URLSearchParams(this.searchParams).toString();
    request.open('GET', url);
    request.onload = (ev) => {this.showList(ev)};
    var csrftoken = Cookies.get('csrftoken');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.send();
  }

  showList(ev) {
    const request = ev.target;
    const data = JSON.parse(request.responseText);
    
    // Convert dates to locale specific format
    if ( this.dateNames ) {
      this.dateNames.forEach( name => {
        data[this.responseName].forEach( item => {
          var d = new Date(item[name]);
          item[name] = d.toLocaleDateString();
        });
      });
    }

    document.querySelectorAll(this.tableSelector + ' ' + this.rowSelector).forEach( row => { row.remove(); });
    document.querySelector(this.tableSelector).innerHTML += this.listTemplate(data);

    // Set on click actions for headings
    document.querySelectorAll(this.tableSelector + ' th').forEach( heading => {
      heading.onclick = (ev) => {this.setSortOrder(ev)};
    });

    // Set on click actions for rows
    document.querySelectorAll(this.tableSelector + ' ' + this.rowSelector).forEach( row => {
      row.onclick = (ev) => {
        var url = this.itemUrl + '?' + new URLSearchParams({id: ev.currentTarget.dataset.id}).toString();
        window.location.href = url;
      };
    });
  }

  setSortOrder(ev) {
    document.querySelectorAll(this.tableSelector + ' th').forEach( heading => {
      heading.style.fontStyle = 'normal';
      heading.style.fontSize = '1em';
    });

    ev.target.style.fontStyle = 'italic';
    ev.target.style.fontSize = '1.1em';
    this.getList(ev.target.dataset.order);
  }
}