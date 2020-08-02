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
    this.dateName = data.dateName;          // The name of date variable to be localised
    this.itemUrl = data.itemUrl;            // url to get an item's page

    self = this;                            // make context available in callbacks

    document.addEventListener('DOMContentLoaded', () => {

      // Default sort order is 'name' in the first column. 
      // Style the heading to reflect this
      var th = document.querySelector(self.tableSelector + ' th');
      th.style.fontStyle = 'italic';
      th.style.fontSize = '1.1em';
    
      self.getList('name');
    })
  }

  getList(order) {
    const request = new XMLHttpRequest();
    self.searchParams.order = order;
    var url = self.listUrl + '?' + new URLSearchParams(self.searchParams).toString();
    request.open('GET', url);
    request.onload = self.showList;
    var csrftoken = Cookies.get('csrftoken');
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.send();
  }

  showList(ev) {
    const request = ev.target;
    const data = JSON.parse(request.responseText);

    // Convert create dates to locale specific format
    if ( self.dateName ) {
      data[self.responseName].forEach( item => {
        var d = new Date(item[self.dateName]);
        item[self.dateName] = d.toLocaleDateString();
      });
    }

    document.querySelectorAll(self.tableSelector + ' ' + self.rowSelector).forEach( row => { row.remove(); });
    document.querySelector(self.tableSelector).innerHTML += self.listTemplate(data);

    // Set on click actions for headings
    document.querySelectorAll(self.tableSelector + ' th').forEach( heading => {
      heading.onclick = self.setSortOrder;
    });

    // Set on click actions for rows
    document.querySelectorAll(self.tableSelector + ' ' + self.rowSelector).forEach( row => {
      row.onclick = (ev) => {
        var url = self.itemUrl + '?' + new URLSearchParams({id: ev.currentTarget.dataset.id}).toString();
        window.location.href = url;
      };
    });
  }

  setSortOrder(ev) {
    document.querySelectorAll(self.tableSelector + ' th').forEach( heading => {
      heading.style.fontStyle = 'normal';
      heading.style.fontSize = '1em';
    });

    ev.target.style.fontStyle = 'italic';
    ev.target.style.fontSize = '1.1em';
    self.getList(ev.target.dataset.order);
  }
}