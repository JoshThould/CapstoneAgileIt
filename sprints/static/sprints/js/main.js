document.addEventListener('DOMContentLoaded', function () {
  // 🔴 Title animation
  const itSpan = document.querySelector('.it');
  const text = 'It';
  let index = 0;
  let direction = 1;

  function typeLoop() {
    itSpan.textContent = text.slice(0, index);
    index += direction;

    if (index > text.length) {
      direction = -1;
      setTimeout(typeLoop, 1000);
    } else if (index < 0) {
      direction = 1;
      setTimeout(typeLoop, 500);
    } else {
      setTimeout(typeLoop, 300);
    }
  }

  typeLoop();

  // 🧩 Kanban drag-and-drop
  document.querySelectorAll('.story-card').forEach(card => {
    card.setAttribute('draggable', true);
    card.addEventListener('dragstart', e => {
      e.dataTransfer.setData('storyId', card.dataset.storyId);
    });
  });

  document.querySelectorAll('.story-list').forEach(list => {
    list.addEventListener('dragover', e => {
      e.preventDefault();
    });

    list.addEventListener('drop', e => {
      e.preventDefault();

      const storyId = e.dataTransfer.getData('storyId');
      const newStatus = list.dataset.status;

      const card = document.querySelector(`[data-story-id="${storyId}"]`);
      if (!card) return;

      list.appendChild(card);

      fetch(`/sprints/update-status/${storyId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ status: newStatus }),
      })
      .then(res => res.json())
      .then(data => {
        if (!data.success) {
          alert('Failed to update status');
        }
      });
    });
  });

  function getCSRFToken() {
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
  }
});