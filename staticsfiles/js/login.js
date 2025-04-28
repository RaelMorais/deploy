        /**
        * Realiza login do usuário via API.
        * Envia username e password, armazena tokens no localStorage se for bem-sucedido,
        * exibe mensagens de erro ou redireciona em caso de sucesso.
        */
        async function login() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const errorElement = document.getElementById('error');

            try {
                const response = await fetch('https://teste122.azurewebsites.net/api/token/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ username, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    console.log('Token salvo:', data.access); // Para depuração
                    localStorage.setItem('access_token', data.access);
                    localStorage.setItem('refresh_token', data.refresh);
                    errorElement.textContent = 'Login bem-sucedido!';
                    window.location.href = '/votos/';
                } else {
                    errorElement.textContent = data.detail || 'Erro ao fazer login';
                    console.log('Erro no login:', data);
                }
            } catch (error) {
                errorElement.textContent = 'Erro de conexão';
                console.error('Erro:', error);
            }
        }