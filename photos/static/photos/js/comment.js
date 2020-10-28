document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('.add-comment').disabled = true;

    document.querySelector('#input-comment').onkeyup = () => {
        if (document.querySelector('#input-comment').value.length > 0)
            document.querySelector('.add-comment').disabled = false;
        else
            document.querySelector('.add-comment').disabled = true;
    };

    
    document.querySelectorAll('.add-comment').forEach(button => {
    button.onclick = () => {
        var get_comment = document.querySelector('#input-comment').value;
        $.ajax({

            type:"POST",
            url: "/comment/" + post_id,
            data: {
                csrfmiddlewaretoken: csrf,
                'u_comment': get_comment,
            },
            success: (data) => {                    
                add_comment = JSON.stringify(data[0].comment);
                username = JSON.stringify(data[0].name);
                date = JSON.stringify(data[0].date);
                time = JSON.stringify(data[0].time);

                const p = document.createElement('p');
                p.setAttribute('class', 'box');
                const line_break = document.createElement('br');
                const username_span = document.createElement('span');
                const time_span = document.createElement('span');
                const date_span = document.createElement('span');
                time_span.setAttribute('class', 'time');
                username_span.setAttribute('class', 'username');
                time_span.setAttribute('class', 'date-time');
                date_span.setAttribute('class', 'date-time')
                username_span.innerHTML = JSON.parse(username);
                time_span.innerHTML = JSON.parse(time);
                date_span.innerHTML = JSON.parse(date);
                p.innerHTML = username_span.outerHTML + JSON.parse(add_comment) + date_span.outerHTML + time_span.outerHTML;

                document.querySelector('#comments').append(p);
                document.querySelector('#input-comment').value = "";
                scrollDown();  
            },
        });
    };
    });
    function scrollDown(){
        window.scrollTo(0,document.body.scrollHeight);
    }
});