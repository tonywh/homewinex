function showActiveTab(name) {
  console.log("here");
  // Make all tabs inactive except the selected tab
  document.querySelectorAll('.menubar .nav-item').forEach( item => {
    if ( item.dataset.name == name ) {
      item.classList.add("active");
      console.log("active", name);
    } else {
      item.classList.remove("active");
      console.log("inactive", name);
    }
  });
}
