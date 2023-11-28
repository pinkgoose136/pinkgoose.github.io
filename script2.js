document.addEventListener('DOMContentLoaded', function () {
    var dropdown = document.getElementById('categorySelect');
    var options;

    if (aValue === 'channels' ) {
        options = ['Политика', 'Мемы', 'Новости', 'Технологии'];
    } 
    else if (aValue === 'groups') {
        options = ['Общение', 'Мемы', 'Знакомства', 'Тематичесике'];
    }  
    else if (aValue === 'bots') {
        options = ['Полезные', 'Игры', 'Развлечения'];
    }  
    else if (aValue === 'stickers' || aValue === 'emoji') {
        options = ['Мемы', 'Известности', 'Тематические', 'Анимированные'];
    }  

    for (let i = 0; i < options.length; i++) {
        var option = document.createElement('option');
        option.text = options[i];
        dropdown.add(option);
    }
    dropdown.value = '';
});