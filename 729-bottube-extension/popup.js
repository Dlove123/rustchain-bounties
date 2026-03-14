// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.tab).classList.add('active');
  });
});

// Search videos
async function searchVideos() {
  const query = document.getElementById('searchInput').value;
  const videoList = document.getElementById('videoList');
  videoList.innerHTML = '<p>Loading...</p>';
  
  try {
    const response = await fetch(`https://api.bottube.com/search?q=${encodeURIComponent(query)}`);
    const data = await response.json();
    
    videoList.innerHTML = '';
    if (data.results && data.results.length > 0) {
      data.results.forEach(video => {
        videoList.innerHTML += `
          <div class="video-item">
            <div class="video-title">${video.title}</div>
            <div class="video-votes">👍 ${video.votes || 0}</div>
          </div>
        `;
      });
    } else {
      videoList.innerHTML = '<p>No results found</p>';
    }
  } catch (error) {
    videoList.innerHTML = '<p>Error loading videos</p>';
  }
}

// Upload video
async function uploadVideo() {
  const title = document.getElementById('videoTitle').value;
  const description = document.getElementById('videoDesc').value;
  const videoUrl = document.getElementById('videoUrl').value;
  
  if (!title || !videoUrl) {
    alert('Please fill in title and video URL');
    return;
  }
  
  try {
    const response = await fetch('https://api.bottube.com/videos/upload', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, video_url: videoUrl })
    });
    const data = await response.json();
    alert(data.message || 'Upload successful!');
  } catch (error) {
    alert('Upload failed: ' + error.message);
  }
}

// Load user profile
async function loadProfile() {
  const userInfo = document.getElementById('userInfo');
  try {
    const response = await fetch('https://api.bottube.com/user/profile');
    const data = await response.json();
    userInfo.innerHTML = `
      <p><strong>Username:</strong> ${data.username || 'Guest'}</p>
      <p><strong>Videos:</strong> ${data.video_count || 0}</p>
      <p><strong>Total Votes:</strong> ${data.total_votes || 0}</p>
    `;
  } catch (error) {
    userInfo.innerHTML = '<p>Not logged in</p>';
  }
}

loadProfile();
