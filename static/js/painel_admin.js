// Image Preview Functionality
const fileUpload = document.getElementById('file-upload');
const previewImage = document.getElementById('previewImage');
const imagePreview = document.getElementById('imagePreview');
const placeholder = imagePreview.querySelector('.placeholder');

fileUpload.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(event) {
            previewImage.src = event.target.result;
            previewImage.style.display = 'block';
            placeholder.style.display = 'none';
        }
        
        reader.readAsDataURL(file);
    } else {
        previewImage.style.display = 'none';
        placeholder.style.display = 'block';
    }
});

document.getElementById('post-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Impede o envio padrão

    const titulo = document.getElementById('post-title').value;
    if (!titulo) {
        alert('Por favor, preencha o título.');
        return;
    }

    const form = e.target;
    const formData = new FormData(form);

    fetch('/postar', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            alert('Post criado com sucesso!');
            form.reset(); // limpa o formulário
        } else {
            alert('Erro ao criar o post.');
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        alert('Erro na conexão com o servidor.');
    });
});

        const menuItems = document.querySelectorAll(".admin-menu li");
        const sections = document.querySelectorAll(".admin-section");

        menuItems.forEach(item => {
            item.addEventListener("click", (e) => {
                e.preventDefault();

                // Remove 'active' de todos os itens e seções
                menuItems.forEach(i => i.classList.remove("active"));
                sections.forEach(s => s.classList.remove("active"));

                // Ativa o item clicado e a seção correspondente
                item.classList.add("active");
                const target = item.getAttribute("data-section");
                document.getElementById(target).classList.add("active");
            });
        });