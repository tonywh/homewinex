document.addEventListener('DOMContentLoaded', () => {

  // oninput actions
  document.querySelector('#name').oninput = enableCreate;
  document.querySelector('#style').oninput = (ev) => {
    i = ev.target.selectedIndex;
    options = ev.target.options;
    if ( i == 0 ) {
      document.querySelector('#target-alcohol').innerHTML = "";
      document.querySelector('#target-acid').innerHTML = "";
      document.querySelector('#target-tannin').innerHTML = "";
      document.querySelector('#target-solids').innerHTML = "";
    } else {
      document.querySelector('#target-alcohol').innerHTML = parseFloat(options[i].dataset.alcohol).toFixed(1) + "%<br>alc";
      document.querySelector('#target-acid').innerHTML = parseFloat(options[i].dataset.acid).toFixed(2) + "<br>acid (g/l)";
      document.querySelector('#target-tannin').innerHTML = parseFloat(options[i].dataset.tannin).toFixed(2) + "<br>tannin (g/l)";
      document.querySelector('#target-solids').innerHTML = parseFloat(options[i].dataset.solids).toFixed(2) + "<br>sol. solids (g/l)";
    }

    enableCreate();
  };
  document.querySelector('#volume').oninput = enableCreate;

})

function enableCreate() {
  // Enable if all mandatory inputs are not blank
  disabled = ( document.querySelector('#name').value == ""
               || document.querySelector('#style').value < 0
               || document.querySelector('#volume').value <= 0 )

  document.querySelector('.submit').disabled = disabled;

  return true;
}