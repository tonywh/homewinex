document.addEventListener('DOMContentLoaded', () => {

  // oninput actions
  document.querySelector('#volume').oninput = enableStart;
})

function enableStart() {
  // Enable if all mandatory inputs are not blank
  disabled = ( document.querySelector('#volume').value <= 0 )

  document.querySelector('.submit').disabled = disabled;

  return true;
}