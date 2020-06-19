document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.form-control').forEach( input => {
    input.onkeyup = enableSave;
  });
  document.querySelectorAll('.custom-control-input').forEach( input => {
    input.onclick = enableSave;
  });
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