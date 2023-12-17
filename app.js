// Example function for handling form submission
function submitForm() {
    // Get form input values
    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;
    var vulnerability = document.getElementById('vulnerability').value;
    var description = document.getElementById('description').value;
  
    // Simple form validation
    if (!name || !email || !vulnerability || !description) {
      alert('Please fill in all fields');
      return;
    }
  
    // Prepare data to send to the server
    var formData = {
      name: name,
      email: email,
      vulnerability: vulnerability,
      description: description,
    };
  
    // Use AJAX to send data to the server
    var xhr = new XMLHttpRequest();
    var url = '/submit_bug'; // Replace with the actual server endpoint
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
  
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          // Handle successful response from the server
          alert('Bug submitted successfully!');
        } else {
          // Handle error response from the server
          alert('Error submitting bug. Please try again later.');
        }
      }
    };
  
    // Convert formData to JSON before sending
    var jsonData = JSON.stringify(formData);
    xhr.send(jsonData);
  }
  