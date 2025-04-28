        /**
        * Exporta dados para um arquivo Excel via requisição GET autenticada.
        * Requer token JWT salvo no localStorage. Em caso de sucesso, faz o download
        * do arquivo. Em caso de erro, exibe mensagens apropriadas ao usuário.
        */
        async function exportarExcel() {
            const token = localStorage.getItem('access_token');
            const errorElement = document.getElementById('error');

            // Pegar o token e exibir no console 
            console.log('Token:', token); // depuração

            // Se não houver token, exibe erro e redireciona para login
            if (!token) {
                errorElement.textContent = 'Você precisa estar logado para exportar.';
                window.location.href = '/login/';
                return;
            }
            // Realiza requisão GET pro exportar 
            try {
                const response = await fetch('http://127.0.0.1:8000/exportar/', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                // Apenas para depuração no console 
                console.log('Status da resposta:', response.status); // Depuração 
                console.log('Headers enviados:', { Authorization: `Bearer ${token}` }); // depuração

                // Exibindo status da resposta 
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'votosElogiar.xlsx';
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    errorElement.textContent = 'Arquivo exportado com sucesso!';
                    // Log de erro (exibindo mensagem de sucesso no "error")
                } else {
                    const contentType = response.headers.get('content-type');
                    let errorData = {};
                    if (contentType && contentType.includes('application/json')) {
                        errorData = await response.json();
                    }
                    errorElement.textContent = errorData.detail || `Erro ao exportar o arquivo (status: ${response.status}).`;
                    console.log('Erro na resposta:', errorData);
                    // Exibindo erro da resposta no 'error' -> Não alterar 
                }
            } catch (error) {
                errorElement.textContent = 'Erro de conexão. Verifique o servidor.';
                // Não alterar --> Importante, sem isso, os métodos caso deem erro, irá retornar um callback, "derrubando a aplicação"
                console.error('Erro:', error);
            }
        }