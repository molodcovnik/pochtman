const baseUrlNotifications = window.location.protocol + "//" + window.location.host + "/api";
const domain = window.location.protocol + "//" + window.location.host;
let gridCells = document.getElementById('table-results');
let url = window.location.pathname;
let url_array = url.split('/') // Split the string into an array with / as separator
let pk_temp = url_array[url_array.length-3];


gridCells.addEventListener('dblclick', (e) => {
    // let parent = e.target.parentNode;

    let uid = e.target.parentNode.getAttribute('data-uid');
    
    if (uid) {
        console.log(uid);
        window.location.pathname = window.location.pathname + uid + '/';
    }
    // console.log(window.location.pathname);
    });

   
function onlyUnique(value, index, array) {
    return array.indexOf(value) === index;
}
document.addEventListener("DOMContentLoaded", async () => {
    let arr = [];
    let fieldsArr = ["Время", ];
    let notifications = await getNotification(pk_temp);
    let data = await notifications.json();
    let fields = await getFieldsName(pk_temp);
    let fieldsData = await fields.json();
    fieldsData.fields.map(item => fieldsArr.push(item.field_name));
    fieldsArr.push("Действия");
    data.map(item => arr.push(item.uid));
    let uniqUids = arr.filter(onlyUnique);
    
    document.getElementById('table-results').insertAdjacentHTML("afterbegin",
        `<tr class="table-row__head">
            ${fieldsArr.map(item => `<th>${item}</th>`).join("")}
        </tr>`
    );

    document.querySelector('.table-row__head').insertAdjacentHTML("beforeend", `<th class="col1"><input type="checkbox" class="main-check"></th>`);
    let arrData = [];
    uniqUids.map(item => {
        let match = data.filter(dataItem => dataItem.uid === item)

        arrData.push(match);
    });

    document.querySelector('.main-check').addEventListener('change', (e) => {
        let checked =  e.target.checked;
        let allChecks = document.querySelectorAll('.check');
        if (checked) {
            allChecks.forEach(checkedCheck => {
                checkedCheck.checked = true;
            });
        } else {
            allChecks.forEach(checkedCheck => {
                checkedCheck.checked = false;
            });
        }
    });
        

    arrData.forEach(field => {
        let dataItem = field.map(dataItem => dataItem.data);
        let timeItem = field.map(dataItem => dataItem.time_add);
        let readStatus = field.map(dataItem => dataItem.read_status);
        let uid = field.map(dataItem => dataItem.uid);
        let timeCreated = timeItem.filter(onlyUnique);
        let date = new Date(timeCreated);
        let day = ('0' + date.getDate()).slice(-2);
        let month = ('0' + (date.getMonth() + 1)).slice(-2);
        let year = date.getFullYear();
        let hour = ('0' + date.getHours()).slice(-2);
        let minutes = ('0' + date.getMinutes()).slice(-2);
        let seconds = ('0' + date.getSeconds()).slice(-2);
        let formattedDate = day + "." + month + "." + year + " " + hour + ":" + minutes + ":" + seconds;

        // ADD DATA_UID TO !!!
        document.getElementById('table-results').insertAdjacentHTML("beforeend", 
        `
        <tr class="${readStatus[0] ? "table-row readed" : "table-row unreaded"}" data-uid="${uid[0]}">
            <td class="table-cell__time">${formattedDate}</td>
            ${dataItem.map(item => `<td class="table-cell__data">${item === 'True' ? 'Да' : item === 'False' ? 'Нет' : item}</td>`).join("")}
            <td class="td-buttons"><a onclick="window.location.pathname = window.location.pathname + ${uid[0]} + '/';"><img class="action-notification action-notification__view-notification" src="${domain}/static/images/detail.png" alt="Читать"></a><a onclick="deleteNotification(${uid[0]});"><img class="action-notification action-notification__remove-notification" src="${domain}/static/images/remove.png" alt="Удалить?"></a></td>
            <td class="col1"><input type="checkbox" class="check"></td>
        </tr>
        `
        );
    });

    });

async function getNotification(pk) {
    return await fetch(`${baseUrlNotifications}/notifications/${pk}/`);
    }

async function getFieldsName(pk) {
    return await fetch(`${baseUrlNotifications}/templates/${pk}/fields/`);
    }

document.querySelector('.view-checks').addEventListener('click', (e) => {
    let selectedChecks = document.querySelectorAll('.check:checked');
    selectedChecks.forEach(item => {
        console.log(item.parentNode.parentNode.getAttribute('data-uid'));
    });
});

async function deleteNotification(uid) {

    const data = {
        "uid": uid,
    };
    let response = await fetch(`${baseUrlNotifications}/notifications/delete`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization' : `Token ${localStorage.getItem("token")}`
            },
            body: JSON.stringify(data),
        });
    let result = await response.text();
    window.location.pathname = '/templates/' + pk_temp + '/notifications/';
}