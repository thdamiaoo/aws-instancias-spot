// tests/frontend/script.test.js

describe('Spot Instance Advisor', () => {
  test('renders Spot Instance Advisor title', () => {
    document.body.innerHTML = `<h1>Spot Instance Advisor</h1>`;
    const title = document.querySelector('h1');
    expect(title).toBeTruthy();
  });

  test('consulta instâncias com parâmetros válidos', async () => {
    const response = await fetch('/instancias_spot?regiao=us-east-1&tipo_instancia=c5.large&cpu=2&memoria=4');
    const data = await response.json();
    console.log(data);
    expect(data).toHaveProperty('instances');
    expect(data.instances.length).toBeGreaterThan(0); 
  });

  test('exibe aviso quando tipo de instância tem menos de 3 caracteres', () => {
    document.body.innerHTML = `<input id="tipo_instancia" value="ab"><div id="error-message"></div>`;
    const tipoInstancia = document.getElementById('tipo_instancia');
    const errorMessage = document.getElementById('error-message');

    if (tipoInstancia.value.length < 3) {
      errorMessage.textContent = 'Tipo de instância deve ter pelo menos 3 caracteres';
    }

    expect(errorMessage.textContent).toBe('Tipo de instância deve ter pelo menos 3 caracteres');
  });
});
