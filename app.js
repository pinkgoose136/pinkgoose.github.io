let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#2cab37';

let item = "";

let buttonsContainer = document.getElementById("buttons-container");

buttonsContainer.addEventListener("click", function(event) {
    let target = event.target;
    
    if (target.classList.contains("button")) {
        if (tg.MainButton.isVisible) {
            tg.MainButton.hide();
        } else {
            let buttonText = target.innerText;
            tg.MainButton.setText(`Вы выбрали ${buttonText}!`);
            item = buttonText;
            tg.MainButton.show();
        }
    }
});

Telegram.WebApp.onEvent("mainButtonClicked", function() {
    tg.sendData(item);
});

let usercard = document.getElementById("usercard");

let p = document.createElement("p");

p.innerText = `${tg.initDataUnsafe.user.first_name}
${tg.initDataUnsafe.user.last_name}`;

usercard.appendChild(p);







