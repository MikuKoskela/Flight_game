const difficulty = document.querySelector("#dropdown")
difficulty.addEventListener("click",check_difficulty)
const play = document.querySelector("#block")
play.addEventListener("click",login_page)

function check_difficulty() {
    if (difficulty.value === "Easy") {
        console.log("Easy")
    } else if (difficulty.value === "Medium") {
        console.log("Medium")
    } else {
        console.log("Hard")
    }
}
function login_page(){


}


