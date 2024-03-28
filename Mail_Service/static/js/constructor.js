const baseUrlConst = "http://pochtmen.ru/api";
const createBtn = document.querySelector('.create-form-btn');
const constructorDiv = document.querySelector('.constructor');
const constructorResults = document.querySelector('.constructor-results');
let token = document.querySelector(".constructor__fields-wrapper");
let csrf = token.getAttribute("data-csrf");
const codeBlock = document.querySelector('.code-result');
const jsBlock = document.querySelector('.js-code-content')
const cssDiv = document.querySelector('.css-result');
const htmlDiv = document.querySelector('.html-code-content')
const resWrapper = document.querySelector('.results-wrapper');


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

createBtn.addEventListener('click', (e) => {
    fetchFieldsJSON();
    createBtn.style.display = 'none';
    constructorDiv.classList.add('show');    
});

async function fetchFieldsJSON() {
    const response = await fetch(`${baseUrlConst}/fields/`);

    if (!response.ok) {
        const message = `An error has occured: ${response.status}`;
        throw new Error(message);
      }

    const fields = await response.json();

    fields.forEach(field => {
      const id = field.id;
      const name = field.field_name;
      const type = field.field_type;
      const fieldDiv = `
        <div class="field border" data-id="${id}" data-name="${name}" data-type="${type}">
            <h3 class="field__title margin-top-2rem" data-id="${id}" data-name="${name}" data-type="${type}">${name}</h3>
            <p class="field__desc margin-top-2rem" data-id="${id}" data-name="${name}" data-type="${type}">${type}</p>
            <div class="wrapper-btn center padding-bottom-5rem" data-id="${id}" data-name="${name}" data-type="${type}">
                <button data-id="${id}" data-name="${name}" data-type="${type}" class="btn field__btn margin-top-2rem">+</button>
            </div>
        </div>
      `
      document.querySelector('.fields').insertAdjacentHTML('beforeend', fieldDiv);
    
    })
    
    document.querySelector('.constructor__form-name').insertAdjacentHTML('afterbegin', `<label for="input-name-template" class="" style="display:block;color:#e40d0d;">Сначала введите название формы</label><input id="input-name-template" class="constructor__input-form-name margin-top-2rem border" type="text" placeholder="Название формы"><p style="color:#e40d0d;" class="margin-bottom-3rem margin-top-2rem">Далее выберете необходимые поля</p>`);
    const inputFormName = document.querySelector('.constructor__input-form-name');
    const selectedFields = document.querySelector('.selected-fields');
    inputFormName.addEventListener("change", async (e) => {
        let newFormName = e.target.value;
        let selectedFieldsTitle = `<div class="selected-fields__title"><h3>${newFormName}</h3></div>`;
        let btnSendData = `<div class="wrapper-btn center margin-top-2rem selected-fields__btn-send-data"><button class="btn-not-anim selected-fields__send-data selected-fields__send-data-create-form">Создать</button><div><p style="color:#e40d0d;margin-top: 2rem;">И последнее, сохраните форму!</p></div></div>`;
        selectedFields.insertAdjacentHTML("afterbegin", selectedFieldsTitle);
        selectedFields.insertAdjacentHTML("beforeend", btnSendData);
        let userName = document.querySelector('.navbar__auth-username').textContent;
        let sendData = document.querySelector('.selected-fields__send-data-create-form');
        sendData.addEventListener("click", async () => {
            let fieldsSelected = [].map.call(document.querySelectorAll('.selected-fields__field[data-id]'), function(el) {
                return el.dataset.id;
            })

            let authorUser = document.querySelector(".navbar__username");
            let authorId = authorUser.getAttribute("data-user-id");

            createForm(newFormName, fieldsSelected, authorId, csrf);
            constructorDiv.remove();
            addSectionResults(newFormName);
            constructorResults.classList.add('show');
        });
            
    });
}  


function addSectionResults(formName) {
    const resultsDiv = `<h2 class="constructor-results__title">${formName}</h2>`;
    
    document.querySelector('.constructor-results').insertAdjacentHTML('afterbegin', resultsDiv);
    // document.querySelector('.constructor-results__title').insertAdjacentHTML('afterend', navBlock);
    document.querySelector('.constructor-results').insertAdjacentHTML("beforeend", `<div class="loader-css margin-top-5rem"><span class="loader"></span></div>`);
}

async function createForm(formName, fieldsSelected, userId, token){
    
    try {
        
        const response = await fetch(`${baseUrlConst}/templates/`, {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json',
           'X-CSRFToken': token
           },
           body: JSON.stringify({
     // your expected POST request payload goes here
             name: formName.toLowerCase(),
             fields: fieldsSelected,
             author: userId
            })
         });

         const data = await response.json();
      // enter you logic when the fetch is successful
         console.log(data);
        //  let templateId = data.id;
        //  localStorage.setItem("templateId", templateId);
         let lastTemp =  await getLastTempId(userId);
         let lastTempData =  await lastTemp.json();
         await fetch(`${baseUrlConst}/last_template/`, {
                method: 'POST',
                body: JSON.stringify({
                    templateId: lastTempData.id
                }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf
                },
                
            })
            .then((response) => {
                if (response.status === 200) {
                    document.querySelector('.loader-css').remove();
                    document.querySelector('[data-name="html"]').click()
                } else if (response.status > 400) {
                    document.querySelector('.loader').textContent = 'Internal Server';
                }
                return response.json()
                
            })
            .then(data => {
                let jsCode = data.js_code;
                let code = data.code;

                htmlDiv.insertAdjacentHTML('beforeend', code);
                cssDiv.insertAdjacentHTML('afterbegin', cssCodeGen(lastTempData.name));
                jsBlock.insertAdjacentHTML('beforeend', jsCode);
                resWrapper.insertAdjacentHTML('afterend', `<div class="wrapper-btn center margin-top-3rem margin-bottom-3rem"><button class="navigation__btn" onclick="window.location.pathname = '/templates';">Мои формы</button></div>`);
                
            })
            .catch(error =>  {
            console.log('error', error);
            });
       } catch(error) {
     // enter your logic for when there is an error (ex. error toast)

          console.log(error)
         } 
    }

async function getLastTempId(userId) {
    return await fetch(`${baseUrlConst}/last_template`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authentication': userId,
            }
        });
};

async function insertedResultCode() {

}

const fieldsBlock = document.querySelector('.fields');
fieldsBlock.addEventListener('click', function(e) {
   
    // console.log(e.target.dataset.id);
    const inputFormName = document.querySelector('.constructor__input-form-name');
    inputFormName.setAttribute('readonly', true);
    const fieldId = e.target.getAttribute('data-id');
    const fieldName = e.target.getAttribute('data-name');
    const fieldType = e.target.getAttribute('data-type');
    e.target.closest('.field').remove();
    const btnSendData = document.querySelector('.selected-fields__btn-send-data');
    let selectedField = `<div class="selected-fields__field" data-id="${fieldId}"><h4><span class="selected-fields selected-name">${fieldName}</span> : <span class="selected-fields selected-type">${fieldType}</span></h4></div>`;
    btnSendData.insertAdjacentHTML("beforebegin", selectedField);

});

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

function loaderBlock() {
    const resultsWrapper = document.querySelector('.head__description');
    resultsWrapper.insertAdjacentHTML("afterend", `<p class="loader">Loading</p>`);
    
}

// function goToTemplates() {
//     window.location.pathname = '/templates';
// }