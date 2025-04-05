document.addEventListener('DOMContentLoaded', function() {
    // Menu Hamburguer
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navItems = document.querySelectorAll('.nav-item');

    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Fechar menu ao clicar em um item
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            if (item.classList.contains('dropdown')) {
                item.classList.toggle('active');
            } else {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    });

    // Fechar menu ao clicar fora
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.navbar') && !e.target.closest('.hamburger')) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });
});