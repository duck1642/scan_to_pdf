<script>
  import { createEventDispatcher } from 'svelte';
  import ImageCard from './ImageCard.svelte';
  
  export let files = []; // [{ id, file, url, name }]
  
  const dispatch = createEventDispatcher();
  
  let draggedIndex = null;
  let dragOverIndex = null;

  function handleDragStart(event) {
    draggedIndex = event.detail.index;
  }

  function handleDragOver(e, index) {
    e.preventDefault();
    dragOverIndex = index;
  }

  function handleDragLeave() {
    // Avoid resetting immediately if entering another child, 
    // but dragend will handle final cleanup
  }

  function handleDrop(e, targetIndex) {
    e.preventDefault();
    
    if (draggedIndex !== null && draggedIndex !== targetIndex) {
      dispatch('reorder', { 
        fromIndex: draggedIndex, 
        toIndex: targetIndex 
      });
    }
    
    cleanupDragState();
  }

  function cleanupDragState() {
    draggedIndex = null;
    dragOverIndex = null;
  }

  function handleDelete(event) {
    dispatch('delete', event.detail);
  }

  function handleCrop(event) {
    dispatch('crop', event.detail);
  }
</script>

<div class="grid-container">
  {#each files as fileObj, i (fileObj.id)}
    <div 
      class="grid-item {dragOverIndex === i ? 'drag-over' : ''}"
      on:dragover={(e) => handleDragOver(e, i)}
      on:dragleave={handleDragLeave}
      on:drop={(e) => handleDrop(e, i)}
    >
      <ImageCard 
        {fileObj} 
        index={i} 
        on:dragStart={handleDragStart}
        on:dragEnd={cleanupDragState}
        on:delete={handleDelete}
        on:crop={handleCrop}
      />
    </div>
  {/each}
</div>

<style>
  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1.25rem;
    width: 100%;
    margin-top: 1.5rem;
  }

  .grid-item {
    transition: var(--transition-smooth);
    border-radius: var(--radius-md);
    border: 2px solid transparent;
  }

  /* Glow highlight when dragging over an item to show drop target */
  .grid-item.drag-over {
    border-color: var(--accent-cyan);
    box-shadow: var(--shadow-glow);
    transform: scale(1.02);
  }

  /* Responsive styling adjustments */
  @media (max-width: 600px) {
    .grid-container {
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
      gap: 0.8rem;
    }
  }
</style>
