document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#profile').onchange = () => {
        document.querySelector('#form').submit();
    }

});