const jsBlock = document.querySelector('.js-code-content');
const cssDiv = document.querySelector('.css-result');
const htmlDiv = document.querySelector('.html-code-content');
const tempName = document.querySelector('.temp-card__header').textContent;
const currentTempId = document.querySelector('.temp-card').getAttribute('data-temp-id');
let token = document.querySelector(".temp-detail-left");
let csrf = token.getAttribute("data-csrf");

loadTempCode(currentTempId);

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
    await fetch("http://127.0.0.1:8000/api/last_template/", {
        method: 'POST',
        body: JSON.stringify({
            templateId: currentTempId
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
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
