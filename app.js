const filters = document.querySelectorAll('[data-filter]');
const cards = document.querySelectorAll('[data-category]');
filters.forEach(button => button.addEventListener('click', () => {
  filters.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
  let count = 0;
  cards.forEach(card => {
    card.hidden = button.dataset.filter !== 'Todos' && card.dataset.category !== button.dataset.filter;
    if (!card.hidden) count++;
  });
  document.getElementById('result-count').textContent = `${count} entregáveis`;
}));
