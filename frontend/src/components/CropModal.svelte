<script>
  import { onMount, createEventDispatcher } from 'svelte';
  
  export let imageUrl = '';
  export let fileName = '';
  
  const dispatch = createEventDispatcher();
  
  let canvas;
  let ctx;
  let imageObj;
  
  // Dimensions and scaling
  let canvasWidth = 500;
  let canvasHeight = 400;
  let scaleFactor = 1; // original / display
  
  // Crop area coordinates (in canvas pixels)
  let cropX = 50;
  let cropY = 50;
  let cropW = 200;
  let cropH = 200;
  
  // Mouse interaction state
  let isDraggingBox = false;
  let activeHandle = null; // 'nw', 'ne', 'se', 'sw', or null
  let startX = 0;
  let startY = 0;
  let startCropX = 0;
  let startCropY = 0;
  let startCropW = 0;
  let startCropH = 0;
  
  const HANDLE_SIZE = 12;
  const MIN_SIZE = 40;

  onMount(() => {
    loadImage();
  });

  function loadImage() {
    imageObj = new Image();
    imageObj.onload = () => {
      // Calculate display dimensions to fit maximum size
      const maxW = Math.min(window.innerWidth * 0.8, 650);
      const maxH = Math.min(window.innerHeight * 0.6, 500);
      
      let w = imageObj.width;
      let h = imageObj.height;
      
      if (w > maxW) {
        h = (maxW / w) * h;
        w = maxW;
      }
      if (h > maxH) {
        w = (maxH / h) * w;
        h = maxH;
      }
      
      canvasWidth = w;
      canvasHeight = h;
      scaleFactor = imageObj.width / w;
      
      // Initialize crop box to be 80% of canvas centered
      cropW = w * 0.8;
      cropH = h * 0.8;
      cropX = (w - cropW) / 2;
      cropY = (h - cropH) / 2;
      
      // Ensure canvas has the correct width/height attributes
      canvas.width = w;
      canvas.height = h;
      ctx = canvas.getContext('2d');
      
      draw();
    };
    imageObj.src = imageUrl;
  }

  function draw() {
    if (!ctx || !imageObj) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    
    // 1. Draw base image
    ctx.drawImage(imageObj, 0, 0, canvasWidth, canvasHeight);
    
    // 2. Draw darkened overlay outside crop box
    ctx.fillStyle = 'rgba(0, 0, 0, 0.55)';
    
    // Top
    ctx.fillRect(0, 0, canvasWidth, cropY);
    // Bottom
    ctx.fillRect(0, cropY + cropH, canvasWidth, canvasHeight - (cropY + cropH));
    // Left (between top and bottom)
    ctx.fillRect(0, cropY, cropX, cropH);
    // Right (between top and bottom)
    ctx.fillRect(cropX + cropW, cropY, canvasWidth - (cropX + cropW), cropH);
    
    // 3. Draw crop box outline
    ctx.strokeStyle = 'var(--accent-cyan)';
    ctx.lineWidth = 2;
    ctx.strokeRect(cropX, cropY, cropW, cropH);
    
    // 4. Draw drag handles
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = 'var(--accent-cyan)';
    ctx.lineWidth = 2;
    
    const handles = getHandleCoords();
    Object.values(handles).forEach(h => {
      ctx.fillRect(h.x - HANDLE_SIZE / 2, h.y - HANDLE_SIZE / 2, HANDLE_SIZE, HANDLE_SIZE);
      ctx.strokeRect(h.x - HANDLE_SIZE / 2, h.y - HANDLE_SIZE / 2, HANDLE_SIZE, HANDLE_SIZE);
    });
  }

  function getHandleCoords() {
    return {
      nw: { x: cropX, y: cropY },
      ne: { x: cropX + cropW, y: cropY },
      se: { x: cropX + cropW, y: cropY + cropH },
      sw: { x: cropX, y: cropY + cropH }
    };
  }

  function hitTest(x, y) {
    const handles = getHandleCoords();
    
    // Check handles first
    for (const [key, h] of Object.entries(handles)) {
      if (Math.abs(x - h.x) <= HANDLE_SIZE && Math.abs(y - h.y) <= HANDLE_SIZE) {
        return key;
      }
    }
    
    // Check if inside crop box
    if (x >= cropX && x <= cropX + cropW && y >= cropY && y <= cropY + cropH) {
      return 'box';
    }
    
    return null;
  }

  function handleMouseDown(e) {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    
    const hit = hitTest(x, y);
    if (!hit) return;
    
    startX = e.clientX;
    startY = e.clientY;
    startCropX = cropX;
    startCropY = cropY;
    startCropW = cropW;
    startCropH = cropH;
    
    if (hit === 'box') {
      isDraggingBox = true;
    } else {
      activeHandle = hit;
    }
  }

  function handleMouseMove(e) {
    if (!isDraggingBox && !activeHandle) return;
    
    const dx = e.clientX - startX;
    const dy = e.clientY - startY;
    
    if (isDraggingBox) {
      // Move whole box, boundary check
      let newX = startCropX + dx;
      let newY = startCropY + dy;
      
      if (newX < 0) newX = 0;
      if (newY < 0) newY = 0;
      if (newX + cropW > canvasWidth) newX = canvasWidth - cropW;
      if (newY + cropH > canvasHeight) newY = canvasHeight - cropH;
      
      cropX = newX;
      cropY = newY;
    } else {
      // Resize using handles
      if (activeHandle === 'nw') {
        let newX = startCropX + dx;
        let newY = startCropY + dy;
        let newW = startCropW - dx;
        let newH = startCropH - dy;
        
        if (newX >= 0 && newW >= MIN_SIZE) {
          cropX = newX;
          cropW = newW;
        }
        if (newY >= 0 && newH >= MIN_SIZE) {
          cropY = newY;
          cropH = newH;
        }
      } else if (activeHandle === 'ne') {
        let newY = startCropY + dy;
        let newW = startCropW + dx;
        let newH = startCropH - dy;
        
        if (cropX + newW <= canvasWidth && newW >= MIN_SIZE) {
          cropW = newW;
        }
        if (newY >= 0 && newH >= MIN_SIZE) {
          cropY = newY;
          cropH = newH;
        }
      } else if (activeHandle === 'se') {
        let newW = startCropW + dx;
        let newH = startCropH + dy;
        
        if (cropX + newW <= canvasWidth && newW >= MIN_SIZE) {
          cropW = newW;
        }
        if (cropY + newH <= canvasHeight && newH >= MIN_SIZE) {
          cropH = newH;
        }
      } else if (activeHandle === 'sw') {
        let newX = startCropX + dx;
        let newW = startCropW - dx;
        let newH = startCropH + dy;
        
        if (newX >= 0 && newW >= MIN_SIZE) {
          cropX = newX;
          cropW = newW;
        }
        if (cropY + newH <= canvasHeight && newH >= MIN_SIZE) {
          cropH = newH;
        }
      }
    }
    
    draw();
  }

  function handleMouseUp() {
    isDraggingBox = false;
    activeHandle = null;
  }

  function saveCrop() {
    if (!imageObj) return;
    
    // Create high-resolution crop canvas
    const destCanvas = document.createElement('canvas');
    
    // Multiply display crop coordinates by scale factor to crop high-res original
    const origX = cropX * scaleFactor;
    const origY = cropY * scaleFactor;
    const origW = cropW * scaleFactor;
    const origH = cropH * scaleFactor;
    
    destCanvas.width = origW;
    destCanvas.height = origH;
    
    const destCtx = destCanvas.getContext('2d');
    destCtx.drawImage(
      imageObj,
      origX, origY, origW, origH, // Source
      0, 0, origW, origH          // Destination
    );
    
    // Export cropped image as Blob
    destCanvas.toBlob((blob) => {
      if (blob) {
        dispatch('cropSave', { blob, fileName });
      }
    }, 'image/jpeg', 0.95);
  }
</script>

<div class="modal-backdrop" on:click={() => dispatch('close')}>
  <div class="modal-content glass animate-fade-in" on:click|stopPropagation>
    <div class="modal-header">
      <h4>Crop Document Note</h4>
      <button class="close-btn" on:click={() => dispatch('close')}>&times;</button>
    </div>
    
    <div class="canvas-container">
      <canvas 
        bind:this={canvas}
        on:mousedown={handleMouseDown}
        on:mousemove={handleMouseMove}
        on:mouseup={handleMouseUp}
        on:mouseleave={handleMouseUp}
      ></canvas>
    </div>
    
    <div class="modal-footer">
      <p class="filename">{fileName}</p>
      <div class="buttons">
        <button class="btn btn-secondary" on:click={() => dispatch('close')}>Cancel</button>
        <button class="btn btn-primary" on:click={saveCrop}>Save Crop</button>
      </div>
    </div>
  </div>
</div>

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(4, 7, 13, 0.85);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }

  .modal-content {
    border-radius: var(--radius-lg);
    width: auto;
    max-width: 90vw;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
    border-bottom: 1px solid var(--border-color);
  }

  h4 {
    font-size: 1.15rem;
    color: var(--text-primary);
  }

  .close-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    font-size: 1.5rem;
    cursor: pointer;
    line-height: 1;
    transition: var(--transition-smooth);
  }

  .close-btn:hover {
    color: var(--text-primary);
  }

  .canvas-container {
    padding: 1.5rem;
    display: flex;
    justify-content: center;
    background: rgba(0, 0, 0, 0.2);
  }

  canvas {
    border-radius: var(--radius-sm);
    cursor: crosshair;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    touch-action: none;
  }

  .modal-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.25rem 1.5rem;
    border-top: 1px solid var(--border-color);
    gap: 2rem;
  }

  .filename {
    color: var(--text-muted);
    font-size: 0.85rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 250px;
  }

  .buttons {
    display: flex;
    gap: 0.75rem;
  }
</style>
