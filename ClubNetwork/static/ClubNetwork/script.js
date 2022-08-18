document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll(".like").forEach(likeButton =>{
        const post_id = likeButton.dataset.postid;

        likeButton.onclick = () =>{
            let like_count = likeButton.lastChild.innerHTML
            if (likeButton.style.color === "red"){
                likeButton.style.color = "black";
                like_count--;
                likeButton.lastChild.innerHTML = like_count;
                fetch(`/posts/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        liked: false
                    })
                  });
            }else{
                likeButton.style.color = "red";
                like_count++;
                likeButton.lastChild.innerHTML = like_count;
                fetch(`/posts/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        liked: true
                    })
                  });
            }
            
        };
    });
});