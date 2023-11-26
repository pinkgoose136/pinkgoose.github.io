function add(itemss){
    let itms = {}
    let ae = ''
    Object.keys(itemss).forEach(function(key2) {
        let valu2 = itemss[key2];
        let keyParts = key2.split('-');
        let tex = "";
        let keyy = "";
        switch (keyParts[2]) {
        case 'link': tex = ''; keyy = '1'; break;
        case 'name': tex = ''; keyy = '-1'; break;
        case 'desc': tex = ''; keyy = '3'; break;
        case 'type': tex = "Тип: "; keyy = '2'; break;
        case 'cat': tex = "Категории: "; keyy = '4'; break;
        case 'tag': tex = "Теги: "; keyy = '5'; break;
        case 'owner': tex = "Айди автора: "; keyy = '6'; break;
        case 'img': tex = ""; keyy = '11'; ae = valu2; break;
        default: tex = expr; keyy = '0'; break;
        }
        
        itms[keyy] = tex + valu2;
    });
    
    
    var head = document.createElement('div');
    head.classList.add('head');
    var left = document.createElement('div');
    left.classList.add('left');
    var right = document.createElement('div');
    right.classList.add('right');

    var imgElement = document.createElement('img');
    imgElement.classList.add('img');
    imgElement.src = "https://pinkgoose.pythonanywhere.com/static/empty.png"
    imgElement.alt = 'Alternative text';


    let title = document.createElement('div');
    let ssil = document.createElement('a');
    ssil.href = itms['1'];
    ssil.classList.add('lnk');
    ssil.textContent = itms['-1']; 
    title.appendChild(ssil);
    var desc = document.createElement('div');
    desc.textContent = itms['3']; 


    left.appendChild(imgElement);
    right.appendChild(title);
    right.appendChild(desc);
    head.appendChild(left);
    head.appendChild(right);

    keysDiv.appendChild(head);
    
    Object.keys(itms).forEach(function(i){
        if (i == '4' || i == '5'){
            let itemDiv = document.createElement('div');
            itemDiv.textContent = itms[i];
            keysDiv.appendChild(itemDiv);
        }
    });
    keysListDiv.appendChild(keysDiv);
}