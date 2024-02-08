const tempIds = document.querySelectorAll('div[data-tempid]');

let templatesAll = [].map.call(tempIds, async function(el) {
    let tempFetch = await getNotifications(el.dataset.tempid);
    let tempFetchData = await tempFetch.json();
    let templateId = tempFetchData.id;
    let templateCount = tempFetchData.count;

    let template = document.getElementById(`${templateId}`);
    let tempNotification = template.querySelector('.temp-card__notification');
    if (templateCount > 0) {
        tempNotification.style.display = 'block';
    } else {
        tempNotification.style.display = 'none';
    }
})


async function getNotifications(tempId) {
    return await fetch(`http://127.0.0.1:8000/api/notifications/${tempId}/count`, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
          }
      });
};