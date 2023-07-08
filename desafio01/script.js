document.addEventListener("DOMContentLoaded", function() {
    // Obtenha o formulário de login
    var loginForm = document.getElementById("login-form");
  
    // Adicione um evento de clique ao botão de entrada
    var entrarButton = loginForm.querySelector("button[type='submit']");
    entrarButton.addEventListener("click", function(event) {
      event.preventDefault(); // Impede o envio do formulário padrão
      window.location.href = "products.html"; // Redireciona para a página
    });
  });

  document.getElementById('forgot-password-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var emailInput = document.getElementById('email');
    var email = emailInput.value;

    if (email.trim() === '') {
      alert('Por favor, preencha o campo de e-mail.');
    } else {
      document.getElementById('popup').classList.add('show');
      setTimeout(function() {
        window.location.href = 'index.html';
      }, 1000);
    }
  })