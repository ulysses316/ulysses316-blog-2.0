post = document.querySelector("#post");
if (window.screen.width <= 600){
    post.classList.add('uk-container');
}
else{
    post.classList.add('container-post');
}