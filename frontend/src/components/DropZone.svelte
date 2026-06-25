<script>
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();
  let isDragging = false;
  let fileInput;
  let folderInput;

  function handleDragOver(e) {
    e.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  function handleDrop(e) {
    e.preventDefault();
    isDragging = false;
    
    if (e.dataTransfer.files) {
      processFiles(e.dataTransfer.files);
    }
  }

  function handleFileSelect(e) {
    if (e.target.files) {
      processFiles(e.target.files);
    }
  }

  function processFiles(fileList) {
    const validImages = [];
    for (let i = 0; i < fileList.length; i++) {
      const file = fileList[i];
      // Accept JPEG, PNG, WEBP, GIF, and HEIC/HEIF files (backend handles conversion)
      if (file.type.startsWith('image/') || /\.(heic|heif)$/i.test(file.name)) {
        validImages.push(file);
      }
    }
    
    if (validImages.length > 0) {
      dispatch('filesAdded', { files: validImages });
    }
    
    // Clear value to allow selecting same files/folder again
    if (fileInput) fileInput.value = '';
    if (folderInput) folderInput.value = '';
  }
</script>

<div 
  class="dropzone glass {isDragging ? 'dragging' : ''}"
  on:dragover={handleDragOver}
  on:dragleave={handleDragLeave}
  on:drop={handleDrop}
  role="button"
  tabindex="0"
  aria-label="File upload dropzone"
>
  <input 
    type="file" 
    multiple 
    accept="image/*" 
    bind:this={fileInput} 
    on:change={handleFileSelect} 
    class="hidden-input" 
    id="file-picker"
  />
  <input 
    type="file" 
    webkitdirectory 
    directory 
    bind:this={folderInput} 
    on:change={handleFileSelect} 
    class="hidden-input" 
    id="folder-picker"
  />

  <div class="dropzone-content">
    <!-- Combined Document Icon -->
    <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 13h6m-3-3v6m-9 1V4a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
    </svg>
    
    <h3>Drag & Drop Note Photos Here</h3>
    <p class="subtitle">Supports JPG, PNG, WEBP, HEIC</p>
    
    <div class="actions">
      <label for="file-picker" class="btn btn-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Select Files
      </label>
      
      <label for="folder-picker" class="btn btn-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
        </svg>
        Select Folder
      </label>
    </div>
  </div>
</div>

<style>
  .dropzone {
    border: 2px dashed var(--border-color);
    border-radius: var(--radius-lg);
    padding: 3rem 2rem;
    text-align: center;
    transition: var(--transition-smooth);
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 250px;
    cursor: default;
  }

  .dropzone:hover, .dropzone.dragging {
    border-color: var(--accent-cyan);
    background: rgba(6, 182, 212, 0.03);
    box-shadow: var(--shadow-glow);
  }

  .hidden-input {
    display: none;
  }

  .dropzone-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .upload-icon {
    width: 64px;
    height: 64px;
    color: var(--text-secondary);
    transition: var(--transition-smooth);
  }

  .dropzone:hover .upload-icon, .dropzone.dragging .upload-icon {
    color: var(--accent-cyan);
    transform: translateY(-4px);
  }

  h3 {
    font-size: 1.3rem;
    color: var(--text-primary);
  }

  .subtitle {
    font-size: 0.9rem;
    color: var(--text-muted);
  }

  .actions {
    display: flex;
    gap: 1rem;
    margin-top: 0.5rem;
  }

  label {
    margin: 0;
  }
</style>
