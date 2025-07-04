
document.addEventListener('DOMContentLoaded', () => {
    const fileForm = document.getElementById('fileForm');
    const loading = document.getElementById('loading');
    const cancelBtn = document.getElementById('cancelBtn');
    let controller;
    if (fileForm) {
        fileForm.addEventListener('submit', (e) => {
            e.preventDefault();
            loading.classList.remove('hidden');
            cancelBtn.classList.remove('hidden');
            controller = new AbortController();
            const formData = new FormData(fileForm);
            fetch(fileForm.action, {
                method: 'POST',
                body: formData,
                signal: controller.signal
            })
            .then(resp => resp.text())
            .then(html => {
                loading.classList.add('hidden');
                cancelBtn.classList.add('hidden');
                document.open();
                document.write(html);
                document.close();
            })
            .catch(err => {
                loading.classList.add('hidden');
                cancelBtn.classList.add('hidden');
                if (err.name === 'AbortError') {
                    alert('Upload canceled');
                } else {
                    alert('Upload failed');
                }
            });
        });
        cancelBtn.addEventListener('click', () => {
            if (controller) {
                controller.abort();
            }
        });
    }
});
