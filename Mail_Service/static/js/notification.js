const baseUrlNotification = window.location.protocol + "//" + window.location.host + "/api";
const fieldCard = document.querySelector('.field-card');
const uid = fieldCard.getAttribute('data-uid');
const pk = fieldCard.getAttribute('data-id');
const form = document.querySelector('.form-delete-temp-data');



changeStatus(uid);

form.onsubmit = async (e) => {
    e.preventDefault();
    const data = {
        "uid": uid,
    };
    let response = await fetch(`${baseUrlNotification}/notifications/delete`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization' : `Token ${localStorage.getItem("token")}`
        },
        body: JSON.stringify(data),
      });
    let result = await response.text();
    window.location.pathname = '/templates/' + pk + '/notifications/';
};

async function changeStatus(uid) {
    const data = {
        "uid": uid,
    };
    let response = await fetch(`${baseUrlNotification}/notifications/status`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization' : `Token ${localStorage.getItem("token")}`
        },
        body: JSON.stringify(data),
      });
    let result = await response.text();
    console.log(result.status);

}


const dropDownBtn = document.querySelector('.dropdown-btn');
const dropDownMenu = document.querySelector('.dropdown-status__menu');
const dropItems = document.querySelectorAll('.dropdown-status__item');
const selectedItem = document.querySelector('.dropdown-btn__active');

window.addEventListener('click', function() {
    closeMenu();
});

dropDownBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleMenu();
});

dropItems.forEach(item => item.addEventListener('click', itemClickHandler));

function toggleMenu() {
    dropDownMenu.classList.toggle('dropdown-status__menu_open');
}

function closeMenu() {
    dropDownMenu.classList.remove('dropdown-status__menu_open');
}

function itemClickHandler(e) {
    e.stopPropagation();
    selectedItem.innerText = e.target.innerText;
    // dropItems.forEach(item => item.classList.remove('dropdown-status__item_active'));
    // e.target.classList.add('dropdown-status__item_active');
    // добавить функцию на пут запрос по юид на смену статуса
    closeMenu();
}
