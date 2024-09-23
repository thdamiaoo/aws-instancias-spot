let currentPageInstancias = 1; // Página atual para instâncias
let currentPageHistorico = 1; // Página atual para histórico

/**
 * Cria os botões de paginação com base no total de itens e na página atual.
 * @param {number} total - Total de itens para paginar.
 * @param {number} currentPage - Página atual.
 * @param {string} type - Tipo de paginação ('instancias' ou 'historico').
 */
function criarPaginas(total, currentPage, type) {
    const paginationDiv = document.getElementById(`pagination-${type}`);
    paginationDiv.innerHTML = ''; // Limpa a paginação existente

    const totalPages = Math.ceil(total / 10); // Ajuste conforme o page_size definido

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        button.className = (i === currentPage) ? 'active' : ''; // Marca a página atual
        button.onclick = () => {
            if (type === 'instancias') {
                currentPageInstancias = i; // Atualiza a página atual de instâncias
                consultarInstancias(currentPageInstancias); // Consulta instâncias
            } else {
                currentPageHistorico = i; // Atualiza a página atual de histórico
                consultarHistoricoPrecos(currentPageHistorico); // Consulta histórico
            }
        };
        paginationDiv.appendChild(button); // Adiciona o botão à paginação
    }
}

/**
 * Carrega as regiões disponíveis da AWS e as adiciona ao select.
 */
function carregarRegioes() {
    const selectRegiao = document.getElementById('regiao');
    fetch('http://127.0.0.1:5000/regioes')
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao carregar as regiões.');
            }
            return response.json();
        })
        .then(regioes => {
            regioes.forEach(regiao => {
                const option = document.createElement('option');
                option.value = regiao; // Valor da opção
                option.textContent = regiao; // Texto exibido
                selectRegiao.appendChild(option); // Adiciona a opção ao select
            });
        })
        .catch(error => {
            document.getElementById('error-message').textContent = error.message; // Exibe mensagem de erro
        });
}

/**
 * Consulta as instâncias Spot da AWS com base nos parâmetros fornecidos.
 * @param {number} pagina - Número da página a ser consultada.
 */
function consultarInstancias(pagina = 1) {
    const regiao = document.getElementById('regiao').value;
    const os = document.getElementById('os').value; // Sistema operacional
    const cpu = document.getElementById('cpu').value;
    const memoria = document.getElementById('memoria').value;
    const tipoInstancia = document.getElementById('tipo_instancia').value;
    const emr = document.getElementById('emr').checked;

    if (!regiao || !cpu || !memoria || tipoInstancia.length < 3) {
        alert("Por favor, preencha todos os campos necessários.");
        return; // Retorna se os campos não estiverem preenchidos
    }

    const queryString = new URLSearchParams({
        regiao: regiao,
        os: os,
        cpu: cpu,
        memoria: memoria,
        tipo_instancia: tipoInstancia,
        emr: emr,
        page: pagina // Adiciona a página na query string
    }).toString();

    fetch(`http://127.0.0.1:5000/instancias_spot?${queryString}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar instâncias.');
            }
            return response.json();
        })
        .then(data => {
            const tbodyInstancias = document.querySelector('#resultados-instancias tbody');
            tbodyInstancias.innerHTML = ''; // Limpa os resultados existentes

            if (data.instances.length > 0) {
                data.instances.forEach(instancia => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${instancia.InstanceType}</td>
                        <td>${instancia.vCPU}</td>
                        <td>${instancia['Memory GiB']}</td>
                        <td>${instancia['Savings over On-Demand']}</td>
                        <td>${instancia['Frequency of interruption']}</td>
                        <td>${instancia.OS}</td>
                    `;
                    tbodyInstancias.appendChild(row); // Adiciona a linha à tabela
                });
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="6">Nenhuma instância encontrada.</td>'; // Mensagem se não encontrar instâncias
                tbodyInstancias.appendChild(row);
            }

            // Atualizando a paginação
            criarPaginas(data.total, pagina, 'instancias'); // Adiciona total aqui
        })
        .catch(error => {
            document.getElementById('error-message').textContent = error.message; // Exibe mensagem de erro
        });
}

/**
 * Consulta o histórico de preços das instâncias com base nos parâmetros fornecidos.
 * @param {number} pagina - Número da página a ser consultada.
 */
function consultarHistoricoPrecos(pagina = 1) {
    const regiao = document.getElementById('regiao').value;
    const tipoInstancia = document.getElementById('tipo_instancia_hist').value;

    if (tipoInstancia.length < 3) {
        alert("O tipo de instância deve ter no mínimo 3 caracteres.");
        return; // Retorna se o tipo de instância for inválido
    }

    const queryString = new URLSearchParams({
        regiao: regiao,
        tipo_instancia: tipoInstancia,
        page: pagina // Adiciona a página na query string
    }).toString();

    fetch(`http://127.0.0.1:5000/coletar_historico_precos?${queryString}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao buscar histórico de preços.');
            }
            return response.json();
        })
        .then(data => {
            const tbodyHistorico = document.querySelector('#resultados-historico tbody');
            tbodyHistorico.innerHTML = ''; // Limpa os resultados existentes

            if (data.historico_precos.length > 0) {
                data.historico_precos.forEach(item => {
                    const row = document.createElement('tr');
                    const priceInCents = (parseFloat(item.SpotPrice)).toFixed(4); // Formata o preço
                    row.innerHTML = `
                        <td>${item.InstanceType}</td>
                        <td>${item.vCPU}</td>
                        <td>${item['Memory GiB']}</td>
                        <td>$${priceInCents}</td>
                        <td>${item['Savings over On-Demand']}</td>
                        <td>${item['Frequency of interruption']}</td>
                        <td>${item['Update Date']}</td>
                    `;
                    tbodyHistorico.appendChild(row); // Adiciona a linha à tabela
                });
            } else {
                const row = document.createElement('tr');
                row.innerHTML = '<td colspan="7">Nenhum dado histórico encontrado.</td>'; // Mensagem se não encontrar dados
                tbodyHistorico.appendChild(row);
            }

            // Atualizando a paginação
            criarPaginas(data.total, pagina, 'historico'); // Adiciona total aqui
        })
        .catch(error => {
            document.getElementById('error-message').textContent = error.message; // Exibe mensagem de erro
        });
}

// Carrega as regiões assim que o documento estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    carregarRegioes();
});
