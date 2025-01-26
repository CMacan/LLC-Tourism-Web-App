function toggleDropdown() {
    const dropdownMenu = document.getElementById("dropdown-menu");
    if (dropdownMenu.style.display === "none") {
      dropdownMenu.style.display = "block";
    } else {
      dropdownMenu.style.display = "none";
    }
  }
  
  

function selectCategory(category) {
    document.getElementById('selected-category').textContent = category;
    toggleDropdown();
}

