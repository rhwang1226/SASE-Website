document.addEventListener('DOMContentLoaded', () => {

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
  
    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
      el.addEventListener('click', () => {
  
        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);
  
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
  
      });
    });
  
  });

  // Get the file input element
const fileInput = document.querySelector('.file-input');

// Add event listener for file selection
fileInput.addEventListener('change', handleFileSelection);

// Handle file selection
function handleFileSelection(event) {
  // Get the selected file
  const selectedFile = event.target.files[0];
  
  if (selectedFile) {
    // Display the file name
    const fileNameElement = document.querySelector('.file-name');
    fileNameElement.textContent = selectedFile.name;
    
    // Perform any additional operations with the file
    // For example, you can read the file contents or upload it to a server
    // Here, we'll just log the file object to the console
    console.log(selectedFile);
  }
}
