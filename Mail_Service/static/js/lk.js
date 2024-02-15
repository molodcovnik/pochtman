const createAPIKeyBtn = document.querySelector('.api__create-api-key-btn');
const editEmailProfile = document.querySelector('.field_wrapper_profile__img');
const emailInputProfile = document.querySelector('.field_wrapper_profile__input');
const csrfDiv = document.querySelector('.profile-csrf');
let token = csrfDiv.getAttribute("data-csrf");
const userNameDiv = document.querySelector('.navbar__username');
let userId = userNameDiv.getAttribute("data-user-id");

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

editEmailProfile.addEventListener("click", async (e) => {
    emailInputProfile.removeAttribute('readonly');
    document.querySelector('.fields_wrapper_profile').insertAdjacentHTML('beforeend',`<div class="field_wrapper_profile" ><img class="field_wrapper_profile__img field_wrapper_profile__img_save" src="https://static.thenounproject.com/png/2853302-200.png" alt=""></div>`)
    editEmailProfile.style.display = 'none';
    emailInputProfile.focus();
    let email = await fetchUserEmail();
    let email_user = await email.json();
    console.log(email_user.email);
    document.querySelector('.field_wrapper_profile__img_save').addEventListener('click', async (e) => {
        // console.log(emailInputProfile.value);
        await fetchPutUserEmail(emailInputProfile.value);
        document.querySelector('.field_wrapper_profile__img_save').style.display = 'none';
        editEmailProfile.style.display = 'block';
        window.location.reload();
    });
})

async function fetchUserEmail() {
    return await fetch('http://127.0.0.1:8000/api/users_email/', {
        headers: {
            'Content-Type': 'application/json',
            'userId': userId
            }
        })
}

async function fetchPutUserEmail(value) {
    await fetch("http://127.0.0.1:8000/api/users_email/", {
        method: 'PATCH',
        body: JSON.stringify({
            userId: userId,
            email: value
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        }})
        .then((response) => {
            console.log(response);
            return response.json()
        })};