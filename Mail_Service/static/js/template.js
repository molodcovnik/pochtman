const baseUrlTemp = window.location.protocol + "//" + window.location.host + "/api";
const jsBlock = document.querySelector('.js-code-content');
const cssDiv = document.querySelector('.css-result');
const htmlDiv = document.querySelector('.html-code-content');
const tempName = document.querySelector('#temp-card__template-name').textContent;
const currentTempId = document.querySelector('.temp-card').getAttribute('data-temp-id');

let template = document.querySelector('.temp-card');
let tempId = template.getAttribute('data-temp-id');
const message = document.querySelector(".messages__success_updated");

// getCheckTgUserDB(tempId);

// запрос на новые уведомления

let timerId = setTimeout(function checkingTgUser() {
    getCheckTgUserDB(tempId);
    timerId = setTimeout(checkingTgUser, 10000);
}, 1500);

if (message) {
    message.classList.add('hidden-animate');
}



loadTempCode(currentTempId);
addNotification(tempId);

function cssCodeGen(tempName) {
    var name = tempName.replace(/ /g, "_");
    const blockCss = `
<code class="css-code">
<span class="keyword">.${name.toLowerCase()}</span> {<span class="rules">
    <span class="rule"><span class="rule__keyword">width:</span><span class="value">500px;</span></span>
    <span class="rule"><span class="rule__keyword">height:</span><span class="value">auto;</span></span>
    <span class="rule"><span class="rule__keyword">border:</span><span class="value">1px solid #80a9ec;</span></span>
    <span class="rule"><span class="rule__keyword">border-radius:</span><span class="value">8px;</span></span>
}
</span>
<span class="keyword">.form</span> {<span class="rules">
    <span class="rule"><span class="rule__keyword">width:</span><span class="value">80%;</span></span>
    <span class="rule"><span class="rule__keyword">height:</span><span class="value">inherit;</span></span>
    <span class="rule"><span class="rule__keyword">margin:</span><span class="value">0 auto;</span></span>
}
</span>
<span class="keyword">.form__label</span> {<span class="rules">
    <span class="rule"><span class="rule__keyword">display:</span><span class="value">block;</span></span>
    <span class="rule"><span class="rule__keyword">text-align:</span><span class="value">center;</span></span>
    <span class="rule"><span class="rule__keyword">font-size:</span><span class="value">20px;</span></span>
    <span class="rule"><span class="rule__keyword">margin-top:</span><span class="value">30px;</span></span>
    <span class="rule"><span class="rule__keyword">font-weight:</span><span class="value">bold;</span></span>
}
</span>
<span class="keyword">.form__input</span> {<span class="rules">
    <span class="rule"><span class="rule__keyword">height:</span><span class="value">35px;</span></span>
    <span class="rule"><span class="rule__keyword">width:</span><span class="value">250px;</span></span>
    <span class="rule"><span class="rule__keyword">border:</span><span class="value">2px solid #1C58F0;</span></span>
    <span class="rule"><span class="rule__keyword">border-radius:</span><span class="value">7px;</span></span>
    <span class="rule"><span class="rule__keyword">padding-left:</span><span class="value">10px;</span></span>
    <span class="rule"><span class="rule__keyword">font-size:</span><span class="value">18px;</span></span>
    <span class="rule"><span class="rule__keyword">margin-top:</span><span class="value">30px;</span></span>
}
</span>
<span class="keyword">.field-wrapper</span> {<span class="rules">
    <span class="rule"><span class="rule__keyword">width:</span><span class="value">100%;</span></span>
    <span class="rule"><span class="rule__keyword">text-align:</span><span class="value">center;</span></span>
}
</span>
<span class="keyword">.send-btn</span> {<span class="rules">
    <span class="rule"><span class="rule__keyword">margin-top:</span><span class="value">50px;</span></span>
    <span class="rule"><span class="rule__keyword">display:</span><span class="value">block;</span></span>
    <span class="rule"><span class="rule__keyword">text-align:</span><span class="value">center;</span></span>
}
</span>
<span class="keyword">.btn</span> {<span class="rules">
    <span class="rule"><span class="rule__keyword">padding:</span><span class="value">10px 30px;</span></span>
    <span class="rule"><span class="rule__keyword">outline:</span><span class="value">none;</span></span>
    <span class="rule"><span class="rule__keyword">border:</span><span class="value">2px solid #1C58F0;</span></span>
    <span class="rule"><span class="rule__keyword">border-radius:</span><span class="value">7px;</span></span>
    <span class="rule"><span class="rule__keyword">background:</span><span class="value">#fff;</span></span>
    <span class="rule"><span class="rule__keyword">cursor:</span><span class="value">pointer;</span></span>
}
</span>
<span class="keyword">.btn:hover</span> {<span class="rules">
    <span class="rule"><span class="rule__keyword">background:</span><span class="value">#e0dede;</span></span>
}
</span>
</code>`;
    return blockCss;
}



async function loadTempCode(currentTempId) {
    loaderBlockTemplate();
    await fetch(`${baseUrlTemp}/last_template/`, {
        method: 'POST',
        body: JSON.stringify({
            templateId: currentTempId
        }),
        headers: {
            'Content-Type': 'application/json',
            'Authorization' : `Token ${localStorage.getItem("token")}`
        },
    })
    .then((response) => {
        if (response.status === 200) {
            document.querySelector('.loader-css').remove();
        } else if (response.status > 400) {
            console.log('error');
        }
        return response.json()
        
    })
    .then(data => {
        let jsCode = data.js_code;
        let code = data.code;

        htmlDiv.insertAdjacentHTML('beforeend', code);
        cssDiv.insertAdjacentHTML('afterbegin', cssCodeGen(tempName));
        jsBlock.insertAdjacentHTML('beforeend', jsCode);
        
    })
    .catch(error =>  {
    console.log('error', error);
    });
}

document.querySelector('.navigation__menu').addEventListener('click', (e) => {
    let currentTarget = e.target.getAttribute('data-name');
    if (currentTarget === 'html') {
        document.querySelector('.html-code-content').classList.toggle('hidden');
        document.querySelector('.css-code-content').classList.add('hidden');
        document.querySelector('.js-code-content').classList.add('hidden');
    } else if (currentTarget === 'css') {
        document.querySelector('.css-code-content').classList.toggle('hidden');
        document.querySelector('.html-code-content').classList.add('hidden');
        document.querySelector('.js-code-content').classList.add('hidden');
    } else if (currentTarget === 'js') {
        document.querySelector('.js-code-content').classList.toggle('hidden');
        document.querySelector('.css-code-content').classList.add('hidden');
        document.querySelector('.html-code-content').classList.add('hidden');
    }
});

function loaderBlockTemplate() {
    const resultsWrapper = document.querySelector('.temp-detail-right');
    resultsWrapper.insertAdjacentHTML("beforeend", `<div class="loader-css margin-top-10rem"><p class="loader"></p></div>`);
    
}


async function getNotifications(tempId) {
    return await fetch(`${baseUrlTemp}/notifications/${tempId}/count`, {
      method: 'GET',
      headers: {
          'Content-Type': 'application/json',
          }
      });
};

async function addNotification(tempId) {
    let tempFetch = await getNotifications(tempId);
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
}
const getSaveBtn = (name) => {
    let saveBtnHTML = `<div class="contact-form__action" ><img class="contact-form__action-save contact-form__action-save_${name}" src="https://static.thenounproject.com/png/2853302-200.png" alt=""></div>`;
    return saveBtnHTML;
}

const getInputForm = (name) => { 
    // let placeholderTg = `placeholder="@user_123"`;
    // let placeholderEmail = ;
    let placeholder = name === "telegram" ? `placeholder="@user_123"` : `placeholder="example@mail.ru"`

    let inputFormHTML = `<div class="form-edit-temp-contact">
    <form action="" method="post" id="edit-${name}-contact">
        <label for="user-${name}"></label>
        <input type="text" name="user-${name}" id="user-${name}" ${placeholder}>
    </form>
    </div>`;
    return inputFormHTML;
}

function editBtnClicked(service_name) {
    let card = document.querySelector(`.contact-form__${service_name}`);
    
    console.log(service_name);
    document.querySelector(`.contact-form__action-edit_${service_name}`).style.display = 'none';
    let saveBtn = getSaveBtn(service_name);
    let formInputContact = getInputForm(service_name);
    let contactData = document.querySelector(`.contact-form__current-contact_${service_name}`);
    document.querySelector(`.contact-form__action_${service_name}`).insertAdjacentHTML('beforeend', saveBtn);
    contactData.remove();
    document.querySelector(`.contact-form__contact_${service_name}`).insertAdjacentHTML("afterbegin", formInputContact);
    let cardInput = card.querySelector(`#user-${service_name}`);
    cardInput.focus();
    
    card.querySelector(`.contact-form__action-save_${service_name}`).addEventListener("click", async (e) => {
        try {
            await fetchUpdateAuthorContacts(cardInput.value, service_name);
            window.location.reload();
        } catch (e) {
            document.querySelector('.main-container').insertAdjacentHTML("afterbegin", `<ul class="messages"><li class="messages__error error">Ошибка валидации. Поле не может быть пустым или более 64 символов.</li></ul>`);
            cardInput.setAttribute('readonly', 'true');
            document.querySelector('.messages__error').addEventListener('click', () => {
                document.querySelector('.messages').remove();
                cardInput.removeAttribute('readonly');
                cardInput.focus();
            })
        }

    })

}

document.querySelector('.contact-form__action-edit_email').addEventListener('click', (e) => {
    editBtnClicked(e.target.dataset.name);
})


document.querySelector('.contact-form__action-edit_telegram').addEventListener('click', (e) => {
    editBtnClicked(e.target.dataset.name);
})

async function fetchUpdateAuthorContacts(value, service_name) {
    let data_tg = {
        telegram_author: value
    }

    let data_email = {
        email_author: value
    }

    let response = await fetch(`${baseUrlTemp}/templates/${currentTempId}/${service_name}/`, {
        method: 'PATCH',
        body: JSON.stringify(service_name === 'telegram' ? data_tg : data_email),
        headers: {
            'Content-Type': 'application/json',
            'Authorization' : `Token ${localStorage.getItem("token")}`
        }})

        if (response.status == 202) {
            let json = await response.json();
            return json;
          }
        
        throw new Error(response.ErrorMessage);
};


async function getCheckTgUserDB(tempId) {
    const checkTg = document.querySelector('.contact-form__check-telegram');
    let tg_response = await fetch(`${baseUrlTemp}/templates/${tempId}/telegram/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization' : `Token ${localStorage.getItem("token")}`
            }
    });
    let tg_result = await tg_response.json();
    if (!tg_result.telegram_author) {
        checkTg.remove();
    } else {
        let response = await fetch(`${baseUrlTemp}/templates/${tempId}/check_telegram/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                }
            });
        let result = await response.json();
        let isTgUser = result.tg_user;
        
        if (isTgUser) {
            checkTg.style.color = '#67e712';
            checkTg.style.opacity = '1';
        } else {
            checkTg.style.color = '#e16c6c';
            checkTg.style.opacity = '1';
        }
        }
};