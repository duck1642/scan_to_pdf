<script>
  import { onDestroy } from 'svelte';
  import DropZone from './components/DropZone.svelte';
  import ImageGrid from './components/ImageGrid.svelte';
  import CropModal from './components/CropModal.svelte';

  let files = []; // Array of { id, file, url, name }
  let pdfName = 'my_note_scans';
  let isLoading = false;
  let editingFile = null;
  let statusMessage = '';
  let statusType = ''; // 'success' or 'error'

  // Clean up object URLs to prevent memory leaks when files are deleted or replaced
  function cleanFileUrls(filesToClean) {
    filesToClean.forEach(f => {
      if (f.url) {
        URL.revokeObjectURL(f.url);
      }
    });
  }

  onDestroy(() => {
    cleanFileUrls(files);
  });

  function handleFilesAdded(event) {
    const newFiles = event.detail.files.map(file => {
      return {
        id: crypto.randomUUID(),
        file: file,
        url: URL.createObjectURL(file),
        name: file.name
      };
    });
    
    files = [...files, ...newFiles];
    showStatus(`Added ${newFiles.length} pages.`, 'success');
  }

  function handleReorder(event) {
    const { fromIndex, toIndex } = event.detail;
    const reordered = [...files];
    const [movedItem] = reordered.splice(fromIndex, 1);
    reordered.splice(toIndex, 0, movedItem);
    files = reordered;
  }

  function handleDelete(event) {
    const { id } = event.detail;
    const itemToDelete = files.find(f => f.id === id);
    if (itemToDelete) {
      URL.revokeObjectURL(itemToDelete.url);
    }
    files = files.filter(f => f.id !== id);
  }

  function handleCropStart(event) {
    const { id } = event.detail;
    editingFile = files.find(f => f.id === id);
  }

  function handleCropSave(event) {
    const { blob, fileName } = event.detail;
    
    // Create new file object from blob
    const croppedFile = new File([blob], fileName, { type: 'image/jpeg' });
    
    files = files.map(f => {
      if (f.id === editingFile.id) {
        // Revoke the old display URL
        URL.revokeObjectURL(f.url);
        
        return {
          ...f,
          file: croppedFile,
          url: URL.createObjectURL(croppedFile)
        };
      }
      return f;
    });
    
    editingFile = null;
    showStatus('Page cropped successfully!', 'success');
  }

  function clearAll() {
    if (confirm('Are you sure you want to clear all uploaded pages?')) {
      cleanFileUrls(files);
      files = [];
      showStatus('All pages cleared.', 'success');
    }
  }

  function showStatus(msg, type) {
    statusMessage = msg;
    statusType = type;
    setTimeout(() => {
      if (statusMessage === msg) {
        statusMessage = '';
      }
    }, 4000);
  }

  async function generatePdf() {
    if (files.length === 0) {
      showStatus('Please add at least one page to compile.', 'error');
      return;
    }

    isLoading = true;
    statusMessage = 'Compiling notes to PDF...';
    statusType = 'success';

    try {
      const formData = new FormData();
      formData.append('output_name', pdfName);
      
      // Append files sequentially to ensure the backend receives them in order
      files.forEach(f => {
        formData.append('images', f.file, f.name);
      });

      // API post via proxy configured in vite.config.js
      const response = await fetch('/api/pdf/merge', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to generate PDF');
      }

      // Read response stream as blob and download it
      const blob = await response.blob();
      const downloadUrl = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = pdfName.endsWith('.pdf') ? pdfName : `${pdfName}.pdf`;
      document.body.appendChild(link);
      link.click();
      
      // Cleanup download URL & link
      URL.revokeObjectURL(downloadUrl);
      document.body.removeChild(link);
      
      showStatus('PDF successfully generated and saved!', 'success');
    } catch (error) {
      showStatus(`Error: ${error.message}`, 'error');
      console.error(error);
    } finally {
      isLoading = false;
    }
  }
</script>

<main class="container">
  <header class="app-header animate-fade-in">
    <div class="logo">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="36" height="36">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <h1>Scan<span class="gradient-text">To</span>PDF</h1>
    </div>
    <p class="subtitle">Convert your photo-taken handwritten notes into clean, organized PDFs locally.</p>
  </header>

  <div class="main-content animate-fade-in">
    <!-- Top upload dropzone -->
    <section class="upload-section">
      <DropZone on:filesAdded={handleFilesAdded} />
    </section>

    <!-- Status notification bar -->
    {#if statusMessage}
      <div class="status-bar glass {statusType} animate-fade-in">
        <p>{statusMessage}</p>
      </div>
    {/if}

    <!-- Visual queue area -->
    {#if files.length > 0}
      <section class="editor-section glass">
        <div class="section-header">
          <div class="meta">
            <h2>Document Pages</h2>
            <span class="count-badge">{files.length} {files.length === 1 ? 'page' : 'pages'}</span>
          </div>
          <button class="btn btn-danger btn-sm" on:click={clearAll}>Clear All</button>
        </div>
        
        <p class="guide-text">Drag and drop pages to re-order. Hover over a page to Crop or Delete.</p>
        
        <ImageGrid 
          {files} 
          on:reorder={handleReorder} 
          on:delete={handleDelete}
          on:crop={handleCropStart}
        />
      </section>

      <!-- Bottom controls for PDF naming and compiling -->
      <section class="compile-controls glass animate-fade-in">
        <div class="input-group">
          <label for="pdf-name">Output PDF Name</label>
          <input 
            type="text" 
            id="pdf-name" 
            bind:value={pdfName} 
            placeholder="e.g. math_lecture_notes" 
          />
        </div>
        
        <button 
          class="btn btn-primary generate-btn" 
          disabled={isLoading || files.length === 0} 
          on:click={generatePdf}
        >
          {#if isLoading}
            <svg class="spinner" viewBox="0 0 50 50">
              <circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle>
            </svg>
            Generating...
          {:else}
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="20" height="20">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Compile PDF
          {/if}
        </button>
      </section>
    {/if}
  </div>

  <!-- Crop Modal (rendered conditionally when editing) -->
  {#if editingFile}
    <CropModal 
      imageUrl={editingFile.url} 
      fileName={editingFile.name} 
      on:close={() => editingFile = null} 
      on:cropSave={handleCropSave}
    />
  {/if}
</main>

<style>
  .container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2.5rem 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .app-header {
    text-align: center;
    margin-bottom: 0.5rem;
  }

  .logo {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.75rem;
    color: var(--accent-cyan);
    margin-bottom: 0.5rem;
  }

  h1 {
    font-size: 2.5rem;
    color: var(--text-primary);
  }

  .gradient-text {
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .subtitle {
    color: var(--text-secondary);
    font-size: 1.05rem;
    max-width: 550px;
    margin: 0 auto;
  }

  .main-content {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .status-bar {
    padding: 0.75rem 1.25rem;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    text-align: center;
    border-left: 4px solid var(--accent-cyan);
  }

  .status-bar.success {
    border-left-color: var(--success);
    background: rgba(16, 185, 129, 0.05);
    color: #a7f3d0;
  }

  .status-bar.error {
    border-left-color: var(--danger);
    background: rgba(244, 63, 94, 0.05);
    color: #fecdd3;
  }

  .editor-section {
    padding: 1.5rem;
    border-radius: var(--radius-lg);
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  h2 {
    font-size: 1.25rem;
    color: var(--text-primary);
  }

  .count-badge {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid var(--border-color);
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.75rem;
    color: var(--text-secondary);
    font-weight: 600;
  }

  .btn-sm {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
    border-radius: var(--radius-sm);
  }

  .guide-text {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 1rem;
  }

  .compile-controls {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 1.5rem;
    border-radius: var(--radius-lg);
    gap: 2rem;
  }

  .input-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    flex: 1;
  }

  .input-group label {
    font-family: var(--font-display);
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-secondary);
  }

  .generate-btn {
    height: 48px;
    padding: 0 2rem;
    white-space: nowrap;
  }

  /* Spinner Animation */
  .spinner {
    animation: rotate 2s linear infinite;
    width: 20px;
    height: 20px;
  }

  .spinner .path {
    stroke: #ffffff;
    stroke-linecap: round;
    animation: dash 1.5s ease-in-out infinite;
  }

  @keyframes rotate {
    100% { transform: rotate(360deg); }
  }

  @keyframes dash {
    0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
    50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
    100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
  }

  @media (max-width: 600px) {
    .compile-controls {
      flex-direction: column;
      align-items: stretch;
      gap: 1rem;
    }
    
    .generate-btn {
      width: 100%;
    }
  }
</style>
