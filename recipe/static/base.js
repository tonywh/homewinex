function showActiveTab(name) {
  // Make all tabs inactive except the selected tab
  document.querySelectorAll('.menubar .nav-item').forEach( item => {
    if ( item.dataset.name == name ) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });
}
