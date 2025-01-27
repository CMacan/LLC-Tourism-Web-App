function toggleChatbot() {
    const chatbotContainer = document.getElementById("chatbot_container");
    const chatbotIcon = document.getElementById("chatbot_icon");
    if (chatbotContainer.style.display === "flex") {
      chatbotContainer.style.display = "none";
      chatbotIcon.style.display = "flex";
    } else {
      chatbotContainer.style.display = "flex";
      chatbotIcon.style.display = "none";
    }
  }

  function handleKeyPress(event) {
    if (event.key === "Enter") {
      event.preventDefault(); // Prevent default form submission
      sendMessage(); // Call sendMessage function to handle the message
    }
  }

  async function sendMessage() {
    const userMessage = document.getElementById("user_message").value;
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    if (!userMessage) {
      alert("Please enter a message.");
      return;
    }

    try {
      const response = await fetch("/chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ message: userMessage }),
      });

      if (response.ok) {
        const data = await response.json();
        const chatBox = document.getElementById("chat_box");
        chatBox.innerHTML += `
          <div class="chat_message user_message">
            <p><b>You:</b> ${userMessage}</p>
          </div>`;
        chatBox.innerHTML += `
          <div class="chat_message chatbot_message">
            <div class="profile_pic"></div>
            <p><b>Lapu-Lapu AI:</b> ${data.response}</p>
          </div>`;
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
        document.getElementById("user_message").value = "";
      } else {
        console.error(
          "Error in response:",
          response.status,
          response.statusText
        );
        alert("Failed to get a response from the bot.");
      }
    } catch (error) {
      console.error("Error in fetch:", error);
      alert("An error occurred while sending the message.");
    }
}
function toggleDropdown() {
  const dropdownMenu = document.getElementById("dropdown-menu");
  dropdownMenu.style.display =
    dropdownMenu.style.display === "none" ? "block" : "none";
}

function selectCategory(category) {
  document.getElementById("selected-category").textContent = category;
  toggleDropdown();
}