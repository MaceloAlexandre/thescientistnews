// Sincroniza os modos manualmente
document.getElementById("darkmode-toggle").addEventListener("change", function () {
    // Desmarca modo leitura se estiver marcado
    document.getElementById("leituramode-toggle").checked = false;
    localStorage.setItem("modo", this.checked ? "dark" : "");
    syncIframeModo(this.checked ? "dark" : "");
});

document.getElementById("leituramode-toggle").addEventListener("change", function () {
    // Desmarca modo escuro se estiver marcado
    document.getElementById("darkmode-toggle").checked = false;
    localStorage.setItem("modo", this.checked ? "leitura" : "");
    syncIframeModo(this.checked ? "leitura" : "");
});

// Carrega modo salvo do localStorage ao abrir
window.addEventListener("DOMContentLoaded", function () {
    const modo = localStorage.getItem("modo");
    document.getElementById("darkmode-toggle").checked = modo === "dark";
    document.getElementById("leituramode-toggle").checked = modo === "leitura";
});

// Envia modo para iframe
function syncIframeModo(modo) {
    const iframe = document.getElementById("iframeposts");
    if (iframe && iframe.contentWindow) {
        iframe.contentWindow.postMessage({ tipo: "modo", valor: modo }, "*");
    }
}
