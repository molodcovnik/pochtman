const createAPIKeyBtn = document.querySelector('.api__create-api-key-btn');
const hiddenBtn = document.querySelector('.hidden-api-key');
const csrfDiv = document.querySelector('.profile-csrf');
let token = csrfDiv.getAttribute("data-csrf");
const userNameDiv = document.querySelector('.navbar__username');
let userId = userNameDiv.getAttribute("data-user-id");

createAPIKeyBtn.addEventListener('click', () => {
    fetchTokenJSON();
    createAPIKeyBtn.style.display = 'none';
    hiddenBtn.style.display = 'block';
});

hiddenBtn.addEventListener('click', () => {
    document.querySelector('.api-code').remove();
    hiddenBtn.style.display = 'none';
    createAPIKeyBtn.style.display = 'block';
});

function insertAPIKey(data, status) {
    let createdApiKey = 
`<pre class="api-code"><code>
HTTP 201 Created
Content-Type: application/json
Vary: Accept
{
    <span class="json-api-red">"token"</span>: <span class="json-api-red">"${data.key}"</span>,
    <span class="json-api-red">"created"</span>: <span class="json-api-red">"${data.created}"</span>
}</code></pre>`;
    let gettedAPIKey = 
`<pre class="api-code"><code>
HTTP 200 OK
Content-Type: application/json
Vary: Accept
{
    <span class="json-api-red">"token"</span>: <span class="json-api-red">"${data.key}"</span>,
    <span class="json-api-red">"created"</span>: <span class="json-api-red">"${data.created}"</span>
}</code></pre>`;

    if (status === 200) {
        document.querySelector('.api').insertAdjacentHTML('beforeend', gettedAPIKey);
    } else if ( status === 201 ) {
        document.querySelector('.api').insertAdjacentHTML('beforeend', createdApiKey);
    } else {
        document.querySelector('.api').insertAdjacentHTML('beforeend', `<div class="api__error">Error</div>`);
    }
}

async function fetchTokenJSON() {
    const response = await fetch('http://127.0.0.1:8000/api/token/');

    if (!response.ok) {
        const message = `An error has occured: ${response.status}`;
        throw new Error(message);
      }
    const data = await response.json();
    insertAPIKey(data, response.status);
    // console.log(data);

}

function hiddenApiBtn() {
    document.querySelector('.api-code').style.display = 'none';
}