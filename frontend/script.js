// Initialize Lucide Icons
lucide.createIcons();

document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');

    const fileInfo = document.getElementById('fileInfo');
    const fileName = document.getElementById('fileName');
    const clearFileBtn = document.getElementById('clearFileBtn');
    const processBtn = document.getElementById('processBtn');

    const uploadSection = document.getElementById('uploadSection');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const resultsSection = document.getElementById('resultsSection');
    const errorNotification = document.getElementById('errorNotification');
    const errorMessage = document.getElementById('errorMessage');

    const newUploadBtn = document.getElementById('newUploadBtn');

    let currentFile = null;

    // --- File Drag and Drop Logic ---

    browseBtn.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-active'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-active'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        let dt = e.dataTransfer;
        let files = dt.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    function handleFileSelect(file) {
        currentFile = file;
        fileName.textContent = file.name;
        dropZone.classList.add('hidden');
        fileInfo.classList.remove('hidden');
        processBtn.classList.remove('hidden');
        errorNotification.classList.add('hidden');
    }

    clearFileBtn.addEventListener('click', () => {
        resetUploadState();
    });

    function resetUploadState() {
        currentFile = null;
        fileInput.value = '';
        dropZone.classList.remove('hidden');
        fileInfo.classList.add('hidden');
        processBtn.classList.add('hidden');
        errorNotification.classList.add('hidden');
    }

    newUploadBtn.addEventListener('click', () => {
        resetUploadState();
        resultsSection.classList.add('hidden');
        uploadSection.classList.remove('hidden');
    });

    // --- API and Processing Logic ---

    processBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        // UI State transition
        uploadSection.classList.add('hidden');
        loadingOverlay.classList.remove('hidden');
        errorNotification.classList.add('hidden');

        try {
            const formData = new FormData();
            formData.append('file', currentFile);

            const response = await fetch('https://vamsi1103-ocr.hf.space/process-document', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.error || `Server error: ${response.status}`);
            }

            const result = await response.json();

            if (result.status === 'success') {
                populateResults(result);
                loadingOverlay.classList.add('hidden');
                resultsSection.classList.remove('hidden');
            } else {
                throw new Error(result.error || 'Unknown processing error');
            }

        } catch (error) {
            showError(error.message);
        }
    });

    function populateResults(res) {
        // Data populated into cards
        document.getElementById('resName').textContent = res.data?.name || 'Not found';
        document.getElementById('resAmount').textContent = res.data?.amount || 'Not found';
        document.getElementById('resDate').textContent = res.data?.date || 'Not found';
        document.getElementById('resId').textContent = res.data?.id || 'Not found';

        // Raw OCR text
        document.getElementById('rawOcrText').value = res.ocr_text || '';

        // Validation banner
        const valBanner = document.getElementById('validationBanner');
        const valText = document.getElementById('validationText');

        if (res.validation?.is_valid) {
            valBanner.className = 'banner success';
            valBanner.innerHTML = `<i data-lucide="check-circle"></i> <span>Data Validation Successful</span>`;
        } else {
            valBanner.className = 'banner error';
            valBanner.innerHTML = `<i data-lucide="x-circle"></i> <span>Validation Failed: ${res.validation?.errors?.join(', ') || 'Errors in data'}</span>`;
        }

        // Action banner
        const actionText = document.getElementById('actionText');
        actionText.textContent = res.action || 'No action taken';

        // Re-init lucide icons for newly injected HTML
        lucide.createIcons();
    }

    function showError(msg) {
        loadingOverlay.classList.add('hidden');
        uploadSection.classList.remove('hidden');
        errorMessage.textContent = msg;
        errorNotification.classList.remove('hidden');
    }
});
