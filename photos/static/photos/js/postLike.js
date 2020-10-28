document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.like').forEach(button => {
    button.onclick = () => {

    const request = new XMLHttpRequest();
    var like_unlike = document.querySelector('.like').value;

    request.open('GET', '/like/' + post_id);

    request.onload = () => {
        var data = request.responseText;
        document.querySelector('#num-likes').innerHTML = data;
        
        if (like_unlike === 'like') {
            document.querySelector('.like').innerHTML = '&#9829;';
            document.querySelector('.like').value = 'unlike';
        }
        if (like_unlike === 'unlike') {
            document.querySelector('.like').innerHTML = '&#9825';
            document.querySelector('.like').value = 'like';
        }
    }

    request.send();
    return false;

    }
    });
});