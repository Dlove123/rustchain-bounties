# BoTTube Integration Guide

Complete guide for integrating BoTTube into your application.

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Code Examples](#code-examples)
5. [Best Practices](#best-practices)

---

## Overview

BoTTube is a decentralized video platform built on RustChain. This guide covers:

- Video upload
- Video playback
- Voting system
- User profiles
- Embedding

---

## Authentication

### API Key

```python
import requests

API_KEY = "your_api_key"
BASE_URL = "https://api.bottube.com"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
```

---

## API Endpoints

### 1. Upload Video

```python
def upload_video(title, description, video_url):
    response = requests.post(
        f"{BASE_URL}/videos/upload",
        headers=headers,
        json={
            "title": title,
            "description": description,
            "video_url": video_url
        }
    )
    return response.json()
```

### 2. Search Videos

```python
def search_videos(query, limit=10):
    response = requests.get(
        f"{BASE_URL}/search",
        params={"q": query, "limit": limit}
    )
    return response.json()
```

### 3. Vote on Video

```python
def vote_video(video_id, vote_type):
    response = requests.post(
        f"{BASE_URL}/videos/{video_id}/vote",
        json={"type": vote_type}  # "upvote" or "downvote"
    )
    return response.json()
```

### 4. Get User Profile

```python
def get_user_profile(username):
    response = requests.get(f"{BASE_URL}/users/{username}")
    return response.json()
```

---

## Code Examples

### JavaScript/Node.js

```javascript
const BoTTubeAPI = require('bottube-sdk');

const api = new BoTTubeAPI({
  apiKey: 'your_api_key'
});

// Upload video
const video = await api.uploadVideo({
  title: 'My Video',
  description: 'Video description',
  videoUrl: 'https://example.com/video.mp4'
});

// Search videos
const results = await api.search('tutorial');

// Vote
await api.vote(videoId, 'upvote');
```

### React Component

```jsx
import { BoTTubePlayer } from 'bottube-player';

function VideoPlayer({ videoId }) {
  return (
    <BoTTubePlayer
      videoId={videoId}
      width={640}
      height={360}
      autoplay={false}
    />
  );
}
```

---

## Best Practices

1. **Rate Limiting**: Respect API rate limits (100 requests/minute)
2. **Error Handling**: Always handle API errors gracefully
3. **Caching**: Cache video metadata to reduce API calls
4. **Security**: Never expose API keys in client-side code
5. **Attribution**: Credit BoTTube when embedding videos

---

## Resources

- [API Documentation](https://docs.bottube.com)
- [GitHub Repository](https://github.com/bottube)
- [Discord Community](https://discord.gg/bottube)

---

*Happy Integrating!* 🎬
