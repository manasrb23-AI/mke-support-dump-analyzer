const fileInput = document.getElementById('file-input');
const uploadZone = document.getElementById('upload-zone');
const progressBar = document.getElementById('progress-bar');
const progressContainer = document.getElementById('progress-bar-container');
const statusText = document.getElementById('status-text');

// Drag and drop handlers
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    if (e.dataTransfer.files.length > 0) {
        handleFile(e.dataTransfer.files[0]);
    }
});

uploadZone.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        handleFile(fileInput.files[0]);
    }
});

function handleFile(file) {
    if (!file.name.endsWith('.tar.gz') && !file.name.endsWith('.tgz') && !file.name.endsWith('.zip')) {
        alert('Please upload a .tar.gz or .zip support dump.');
        return;
    }

    uploadFile(file);
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const xhr = new XMLHttpRequest();

    // Show progress
    progressContainer.classList.remove('hidden');
    statusText.textContent = `Uploading ${file.name}...`;

    xhr.upload.addEventListener('progress', (e) => {
        if (e.lengthComputable) {
            const percentComplete = (e.loaded / e.total) * 100;
            progressBar.style.width = percentComplete + '%';
        }
    });

    xhr.addEventListener('load', () => {
        if (xhr.status === 200) {
            statusText.textContent = 'Analysis Complete! Redirecting...';
            // Replace document content with response (the report page)
            document.open();
            document.write(xhr.responseText);
            document.close();

            // Re-bind scripts if necessary, but document.write usually kills them.
            // A better SPA approach would be to return JSON and render, 
            // but for this simple MVP, replacing the page content works or we can just navigate.

            // Alternative: The server returns HTML, so we just dumped it.
            // To make the URL pretty we could use history.pushState if we cared.
        } else {
            statusText.textContent = 'Error during analysis: ' + (xhr.responseText || 'Unknown error');
            statusText.style.color = '#ef4444';
        }
    });

    xhr.addEventListener('error', () => {
        statusText.textContent = 'Network error occurred.';
        statusText.style.color = '#ef4444';
    });

    xhr.open('POST', '/upload', true);
    xhr.send(formData);
}
