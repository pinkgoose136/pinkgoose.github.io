function addCategory() {
    var categorySelect = document.getElementById('categorySelect');
    var selectedCategory = categorySelect.options[categorySelect.selectedIndex].value;
    var categoryList = document.getElementById('categoryList');
    if (selectedCategory && categoryList.childElementCount < 3) {
        var categoryItem = document.createElement('div');
        categoryItem.textContent = selectedCategory;
        categoryItem.classList.add('category');
        categoryItem.onclick = function() {
            categoryList.removeChild(categoryItem);
            categorySelect.options.add(new Option(categoryItem.textContent, categoryItem.textContent));
            categorySelect.value = '';
        };

        categoryList.appendChild(categoryItem);
        categorySelect.options.remove(categorySelect.selectedIndex);
        categorySelect.value = '';
    }
}

function createTag(existingTags) {
    var tagList = document.getElementById('tagList');
    tagList.innerHTML = '';
    existingTags.forEach(element => {
        var tagItem = document.createElement('div');
        tagItem.textContent = element;
        tagItem.classList.add('tag');
        tagItem.onclick = function() {
            tagList.removeChild(tagItem);
        };
        tagList.appendChild(tagItem);
    });
}

function createCat(existingTags) {
    var categoryList = document.getElementById('categoryList');
    var categorySelect = document.getElementById('categorySelect');
    categoryList.innerHTML = '';
    existingTags.forEach(element => {
        var catItem = document.createElement('div');
        catItem.textContent = element;
        catItem.classList.add('category');
        catItem.onclick = function() {
            categoryList.removeChild(catItem);
            categorySelect.options.add(new Option(catItem.textContent, catItem.textContent));
            categorySelect.value = '';
        };
        categoryList.appendChild(catItem);
        categorySelect.value = '';
    });
}

function addTagOnComma(inputElement) {
    var tagList = document.getElementById('tagList');
    var tagText = inputElement.value.slice(0, -1).toLowerCase();
    var existingTags = Array.from(tagList.getElementsByClassName('tag')).map(tag => tag.textContent);

    if (inputElement.value.includes(',') && inputElement.value !== ',') {
        if (tagText && !existingTags.includes(tagText)) {
            var tagItem = document.createElement('div');
            tagItem.textContent = tagText;
            tagItem.classList.add('tag');
            tagItem.onclick = function() {
                tagList.removeChild(tagItem);
            };
            tagList.appendChild(tagItem);
        }
        inputElement.value = '';
    }
}

function adjustTextAreaHeight() {
    var textarea = document.getElementById("description");
    textarea.style.height = "auto";
    var newHeight = textarea.scrollHeight;
    textarea.style.height = newHeight + "px";
}

function cts_addc(tg, aValue, idd){
    var dropdown = document.getElementById('categorySelect');
    dropdown.innerHTML = '';

    if (aValue === 'emoji'){
        aValue = 'stickers'
    }

    tg.CloudStorage.getItem('cts-'+aValue, function(err, item) {
        if (err) {
            document.getElementById('opa').innerHTML = 'Ошибка получения значений: ' + err;
        } else {
            tg.CloudStorage.getItem('lng-'+idd, function(err, item) {
                if (err) {
                    console.log('Ошибка получения значений: ' + err);
                } else {
                    let tutu = {};
                    let yy = item.split('\n');
                    yy.forEach(ee => {
                        let yd = ee.split(': ');
                        tutu[yd[0]] = yd[1];
                    });
                    
                    let tu = item.split(', ')
                    tu.shift()
                    for (let i = 0; i < tu.length; i++) {
                        var option = document.createElement('option');
                        option.text = tutu[tu[i]];
                        dropdown.add(option);
                    }
                    dropdown.value = '';
                }
            });
        }
    })
}

function create_drop(tg, aaValue, exclude, idde){
    var dropdown = document.getElementById('categorySelect');
    dropdown.innerHTML = '';

    if (aaValue === 'emoji'){
        aaValue = 'stickers'
    }

    tg.CloudStorage.getItem('cts-'+aaValue, function(err, item) {
        if (err) {
            document.getElementById('opa').innerHTML = 'Ошибка получения значений: ' + err;
        } else {
            let tu = item.split(', ')
            tu.shift()
            let tut = tu.filter(item => !exclude.includes(item));

            tg.CloudStorage.getKeys(function(err, keys) {
                if (err) {
                    console.log('Ошибка получения ключей: ' + err);
                } else {
                    let idd = idde
                    let ker = keys.filter(word => word.includes('lng-'+idd))
                    if (ker.length == 0){
                        idd = 'en'
                    }
                    tg.CloudStorage.getItem('lng-'+idd, function(err, item) {
                        if (err) {
                            console.log('Ошибка получения значений: ' + err);
                        } else {
                            let tutu = {};
                            let yy = item.split('\n');
                            yy.forEach(ee => {
                                let yd = ee.split(': ');
                                tutu[yd[0]] = yd[1];
                            });
                            
                            for (let i = 0; i < tut.length; i++) {
                                var option = document.createElement('option');
                                option.text = tutu[tu[i]];
                                dropdown.add(option);
                            }
                            dropdown.value = '';
                        }
                    });
                }
            })
        }
    })
}

function translate(tg, wordlist, idd){
    tg.CloudStorage.getKeys(function(err, keys) {
        if (err) {
            console.log('Ошибка получения ключей: ' + err);
        } else {
            let ker = keys.filter(word => word.includes('lng-'+idd))
            if (ker.length == 0){
                idd = 'en'
            }
            tg.CloudStorage.getItem('lng-'+idd, function(err, item) {
                if (err) {
                    console.log('Ошибка получения значений: ' + err);
                } else {
                    let tutu = {};
                    let yy = item.split('\n');
                    yy.forEach(ee => {
                        let yd = ee.split(': ');
                        tutu[yd[0]] = yd[1];
                    });
                    console.log(tutu)
                    wordlist.forEach(sus =>{
                        if (sus == 'search'){
                            document.getElementById(sus).placeholder = tutu[sus];
                        }else{
                            document.getElementById(sus).textContent = tutu[sus];
                        }
                    })
                }
            });
        }
    })
}