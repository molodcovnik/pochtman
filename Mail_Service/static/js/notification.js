const fieldCard = document.querySelector('.field-card');
const uid = fieldCard.getAttribute('data-uid');
const csrf = fieldCard.getAttribute('data-csrf');
const pk = fieldCard.getAttribute('data-id');

const form = document.querySelector('.form-delete-temp-data');

form.onsubmit = async (e) => {
    e.preventDefault();
    const data = {
        "uid": uid,
    };
    let response = await fetch('http://127.0.0.1:8000/api/notifications/delete', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        body: JSON.stringify(data),
      });
    let result = await response.text();
    window.location.pathname = '/templates/' + pk + '/notifications/';
};