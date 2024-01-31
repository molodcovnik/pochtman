const createAPIKeyBtn = document.querySelector('.api__create-api-key-btn');
createAPIKeyBtn.addEventListener('click', () => {
    fetchTokenJSON();
    
});

function insertAPIKey(data, status) {
    let createdApiKey = 
`<pre><code>
HTTP 201 Created
Content-Type: application/json
Vary: Accept
{
    <span class="json-api-red">"token"</span>: <span class="json-api-red">"${data.key}"</span>,
    <span class="json-api-red">"created"</span>: <span class="json-api-red">"${data.created}"</span>
}</code></pre>`;
    let gettedAPIKey = 
`<pre><code>
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