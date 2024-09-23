// jest.setup.js
global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({ instances: [{ id: 1, type: 'c5.large' }] }), // Mock de instâncias
    })
  );
  