function ativarModo(modo) {
    // Remove ambos os modos primeiro
    document.body.classList.remove('dark-mode', 'reading-mode');
  
    if (modo === 'dark') {
      document.body.classList.add('dark-mode');
      localStorage.setItem('modo', 'dark');
    } else if (modo === 'leitura') {
      document.body.classList.add('reading-mode');
      localStorage.setItem('modo', 'leitura');
    } else {
      localStorage.removeItem('modo');
    }
  
    // 🔄 Aplica o mesmo modo no iframe, se estiver presente
    const iframe = document.getElementById('iframeposts');
    if (iframe && iframe.contentWindow) {
      iframe.contentWindow.postMessage({ tipo: 'modo', valor: modo }, '*');
    }
  }
  
  
  // Ao carregar a página, aplica o modo salvo
  document.addEventListener('DOMContentLoaded', function () {
    const modoSalvo = localStorage.getItem('modo');
    if (modoSalvo === 'dark') {
      document.body.classList.add('dark-mode');
    } else if (modoSalvo === 'leitura') {
      document.body.classList.add('reading-mode');
    }
  });
  

  window.addEventListener('message', function (event) {
    if (event.data && event.data.tipo === 'modo') {
      const modo = event.data.valor;
  
      document.body.classList.remove('dark-mode', 'reading-mode');
  
      if (modo === 'dark') {
        document.body.classList.add('dark-mode');
        localStorage.setItem('modo', 'dark');
      } else if (modo === 'leitura') {
        document.body.classList.add('reading-mode');
        localStorage.setItem('modo', 'leitura');
      } else {
        localStorage.removeItem('modo');
      }
    }
  });

  const modoToggle = document.getElementById('modo-toggle');

  // Lista cíclica de modos
  const modos = ["", "dark", "leitura"];
  let index = 0;

  // Detecta modo salvo
  const modoSalvo = localStorage.getItem("modo");
  if (modoSalvo === "dark") index = 1;
  else if (modoSalvo === "leitura") index = 2;

  // Aplica o modo salvo
  ativarModo(modos[index]);

  // Ao clicar no botão:
  modoToggle.addEventListener("change", () => {
    index = (index + 1) % modos.length;
    ativarModo(modos[index]);
    modoToggle.checked = false; // reseta o checkbox para reutilizar
  });