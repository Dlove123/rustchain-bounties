// Keyboard Shortcuts - #2140 (5 RTC)
document.addEventListener('keydown', (e) => {
  if (e.key === ' ') { e.preventDefault(); togglePlay(); }
  if (e.key === 'f') toggleFullscreen();
  if (e.key === 'm') toggleMute();
  if (e.key === 'ArrowLeft') seek(-10);
  if (e.key === 'ArrowRight') seek(10);
});
