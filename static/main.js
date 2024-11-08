const htmlFiles = [];
const contentDiv = document.getElementById('content');

// 从 Flask API 获取文件列表
fetch('/file-list')
    .then(response => response.json())
    .then(files => {
        files.forEach(file => htmlFiles.push(`web-cache/${file}`));
        loadHTML();
    })
    .catch(error => console.error('Error fetching file list:', error));

// 加载 HTML 页面内容
function loadHTML() {
    const promises = htmlFiles.map(file =>
        fetch(file).then(response => response.text())
    );
    Promise.all(promises).then(pages => {
        contentDiv.innerHTML = pages.join('<hr>');
    });
}

// 搜索并高亮
function searchText() {
    const query = document.getElementById('search').value;
    const innerHTML = contentDiv.innerHTML;
    contentDiv.innerHTML = innerHTML.replace(/<span class="highlight">(.*?)<\/span>/g, '$1');  // 清除之前的高亮

    if (query) {
        const regex = new RegExp(`(${query})`, 'gi');
        contentDiv.innerHTML = innerHTML.replace(regex, '<span class="highlight">$1</span>');
    }
}