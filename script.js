document.addEventListener('DOMContentLoaded', async () => {
  const grid = document.getElementById('properties-grid');
  const filters = document.querySelectorAll('.filter-btn');
  let currentFilter = 'all';
  let PROPERTIES = [];

  // Load properties from JSON (allows automatic updates)
  try {
    const response = await fetch('properties.json');
    PROPERTIES = await response.json();
  } catch (err) {
    console.error('Erro ao carregar imóveis:', err);
    grid.innerHTML = '<p>Erro ao carregar os imóveis. Tente novamente mais tarde.</p>';
    return;
  }

  function render(props) {
    if (props.length === 0) {
      grid.innerHTML = '<p>Nenhum imóvel encontrado com esse filtro.</p>';
      return;
    }
    grid.innerHTML = props.map(p => `
      <article class="card">
        <img src="${p.img || ''}" alt="${p.titulo}" loading="lazy" onerror="this.style.display='none'">
        <div class="card-body">
          <div class="card-type">${p.tipo || 'Imóvel'} · Cód ${p.codigo || ''}</div>
          <h3>${p.titulo}</h3>
          <div class="card-price">${p.preco || 'Sob consulta'}</div>
          <div class="card-location">${p.local || ''}</div>
          <a class="details" href="${p.href}" target="_blank" rel="noopener">Ver detalhes completos →</a>
        </div>
      </article>
    `).join('');
  }

  function applyFilter() {
    const filtered = currentFilter === 'all' 
      ? PROPERTIES 
      : PROPERTIES.filter(p => (p.tipo || '').toLowerCase().includes(currentFilter.toLowerCase()));
    render(filtered);
  }

  filters.forEach(btn => {
    btn.addEventListener('click', () => {
      filters.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.dataset.type;
      applyFilter();
    });
  });

  applyFilter();
});
