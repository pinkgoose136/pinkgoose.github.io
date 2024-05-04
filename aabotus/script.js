function save() {
    var colorCheckboxes = document.querySelectorAll('.color-checkbox input[type="radio"]')
    var colorList = {};

    colorCheckboxes.forEach(function(checkbox) {
        var color = checkbox.value;
        colorList[color] = {'name': '', 'colors': {}}
        colorList[color]['colors'] = [];
        colorList[color]['name'] = document.getElementById(color+'-name').innerHTML
    });

    var allCells = document.querySelectorAll('td');

    allCells.forEach(function(cell) {
        var color1 = cell.style.backgroundColor;
        if (color1) {
            var color = rgbToHex(color1);
            if (color && colorList[color]) {
                colorList[color]['colors'].push(cell.id);
                cell.style.backgroundColor = '';
            }
        }
    });
    localStorage.setItem('colorList', JSON.stringify(colorList));
    for (var color in colorList) {
        console.log("Цвет:", color);
        console.log("Ячейки:", colorList[color]['colors']);
    }
    fill2()
}

function fill() {
    var colorList = JSON.parse(localStorage.getItem('colorList'));
    var allCells = document.querySelectorAll('td');
    document.getElementById('colorcheck').innerHTML = '';

    if (colorList) {
        for (var color in colorList) {
            var nm = colorList[color]['name']
            createTask(nm, color)
            var cells = colorList[color]['colors'];
            cells.forEach(function(idd) {
                document.getElementById(idd).style.backgroundColor = color;
            });
        }
    }
}

function fill2() {
    let tg = window.Telegram.WebApp;
    tg.CloudStorage.getItem('colorList', function(err, colorList) {
        var allCells = document.querySelectorAll('td');
        document.getElementById('colorcheck').innerHTML = '';
    
        if (colorList) {
            for (var color in colorList) {
                var nm = colorList[color]['name']
                createTask(nm, color)
                var cells = colorList[color]['colors'];
                cells.forEach(function(idd) {
                    document.getElementById(idd).style.backgroundColor = color;
                });
            }
        }
    })
}



function createTask(name, colo){
    var newCheckbox = document.createElement('input');
    newCheckbox.type = 'radio';
    newCheckbox.id = 'chk-'+colo
    newCheckbox.name = 'clr'
    newCheckbox.value = colo;
    newCheckbox.checked = true;

    var label = document.createElement('label');
    label.className = 'checkElement'
    label.appendChild(newCheckbox);

    var span = document.createElement('span')
    span.className = 'color-square'; span.style.backgroundColor = colo; 
    var label2 = document.createElement('label');
    label2.htmlFor = 'chk-'+colo; label2.id = colo+'-name'; label2.innerHTML = name;
     
    label.appendChild(span);
    label.appendChild(label2)

    newCheckbox.addEventListener('change', function() {
        var lbls = this.parentElement.parentElement.querySelectorAll('.checkElement')
        lbls.forEach(el => {
            if (el.querySelector('input').checked == false){
                var btns = el.querySelectorAll('button');
                btns.forEach(b => {
                    b.remove()
                })
            }
        });

        openEdit(label);
    });

    document.querySelector('.color-checkbox').appendChild(label);
}

function openEdit(element) {
    var editButton = document.createElement('button');
    editButton.textContent = 'Edit';
    editButton.className = 'edt'
    editButton.onclick = function() {
        openModal(element);
    };
    element.appendChild(editButton);
}


function rgbToHex(rgbString) {
    const values = rgbString.match(/\d+/g);
    if (!values || values.length !== 3) {
        throw new Error("Invalid RGB string format");
    }
    
    const r = parseInt(values[0], 10);
    const g = parseInt(values[1], 10);
    const b = parseInt(values[2], 10);

    const hex = "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    return hex;
}






function handleDeleteClick(event) {
    var idi = event.target.className

    var element = document.getElementById(`chk-${idi}`).parentElement;

    var tds = document.querySelectorAll('td')
    tds.forEach(t => {
        if (t.style.backgroundColor){
            if (rgbToHex(t.style.backgroundColor) == element.querySelector('input').value){
                t.style.backgroundColor = '#FFFFFF'
            }
        }
    });
    element.remove()
    closeModal();
}

function handleEditClick(event) {
    var parent = event.target.parentNode;
    var text = parent.textContent.trim();
    
    var backgroundColor = parent.style.backgroundColor;

    var editWindow = window.open('', '_blank', 'width=300,height=200');
    editWindow.document.write('<h2>Edit Element</h2>');
    editWindow.document.write('<label for="textInput">Text:</label>');
    editWindow.document.write('<input type="text" id="textInput" value="' + text + '"><br>');
    editWindow.document.write('<label for="colorInput">Color:</label>');
    editWindow.document.write('<input type="color" id="colorInput" value="' + backgroundColor + '"><br>');
    editWindow.document.write('<button onclick="saveChanges()">Save Changes</button>');
}


function openModal(element) {
    document.getElementById('myModal').style.display = "block";
    if (element != 'new'){
        var text = element.querySelector('label').textContent.trim();
        document.getElementById('textInput').value = text;
        var color = element.querySelector('label').id.split('-')[0]
        document.getElementById('colorInput').value = color;
        document.getElementById('btnch').className = color;
        document.getElementById('btnDel').className = color
    }else{
        document.getElementById('textInput').value = "Название";
        document.getElementById('colorInput').value = '#FF0000';
        document.getElementById('btnch').className = 'new';
        document.getElementById('btnDel').style.display = 'none'
    }
}

function closeModal() {
    document.getElementById('myModal').style.display = "none";
}


function saveChanges() {
    var newText = document.getElementById('textInput').value;
    var newColor = document.getElementById('colorInput').value;

    var idi = document.getElementById('btnch').className
    if (idi != 'new'){
        var element = document.getElementById(`chk-${idi}`).parentElement;

        var tds = document.querySelectorAll('td')
        tds.forEach(t => {
            if (t.style.backgroundColor){
                if (rgbToHex(t.style.backgroundColor) == element.querySelector('input').value){
                    t.style.backgroundColor = newColor
                }
            }
        });

        element.querySelector('label').textContent = newText;
        element.querySelector('span').style.backgroundColor = newColor;
        element.querySelector('input').value = newColor;
        element.querySelector('input').id = 'chk-'+newColor;
        element.querySelector('label').id = newColor+'-name';
        element.querySelector('label').htmlFor = 'chk-'+newColor;
    }else{
        createTask(newText, newColor)
    }
    closeModal();
}
