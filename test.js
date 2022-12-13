console.log('start');

//Startscreen
async function startscreen() {
    try {
        const response = await fetch('http://127.0.0.1:5000/startgame');
        console.log(response);
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            return data;
        } else {
            const answer = 'No voi paska, ei toimi' + response.error;
            return answer
        }
    } catch (error) {
        console.log('error');
        return error
    }
}

// get_value from input

function getInputValue() {
    const input_field = document.querySelector(`input`);
    const value = input_field.value;
    return value

}

//get_name
async function getName(input) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/screen_name?name=${input}`);
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            return data;
        }
    } catch (error) {
        console.log(`error`, error);
        return error
    }
}

//new_userpword
async function newPassword(password, name) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/new_password?password=${password}&name=${name}`);
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            return data
        }
    } catch (error) {
        console.log(`error`, error)
        return error
    }
}

//get list of items:
async function getItems() {
    try {
        const response = await fetch('http://127.0.0.1:5000/list_items');
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            return data
        }

    } catch (error) {
        console.log(`error`, error)
        return error
    }
}

//gets hints for items

async function getHints(items) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/get_a_hint?items=${items}`);
        if (response.ok) {
            const data = await response.json();
            console.log(data);
            return data
        }

    } catch (error) {
        console.log(`error`, error)
        return error
    }
}

async function narration_continues(){
    try {
        const response = await fetch(`http://127.0.0.1:5000/stranger_advice`);
    if (response.ok) {
            const data = await response.json();
            console.log(data);
            return data
        }

    } catch (error) {
        console.log(`error`, error)
        return error
    }
}

// gets starting location


//main
async function main() {
    let txt = await startscreen();
    const start_screen = document.querySelector(`#dialog`);
    let paragraph = document.createElement(`p`);
    start_screen.appendChild(paragraph);
    let textnode = document.createTextNode(txt);
    paragraph.appendChild(textnode);
    const input = document.createElement(`input`);
    input.type = "text";
    start_screen.appendChild(input);
    const submit = document.createElement(`button`);
    const submit_name = document.createTextNode(`submit`);
    submit.appendChild(submit_name);
    start_screen.appendChild(submit);
    submit.addEventListener(`click`, async function (event) {
        event.preventDefault();
        const value = getInputValue();
        console.log(value);
        let response = await getName(value);
        const username = value
        let next_txt = document.createTextNode(response);
        const input_password = document.createElement('input');
        input_password.type = "password";
        if (response[0] === 'You need to create a password for your inventory.') {
            paragraph.appendChild(next_txt);
            paragraph.replaceChild(next_txt, textnode);
            start_screen.replaceChild(input_password, input);
            submit.addEventListener(`click`, async function (event) {
                const input = getInputValue();
                let result = await newPassword(input, username);
                let txt = document.createTextNode(result);
                const items = await getItems();
                const list_items = document.createElement(`ul`);
                start_screen.appendChild(list_items);
                for (let i = 0; i < items.length; i++) {
                    let item = document.createElement(`li`);
                    item.textContent = items[i];
                    list_items.appendChild(item);
                }
                paragraph.removeChild(next_txt);
                paragraph.appendChild(txt);
                start_screen.removeChild(input_password);
                start_screen.removeChild(submit);
                const nextDialog = document.createElement(`button`);
                nextDialog.textContent = "next";
                start_screen.appendChild(nextDialog);
                nextDialog.addEventListener(`click`, async function(event){
                   paragraph.removeChild(txt);
                   let result = await narration_continues();
                   let nexText = document.createTextNode(result);
                   paragraph.appendChild(nexText);
                });



            });
        }

    });


}


main();