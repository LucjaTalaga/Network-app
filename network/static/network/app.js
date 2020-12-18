document.addEventListener('DOMContentLoaded', function() {
    
    const newPost = document.querySelector('#new-post');
    if (newPost){
      newPost.addEventListener('submit', addNewPost);
    }
    const likeButtons = document.querySelectorAll('.toggle-like');
    likeButtons.forEach(button => {
      button.addEventListener('submit', likeButtonHandler);
    });
    const follow = document.querySelector('#follow');
    if (follow){ 
    follow.addEventListener('submit', followHandler);
    }
    const edit = document.querySelectorAll('.edit');
    if (edit){
      edit.forEach(button => {
        button.addEventListener('submit', editButtonHandler);
      });
    }
});

function addNewPost(event){
    event.preventDefault();
    const csrf = event.target[0].value;
    const postedText = event.target[1].value;
    fetch('/add', {
        method: 'POST',
        headers: { 
            'X-CSRFToken': csrf
        },
        body: JSON.stringify({
            text: postedText
        })
      }).then(resp => {
        if (resp.ok)
          return resp.json();
        else
          throw new Error('Network error');
        }).then(resp => {
            console.log(resp.message);
            displayPost(resp.author, postedText, resp.id, csrf);
        }).catch(err => {
            console.log('Error ', err);
        });
}

function likeButtonHandler(event){
  event.preventDefault();
  const csrf = event.target[0].value;
  const button = event.target[1];
  const method = button.dataset.method;
  const id = button.dataset.id;
  fetch('/like', {
    method: method,
    headers: { 
      'X-CSRFToken': csrf
    },
    body: JSON.stringify({
        id: id
    })
  }).then(resp => {
    if (resp.ok)
      return resp.json();
    else
      throw new Error('Network error');
    }).then(resp => {
        button.dataset.method = resp.method == 'POST' ? 'DELETE' : 'POST';
        button.innerText = resp.method == 'POST' ? 'Dislike' : 'Like';
        let likes = parseInt(event.target.previousElementSibling.innerText);
        const toAdd = resp.method == 'POST' ? 1 : -1;
        likes += toAdd;
        event.target.previousElementSibling.innerText = likes.toString() + " likes";
        
    }).catch(err => {
        console.log('Error ', err);
    });
}

function displayPost(author, text, id, csrf){
  const container = document.querySelector('.posts');
  const newPost = document.createElement('div');
  newPost.classList.add('post-container');
  newPost.innerHTML = `<h4>${author}</h4>
    <p>${text}</p>
    <p>0 likes</p>
    <form class="toggle-like">
    <input type="hidden" name="csrfmiddlewaretoken" value=${csrf}>
      <button class="btn btn-primary" data-method="POST" data-id=${id}>Like</button>
    </form>`;
  newPost.querySelector('.toggle-like').addEventListener('submit', likeButtonHandler);
  container.prepend(newPost);
}

function followHandler(event) {
  event.preventDefault();
  const csrf = event.target[0].value;
  const button = event.target[1];
  const method = button.dataset.method;
  const id = button.dataset.id;
  fetch('/follow', {
    method: method,
    headers: { 
      'X-CSRFToken': csrf
    },
    body: JSON.stringify({
        id: id
    })
  }).then(resp => {
    if (resp.ok)
      return resp.json();
    else
      throw new Error('Network error');
    }).then(resp => {
      button.dataset.method = resp.method == 'POST' ? 'DELETE' : 'POST';
      button.innerText = resp.method == 'POST' ? 'Unfollow' : 'Follow';     
      const toAdd = resp.method == 'POST' ? 1 : -1;
      const textField = event.target.previousElementSibling.previousElementSibling.previousElementSibling;
      const text = textField.innerText;
      const followers = parseInt(text);
      console.log(text);
      console.log(followers);
      const followersUpdated = followers + toAdd;
      textField.innerHTML = text.replace(followers, followersUpdated);  
    }).catch(err => {
      console.log('Error ', err);
  });
}

function editButtonHandler(event) {
  event.preventDefault();
  console.log(event.target);
  const csrf = event.target[0].value;
  const button = event.target[1];
  const textField = event.target.previousElementSibling.previousElementSibling.previousElementSibling;
  const buttonFunction = button.innerText;
  if (buttonFunction === "Edit"){
    const text = textField.innerText;
    textField.innerHTML = `<textarea>${text}</textarea>`;
    button.innerText = 'Save';  
  }
  else {
    const text = textField.firstElementChild.value;
    button.innerText = 'Edit';
    const id = button.dataset.id;
    saveEditedField(id, csrf, text);
    textField.innerHTML = text;
  }
}

function saveEditedField(id, csrf, text){
  
  fetch('/edit', {
    method: 'PUT',
    headers: { 
      'X-CSRFToken': csrf
    },
    body: JSON.stringify({
      id: id,  
      text: text
    })
  }).then(resp => {
    if (resp.ok)
      return resp.json();
    else
      return resp.json();
    }).then(resp => {
        if (resp.error)
          throw new Error(resp.error);
        else
          console.log(resp.message);
    }).catch(err => {
        alert(err);
        console.log('Error ', err);
        return false;
    });
}