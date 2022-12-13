async function getItemsAndHints(){
    try {
        const response = await fetch('http://127.0.0.1:5000/list_items');
        if (response.ok) {
            const items = await response.json();
            console.log(items);
                document.querySelector("#object1").innerHTML = items[0];
                document.querySelector("#object2").innerHTML = items[1];
                document.querySelector("#object3").innerHTML = items[2];
                document.querySelector("#object4").innerHTML = items[3];
                const hints = await iterate_hints(items);
                console.log(hints);

            return items
        }

    } catch (error) {
        console.log(`error`, error)
        return error
    }
}

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

async function iterate_hints(itemList){
    const hints = []
    for (let i = 0; i < itemList.length; i++) {
        hints[i] = await getHints(itemList[i]);
    }
    console.log(hints);
    return hints
}
function show_hints(num) {
    const id = (`#object` + num)
    const item = (document.querySelector(id)).innerHTML;
    console.log(item)
    const value = document.getElementById("hints").src = `http://127.0.0.1:5000/get_a_hint?items=${item}`;
    console.log(value)
    return value
}

const the_items = getItemsAndHints()
console.log(the_items)





























/* const cookieStorage ={
    getItem:(key) => {
        const cookies = document.cookie
            .split(`;`)
            .map(cookie => cookie.split(`=`))
            .reduce((acc, [key, value]) => ({...acc, [key.trim()]: value}), {}); //Have to use trim because cookie strings tend to have whitespaces in the cookie string / {} -> makes reduce function initialized as an object
        return cookies[key];
    },
    setItem: (key, value) =>{
        document.cookie = `${key}=${value}`;
    },
};

const storageType = cookieStorage; // localStorage remembers value even if chrome is closed. sessionStorage clears the value when chrome is closed
const consentPropertyName = `my_cookie`; // Name of the cookie

const shouldShowPopup = () => !storageType.getItem(consentPropertyName); // if consentPropertyName has a value -> returns false / if there is no value returns true
const saveToStorage = () => storageType.setItem(consentPropertyName, true);

window.onload = () =>{
    const consentPopup = document.getElementById(`consent-popup`);
    const acceptBtn = document.getElementById(`accept`);

    const acceptFn = event => {
        saveToStorage(storageType); // when user clicks the button -> save
        consentPopup.classList.add(`hidden`)
    };

    acceptBtn.addEventListener(`click`, acceptFn)

    if (shouldShowPopup(storageType)) {
        setTimeout(() => {
            consentPopup.classList.remove(`hidden`);
        }, 2000);
    }
};
*/
