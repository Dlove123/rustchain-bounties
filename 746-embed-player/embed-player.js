/**
 * BoTTube Embeddable Video Player
 * Embed BoTTube videos on any website
 */

class BoTTubePlayer {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.videoId = options.videoId;
    this.width = options.width || 640;
    this.height = options.height || 360;
    this.autoplay = options.autoplay || false;
    this.showControls = options.showControls !== false;
    
    this.init();
  }
  
  init() {
    if (!this.container || !this.videoId) {
      console.error('BoTTubePlayer: container and videoId required');
      return;
    }
    
    this.render();
  }
  
  render() {
    const embedUrl = `https://bottube.com/embed/${this.videoId}?autoplay=${this.autoplay}&controls=${this.showControls}`;
    
    this.container.innerHTML = `
      <div class="bottube-player" style="position: relative; width: ${this.width}px; height: ${this.height}px;">
        <iframe 
          src="${embedUrl}"
          width="${this.width}"
          height="${this.height}"
          frameborder="0"
          allowfullscreen
          allow="autoplay; encrypted-media"
        ></iframe>
      </div>
    `;
  }
  
  play() {
    const iframe = this.container.querySelector('iframe');
    if (iframe) {
      iframe.contentWindow.postMessage(JSON.stringify({action: 'play'}), 'https://bottube.com');
    }
  }
  
  pause() {
    const iframe = this.container.querySelector('iframe');
    if (iframe) {
      iframe.contentWindow.postMessage(JSON.stringify({action: 'pause'}), 'https://bottube.com');
    }
  }
  
  seek(seconds) {
    const iframe = this.container.querySelector('iframe');
    if (iframe) {
      iframe.contentWindow.postMessage(JSON.stringify({action: 'seek', time: seconds}), 'https://bottube.com');
    }
  }
  
  setVolume(volume) {
    const iframe = this.container.querySelector('iframe');
    if (iframe && volume >= 0 && volume <= 100) {
      iframe.contentWindow.postMessage(JSON.stringify({action: 'volume', level: volume}), 'https://bottube.com');
    }
  }
}

// Auto-initialize players
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-bottube-player]').forEach(el => {
    const videoId = el.getAttribute('data-bottube-player');
    const options = {
      width: parseInt(el.getAttribute('data-width') || 640),
      height: parseInt(el.getAttribute('data-height') || 360),
      autoplay: el.getAttribute('data-autoplay') === 'true',
      showControls: el.getAttribute('data-controls') !== 'false'
    };
    new BoTTubePlayer(el.id, {videoId, ...options});
  });
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BoTTubePlayer;
}
