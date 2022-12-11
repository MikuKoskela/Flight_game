const cookieStorage ={
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

