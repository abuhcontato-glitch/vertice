const previewDialog = document.getElementById('preview-dialog');
const previewImage = document.getElementById('preview-image');
const previewTitle = document.getElementById('preview-title');
const previewDownload = document.getElementById('preview-download');
let lastPreviewButton;
document.querySelectorAll('[data-preview]').forEach(button => {
  button.addEventListener('click', () => {
    lastPreviewButton = button;
    previewImage.src = button.dataset.preview;
    previewImage.alt = button.dataset.title;
    previewTitle.textContent = button.dataset.title;
    previewDownload.href = button.dataset.preview;
    previewDialog.showModal();
    document.body.classList.add('modal-open');
  });
});
document.getElementById('close-preview').addEventListener('click', () => previewDialog.close());
previewDialog.addEventListener('click', event => {
  if (event.target !== previewDialog) return;
  const box = previewDialog.getBoundingClientRect();
  if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) previewDialog.close();
});
previewDialog.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  if (lastPreviewButton) lastPreviewButton.focus();
});
