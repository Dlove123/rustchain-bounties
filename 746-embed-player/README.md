# BoTTube Embeddable Video Player

Embed BoTTube videos on any website with customizable controls.

## Features

- Customizable dimensions
- Autoplay support
- Show/hide controls
- Programmatic controls (play, pause, seek, volume)
- Responsive design

## Installation

```html
<script src="embed-player.js"></script>
```

## Usage

### JavaScript API

```javascript
const player = new BoTTubePlayer('player', {
  videoId: 'VIDEO_ID',
  width: 640,
  height: 360,
  autoplay: false
});

// Controls
player.play();
player.pause();
player.seek(30);
player.setVolume(80);
```

### HTML Embed

```html
<div id="player" 
     data-bottube-player="VIDEO_ID"
     data-width="640"
     data-height="360"
     data-autoplay="false">
</div>
<script src="embed-player.js"></script>
```

## Files

- embed-player.js - Player library
- index.html - Demo page
- README.md - Documentation

---

Fixes #746
