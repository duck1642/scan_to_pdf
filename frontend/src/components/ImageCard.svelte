<script>
  import { createEventDispatcher } from 'svelte';
  
  export let fileObj; // { id, file, url, name }
  export let index;
  
  const dispatch = createEventDispatcher();
  
  let isHovered = false;

  function handleDragStart(e) {
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', index);
    dispatch('dragStart', { index });
  }

  function handleDragEnd() {
    dispatch('dragEnd');
  }

  function handleDelete() {
    dispatch('delete', { id: fileObj.id });
  }

  function handleCrop() {
    dispatch('crop', { id: fileObj.id });
  }
</script>

<div 
  class="card glass"
  draggable="true"
  on:dragstart={handleDragStart}
  on:dragend={handleDragEnd}
  on:mouseenter={() => isHovered = true}
  on:mouseleave={() => isHovered = false}
>
  <div class="index-badge">{index + 1}</div>
  
  <div class="thumbnail-container">
    <img src={fileObj.url} alt={fileObj.name} draggable="false" />
    
    {#if isHovered}
      <div class="overlay animate-fade-in">
        <button class="icon-btn crop-btn" title="Crop/Edit Page" on:click={handleCrop}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="18" height="18">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h8M8 7V5a2 2 0 012-2h4m-6 4H5m11 0h3m-7 10h4m-4 0v3m0-3h3m2-13v13m-2-13H9" />
          </svg>
        </button>
        <button class="icon-btn delete-btn" title="Remove Page" on:click={handleDelete}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="18" height="18">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    {/if}
  </div>

  <div class="card-info">
    <p class="filename" title={fileObj.name}>{fileObj.name}</p>
  </div>
</div>

<style>
  .card {
    position: relative;
    border-radius: var(--radius-md);
    overflow: hidden;
    cursor: grab;
    transition: var(--transition-smooth);
    display: flex;
    flex-direction: column;
    height: 220px;
    width: 100%;
  }

  .card:hover {
    transform: translateY(-4px);
    border-color: var(--accent-cyan);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), var(--shadow-glow);
  }

  .card:active {
    cursor: grabbing;
  }

  .index-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 10;
    background: var(--accent-gradient);
    color: #ffffff;
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 0.85rem;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 2px 8px rgba(6, 182, 212, 0.4);
  }

  .thumbnail-container {
    position: relative;
    flex: 1;
    background: rgba(0, 0, 0, 0.25);
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    border-bottom: 1px solid var(--border-color);
  }

  img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    transition: var(--transition-smooth);
  }

  .card:hover img {
    transform: scale(1.02);
  }

  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(4, 7, 13, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    z-index: 5;
  }

  .icon-btn {
    border: none;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: var(--transition-smooth);
    color: #ffffff;
  }

  .crop-btn {
    background: rgba(6, 182, 212, 0.2);
    border: 1px solid rgba(6, 182, 212, 0.4);
  }

  .crop-btn:hover {
    background: var(--accent-cyan);
    transform: scale(1.1);
  }

  .delete-btn {
    background: rgba(244, 63, 94, 0.2);
    border: 1px solid rgba(244, 63, 94, 0.4);
  }

  .delete-btn:hover {
    background: var(--danger);
    transform: scale(1.1);
  }

  .card-info {
    padding: 0.6rem;
    background: rgba(15, 23, 42, 0.3);
  }

  .filename {
    font-size: 0.75rem;
    color: var(--text-secondary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-align: center;
  }
</style>
