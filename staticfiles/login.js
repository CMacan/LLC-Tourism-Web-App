document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const otpForm = document.getElementById('otpForm');
    const otpModal = new bootstrap.Modal(document.getElementById('otpModal'));
    const otpInputs = document.querySelectorAll('.otp-input');
    
    // Handle login form submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        
        try {
            const response = await fetch('/admin_side/send-otp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ email: email })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                otpModal.show();
            } else {
                alert(data.error || 'Failed to send OTP');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to send OTP. Please try again.');
        }
    });

    // Handle OTP verification
    otpForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const otp = Array.from(otpInputs).map(input => input.value).join('');
        const email = document.getElementById('email').value;

        try {
            const response = await fetch('/admin_side/verify-otp/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ 
                    email: email,
                    otp: otp 
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                window.location.href = '/admin_side/dashboard/';
            } else {
                alert(data.error || 'Invalid OTP');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to verify OTP. Please try again.');
        }
    });

    // CSRF Token helper function
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
});

document.addEventListener('DOMContentLoaded', function () {
    const otpInputs = document.querySelectorAll('.otp-input');
    const otpForm = document.getElementById('otpForm');
    const otpTimerElement = document.getElementById('otpTimer');
    const verifyButton = otpForm.querySelector('button[type="submit"]');
    
    let otpExpiryTime; // Time when the OTP will expire
    let countdownInterval;
  
    function startOTPTimer(durationInSeconds) {
      const now = Date.now();
      otpExpiryTime = now + durationInSeconds * 1000;
  
      updateCountdown(); // Initialize the timer display
      countdownInterval = setInterval(updateCountdown, 1000);
    }
  
    function updateCountdown() {
      const remainingTime = Math.max(0, otpExpiryTime - Date.now());
      const minutes = Math.floor(remainingTime / (1000 * 60));
      const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
  
      // Update the timer display
      otpTimerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  
      if (remainingTime <= 0) {
        clearInterval(countdownInterval);
        handleOTPExpiry();
      }
    }
  
    function handleOTPExpiry() {
      otpTimerElement.textContent = 'Expired';
      verifyButton.disabled = true;
      otpInputs.forEach(input => input.disabled = true);
      alert('The OTP has expired. Please request a new one.');
    }
  
    otpForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      const otp = Array.from(otpInputs).map(input => input.value).join('');
      const email = document.getElementById('email').value;
  
      try {
        const response = await fetch('/admin_side/verify-otp/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
          },
          body: JSON.stringify({ email, otp }),
        });
  
        if (response.ok) {
          // Redirect on success
          window.location.href = '/admin_side/dashboard/';
        } else {
          // Parse the response error
          const data = await response.json();
          alert(data.error || 'Invalid OTP');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Failed to verify OTP. Please try again.');
      }
    });
  
    function getCookie(name) {
      const cookieValue = document.cookie.split('; ').find((row) => row.startsWith(name + '='));
      return cookieValue ? cookieValue.split('=')[1] : null;
    }
  
    // Simulate starting the OTP modal with a 3-minute expiry time
    document.getElementById('loginForm').addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      localStorage.setItem('lastEmail', email);
  
      // Start OTP timer (3 minutes)
      startOTPTimer(180);
  
      // Open OTP modal
      const otpModal = new bootstrap.Modal(document.getElementById('otpModal'));
      otpModal.show();
    });
  });
  

