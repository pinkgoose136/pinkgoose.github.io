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
        };

        categoryList.appendChild(categoryItem);
        categorySelect.options.remove(categorySelect.selectedIndex);
        categorySelect.value = '';
    }
}

function createTag(existingTags) {
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

function addTagOnComma(inputElement) {
    var tagList = document.getElementById('tagList');
    var tagText = inputElement.value.slice(0, -1);
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

function create_drop(aaValue){
    var dropdown = document.getElementById('categorySelect');
    var options;

    if (aaValue === 'channels' ) {
        options = ['Политика', 'Мемы', 'Новости', 'Технологии'];
    } 
    else if (aaValue === 'groups') {
        options = ['Общение', 'Мемы', 'Знакомства', 'Тематичесике'];
    }  
    else if (aaValue === 'bots') {
        options = ['Полезные', 'Игры', 'Развлечения'];
    }  
    else if (aaValue === 'stickers' || aaValue === 'emoji') {
        options = ['Мемы', 'Известности', 'Тематические', 'Анимированные'];
    }  

    for (let i = 0; i < options.length; i++) {
        var option = document.createElement('option');
        option.text = options[i];
        dropdown.add(option);
    }
    dropdown.value = '';
}