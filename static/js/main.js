document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const uploadStatus = document.getElementById('uploadStatus');
    const processButton = document.getElementById('processButton');
    const resultsSection = document.getElementById('resultsSection');
    const loading = document.getElementById('loading');
    const autoDetectLang = document.getElementById('autoDetectLang');
    const languageSelector = document.getElementById('languageSelector');
    const processAll = document.getElementById('processAll');
    const pageRangeInput = document.getElementById('pageRangeInput');

    // Current state
    let currentPage = 1;
    let totalPages = 1;

    // Event Listeners
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('drop', handleDrop);
    fileInput.addEventListener('change', handleFileSelect);
    processButton.addEventListener('click', processFile);
    document.getElementById('clearResults').addEventListener('click', clearResults);
    document.getElementById('copyText').addEventListener('click', copyText);
    document.getElementById('prevPage').addEventListener('click', () => changePage(-1));
    document.getElementById('nextPage').addEventListener('click', () => changePage(1));

    // Tab switching
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab + 'Content').classList.add('active');
        });
    });

    // Toggle handlers
    autoDetectLang.addEventListener('change', () => {
        languageSelector.style.display = autoDetectLang.checked ? 'none' : 'block';
    });

    processAll.addEventListener('change', () => {
        pageRangeInput.style.display = processAll.checked ? 'none' : 'block';
    });

    // File handling functions
    function handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('dragover');
    }

    function handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        handleFiles(files);
    }

    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type === 'application/pdf') {
                uploadFile(file);
            } else {
                showError('الرجاء تحميل ملف PDF فقط');
            }
        }
    }

    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            showLoading('جاري تحميل الملف...');
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.success) {
                showSuccess('تم تحميل الملف بنجاح');
                processButton.disabled = false;
            } else {
                showError(data.error || 'حدث خطأ أثناء تحميل الملف');
            }
        } catch (error) {
            showError('حدث خطأ أثناء تحميل الملف');
        } finally {
            hideLoading();
        }
    }

    async function processFile() {
        const settings = {
            auto_detect_lang: autoDetectLang.checked,
            manual_langs: getSelectedLanguages(),
            process_all: processAll.checked,
            page_range: document.getElementById('pageRange').value,
            use_ocr: document.getElementById('useOcr').checked,
            enhance_images: document.getElementById('enhanceImages').checked,
            correct_spelling: document.getElementById('correctSpelling').checked,
            remove_extra_spaces: document.getElementById('removeExtraSpaces').checked
        };

        try {
            showLoading('جاري معالجة الملف...');
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(settings)
            });
            const data = await response.json();

            if (data.success) {
                totalPages = data.total_pages;
                currentPage = 1;
                showResults();
                loadPage(currentPage);
            } else {
                showError(data.error || 'حدث خطأ أثناء معالجة الملف');
            }
        } catch (error) {
            showError('حدث خطأ أثناء معالجة الملف');
        } finally {
            hideLoading();
        }
    }

    async function loadPage(page) {
        try {
            const response = await fetch(`/view/${page}`);
            const data = await response.json();

            if (response.ok) {
                document.getElementById('extractedText').value = data.text;
                document.getElementById('pageInfo').textContent = `صفحة ${page} من ${data.total_pages}`;
                
                if (data.has_image) {
                    document.getElementById('pageImage').src = `/image/${page}`;
                }

                document.getElementById('prevPage').disabled = page <= 1;
                document.getElementById('nextPage').disabled = page >= data.total_pages;
            } else {
                showError(data.error || 'حدث خطأ أثناء تحميل الصفحة');
            }
        } catch (error) {
            showError('حدث خطأ أثناء تحميل الصفحة');
        }
    }

    function changePage(delta) {
        const newPage = currentPage + delta;
        if (newPage >= 1 && newPage <= totalPages) {
            currentPage = newPage;
            loadPage(currentPage);
        }
    }

    async function clearResults() {
        try {
            const response = await fetch('/clear', {
                method: 'POST'
            });
            const data = await response.json();

            if (data.success) {
                resultsSection.style.display = 'none';
                uploadStatus.innerHTML = '';
                fileInput.value = '';
                processButton.disabled = true;
            }
        } catch (error) {
            showError('حدث خطأ أثناء مسح النتائج');
        }
    }

    function copyText() {
        const textArea = document.getElementById('extractedText');
        textArea.select();
        document.execCommand('copy');
        showSuccess('تم نسخ النص بنجاح!');
    }

    // Utility functions
    function getSelectedLanguages() {
        const select = document.getElementById('languages');
        return Array.from(select.selectedOptions).map(option => [option.value, option.text]);
    }

    function showLoading(message) {
        loading.querySelector('p').textContent = message;
        loading.style.display = 'block';
    }

    function hideLoading() {
        loading.style.display = 'none';
    }

    function showError(message) {
        uploadStatus.innerHTML = `<div class="alert alert-error">${message}</div>`;
    }

    function showSuccess(message) {
        uploadStatus.innerHTML = `<div class="alert alert-success">${message}</div>`;
    }

    function showResults() {
        resultsSection.style.display = 'block';
    }
});
