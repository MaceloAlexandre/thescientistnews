// ============== FUNCIONALIDADES EXISTENTES ============== //

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

// Form Submission
document.getElementById('post-form').addEventListener('submit', function(e) {
    e.preventDefault();

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
            form.reset();
        } else {
            alert('Erro ao criar o post.');
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
        alert('Erro na conexão com o servidor.');
    });
});

// Menu Navigation
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

        // Se for a seção de revisão, carrega os links automaticamente
        if (target === 'revisar') {
            buscarLinksParaRevisao();
        }
    });
});

// ============== NOVAS FUNCIONALIDADES PARA REVISÃO ============== //

// Buscar links para revisão
function buscarLinksParaRevisao() {
    const revisarSection = document.getElementById('revisar');
    const loadingHTML = `
        <h2 class="section-title"><i class="fas fa-check-circle"></i> Revisar Postagens</h2>
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Buscando links para revisão...</p>
        </div>
    `;
    
    // Substitui todo o conteúdo pelo loading
    revisarSection.innerHTML = loadingHTML;
    
    fetch('/api/links-para-revisao')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                revisarSection.innerHTML = `
                    <h2 class="section-title"><i class="fas fa-check-circle"></i> Revisar Postagens</h2>
                    <div class="error-state">
                        <i class="fas fa-exclamation-triangle"></i>
                        <p>${data.error}</p>
                        <button id="retry-button" class="btn btn-primary">Tentar novamente</button>
                    </div>
                `;
                document.getElementById('retry-button').addEventListener('click', buscarLinksParaRevisao);
                return;
            }
            
            if (data.links && data.links.length > 0) {
                renderizarLinks(data.links);
            } else {
                revisarSection.innerHTML = `
                    <h2 class="section-title"><i class="fas fa-check-circle"></i> Revisar Postagens</h2>
                    <div class="empty-state">
                        <i class="fas fa-exclamation-circle"></i>
                        <p>Nenhum link encontrado para revisão.</p>
                        <button id="buscar-links" class="btn btn-primary">
                            <i class="fas fa-search"></i> Buscar Novamente
                        </button>
                    </div>
                `;
                document.getElementById('buscar-links').addEventListener('click', buscarLinksParaRevisao);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            revisarSection.innerHTML = `
                <h2 class="section-title"><i class="fas fa-check-circle"></i> Revisar Postagens</h2>
                <div class="error-state">
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>Erro ao carregar links. Verifique sua conexão.</p>
                    <button id="retry-button" class="btn btn-primary">Tentar novamente</button>
                </div>
            `;
            document.getElementById('retry-button').addEventListener('click', buscarLinksParaRevisao);
        });
}
// Renderizar links na seção de revisão
function renderizarLinks(links) {
    const revisarSection = document.getElementById('revisar');
    let linksHTML = `
        <h2 class="section-title"><i class="fas fa-check-circle"></i> Revisar Postagens</h2>
        <div class="links-container">
            <div class="links-header">
                <h3>Links Encontrados (${links.length})</h3>
                <button id="atualizar-links" class="btn btn-secondary">
                    <i class="fas fa-sync-alt"></i> Atualizar
                </button>
            </div>
            <div class="links-grid">
    `;
    
    links.forEach(link => {
        linksHTML += `
            <div class="link-card">
                <div class="link-title">${link.titulo}</div>
                
                <!-- Container ajustado -->
                <div style="
                    min-height: 240px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    background: #f5f5f5;
                    margin: 10px 0;
                    border-radius: 4px;
                    position: relative;  <!-- Novo -->
                    overflow: hidden;  <!-- Novo -->
                ">
                    ${link.imagem ? 
                        `<img src="${link.imagem}" 
                              alt="Imagem" 
                              style="
                                  max-width: 100%;
                                  max-height: 100%;
                                  width: auto;
                                  height: 250px;
                                  position: absolute;  <!-- Novo -->
                                  top: 50%;  <!-- Novo -->
                                  left: 50%;  <!-- Novo -->
                                  transform: translate(-50%, -50%);  <!-- Novo -->
                                  object-fit: contain;
                                  border-radius: 4px;
                              ">` 
                        : `<div style="color: #999;">Sem imagem</div>`
                    }
                </div>
                
                <div class="link-actions">
                    <button class="btn btn-primary editar-link" data-url="${link.url}">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                </div>
            </div>
        `;
    });
    
    revisarSection.innerHTML = linksHTML;
    
    // Adiciona eventos aos botões de editar
    document.querySelectorAll('.editar-link').forEach(btn => {
        btn.addEventListener('click', function() {
            abrirEditorLink(this.getAttribute('data-url'));
        });
    });
    
    // Adiciona evento de atualização de links
    document.getElementById('atualizar-links').addEventListener('click', buscarLinksParaRevisao);
}



function abrirEditorLink(url) {
    const revisarSection = document.getElementById('revisar');
    const imagePreview = document.getElementById('imagePreview');
    
    // Estado de carregamento
    revisarSection.innerHTML = `
        <h2 class="section-title"><i class="fas fa-check-circle"></i> Revisar Postagens</h2>
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Processando: ${url}</p>
        </div>
    `;

    fetch(`/api/get-link-content?url=${encodeURIComponent(url)}`)
        .then(response => {
            if (!response.ok) throw new Error(`Erro HTTP! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (!data.success || !data.postagem) {
                throw new Error(data.error || 'Conteúdo não pôde ser extraído');
            }

            const p = data.postagem;
            
            // Preenche os campos básicos
            document.getElementById('post-title').value = p.titulo || '';
            document.getElementById('post-summary').value = p.resumo || '';
            document.getElementById('post-materia').value = p.materia;
            
            // GERENCIAMENTO DA FONTE ORIGINAL - COM DEPURAÇÃO
            console.log('URL da fonte original:', url); // Log para depuração
            
            // Remove qualquer input existente
            const existingInput = document.getElementById('fonte-original');
            if (existingInput) {
                existingInput.remove();
            }
            
            // Cria novo input hidden
            const fonteInput = document.createElement('input');
            fonteInput.type = 'hidden';
            fonteInput.id = 'fonte-original';
            fonteInput.name = 'fonte_original';
            fonteInput.value = url;
            
            // Adiciona ao formulário
            document.getElementById('post-form').appendChild(fonteInput);
            
            // Verificação final
            console.log('Campo fonte_original criado:', {
                id: fonteInput.id,
                name: fonteInput.name,
                value: fonteInput.value
            });
            
            // Preenche categoria
            if (p.categoria) {
                const select = document.getElementById('post-category');
                const option = [...select.options].find(opt => 
                    opt.value.toLowerCase() === p.categoria.toLowerCase()
                );
                if (option) option.selected = true;
            }
            
            // Imagem
            const previewImg = document.getElementById('previewImage');
            const placeholder = imagePreview.querySelector('.placeholder');
            
            if (p.midia) {
                previewImg.src = p.midia;
                previewImg.style.display = 'block';
                placeholder.style.display = 'none';
                
                // Gerencia o campo hidden da mídia
                let midiaInput = document.getElementById('midia-url');
                if (!midiaInput) {
                    midiaInput = document.createElement('input');
                    midiaInput.type = 'hidden';
                    midiaInput.id = 'midia-url';
                    midiaInput.name = 'midia_url';
                    document.getElementById('post-form').appendChild(midiaInput);
                }
                midiaInput.value = p.midia;
            } else {
                previewImg.style.display = 'none';
                placeholder.style.display = 'block';
            }
            
            // Ativa seção
            menuItems.forEach(i => i.classList.remove("active"));
            sections.forEach(s => s.classList.remove("active"));
            document.querySelector('.admin-menu li[data-section="criar"]').classList.add("active");
            document.getElementById('criar').classList.add("active");
        })
        .catch(error => {
            console.error("Erro detalhado:", error);
            
            let errorMsg = error.message.includes("Failed to fetch") 
                ? "Falha na conexão com o servidor" 
                : error.message;
            
            revisarSection.innerHTML = `
                <h2 class="section-title"><i class="fas fa-check-circle"></i> Revisar Postagens</h2>
                <div class="error-state">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Erro ao processar o link</h3>
                    <p>${errorMsg}</p>
                    <p class="small">URL: ${url}</p>
                    <div class="mt-3">
                        <button id="retry-button" class="btn btn-primary">
                            <i class="fas fa-sync-alt"></i> Tentar novamente
                        </button>
                        <button id="back-button" class="btn btn-secondary ml-2">
                            <i class="fas fa-arrow-left"></i> Voltar
                        </button>
                    </div>
                </div>
            `;
            
            document.getElementById('retry-button').addEventListener('click', () => abrirEditorLink(url));
            document.getElementById('back-button').addEventListener('click', buscarLinksParaRevisao);
        });
}