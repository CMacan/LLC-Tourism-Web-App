function handleSubmit(event) {
  event.preventDefault();
  
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  
  console.log('Attempting login with:', username);

  fetch('/login/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
          username: username,
          password: password
      })
  })
  .then(async response => {
      const responseData = await response.json();
      console.log('Response:', responseData);
      
      if (response.ok) {
          window.location.href = '/dashboard/';
      } else {
          alert(responseData.error || 'Login failed');
      }
  })
  .catch(error => {
      console.error('Error:', error);
      alert('An error occurred');
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

// Handle forgot password link
document.getElementById('forgotPasswordLink').addEventListener('click', function(e) {
    e.preventDefault();
    const email = prompt("Please enter your email:");
    if (email) {
        fetch('/reset_password/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
              email: email
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while resetting password');
        });
    }
});

