let currentPage = 1;
const itemsPerPage = 6;
let currentData = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchDataAndRender();
});

async function fetchDataAndRender() {
    try {
        const response = await fetch('database.md');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const markdown = await response.text();
        const data = parseMarkdownTable(markdown);
        
        // Initialize global state
        currentData = data;
        currentPage = 1;
        
        renderTabs(data);
        renderGrid();
    } catch (error) {
        console.error('Error loading database:', error);
        document.getElementById('poems-grid').innerHTML = '<p>載入資料失敗，請確認伺服器環境或檔案路徑。</p>';
    }
}

function parseMarkdownTable(markdown) {
    const lines = markdown.split('\n');
    const data = [];
    let isTable = false;
    let headers = [];

    for (let line of lines) {
        line = line.trim();
        if (line.startsWith('|')) {
            if (!isTable) {
                headers = line.split('|').map(h => h.trim()).filter(h => h);
                isTable = true;
            } else if (line.includes('---')) {
                continue;
            } else {
                const rowValues = line.split('|').map(v => v.trim()).filter((_, index, arr) => {
                    if (index === 0 && arr[0] === '') return false;
                    if (index === arr.length - 1 && arr[arr.length - 1] === '') return false;
                    return true;
                });
                
                if (rowValues.length === headers.length) {
                    const rowData = {};
                    headers.forEach((header, i) => {
                        rowData[header] = rowValues[i];
                    });
                    data.push(rowData);
                }
            }
        } else {
            isTable = false;
        }
    }
    return data;
}

function renderTabs(allData) {
    const categories = [...new Set(allData.map(item => item['類別']))];
    const tabsContainer = document.getElementById('category-tabs');
    tabsContainer.innerHTML = ''; // Clear existing
    
    // Add "All" tab
    const allBtn = document.createElement('button');
    allBtn.className = 'tab-btn active';
    allBtn.textContent = '全部';
    allBtn.onclick = () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        allBtn.classList.add('active');
        currentData = allData;
        currentPage = 1;
        document.querySelector('.container').classList.add('profile-to-bottom');
        renderGrid();
    };
    tabsContainer.appendChild(allBtn);

    // Add category tabs
    categories.forEach(category => {
        const btn = document.createElement('button');
        btn.className = 'tab-btn';
        btn.textContent = category;
        btn.onclick = () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentData = allData.filter(item => item['類別'] === category);
            currentPage = 1;
            document.querySelector('.container').classList.add('profile-to-bottom');
            renderGrid();
        };
        tabsContainer.appendChild(btn);
    });
}

function renderGrid() {
    const grid = document.getElementById('poems-grid');
    grid.innerHTML = ''; // Clear existing
    
    // Pagination slicing
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedData = currentData.slice(startIndex, endIndex);

    paginatedData.forEach(item => {
        const contentHtml = item['內文'].replace(/<br>/g, '\n');
        // Extract a short snippet (first line)
        const snippet = contentHtml.split('，')[0] + '...';

        const cardContainer = document.createElement('div');
        cardContainer.className = 'card-container';
        
        cardContainer.innerHTML = `
            <div class="card">
                <div class="card-front">
                    <div class="poem-category">${item['類別']}</div>
                    <h3 class="poem-title">${item['標題']}</h3>
                    <div class="poem-snippet">${snippet}</div>
                </div>
                <div class="card-back">
                    <div class="poem-full">${item['內文'].replace(/<br>/g, '<br/>')}</div>
                    <div class="poem-meta">
                        <span class="source">來源：${item['創作年份/來源']}</span>
                        <span class="annotation">註：${item['註釋']}</span>
                    </div>
                </div>
            </div>
        `;
        
        grid.appendChild(cardContainer);
    });
    
    renderPagination();
}

function renderPagination() {
    const paginationContainer = document.getElementById('pagination');
    if (!paginationContainer) return;
    
    paginationContainer.innerHTML = ''; // Clear existing
    
    const totalPages = Math.ceil(currentData.length / itemsPerPage);
    if (totalPages <= 1) return; // Hide pagination if only 1 page
    
    const prevBtn = document.createElement('button');
    prevBtn.className = 'page-btn';
    prevBtn.textContent = '上一頁';
    prevBtn.disabled = currentPage === 1;
    prevBtn.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            renderGrid();
            window.scrollTo({ top: document.getElementById('category-tabs').offsetTop - 50, behavior: 'smooth' });
        }
    };
    
    const pageInfo = document.createElement('span');
    pageInfo.className = 'page-info';
    pageInfo.textContent = `第 ${currentPage} / ${totalPages} 頁`;
    
    const nextBtn = document.createElement('button');
    nextBtn.className = 'page-btn';
    nextBtn.textContent = '下一頁';
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            renderGrid();
            window.scrollTo({ top: document.getElementById('category-tabs').offsetTop - 50, behavior: 'smooth' });
        }
    };
    
    paginationContainer.appendChild(prevBtn);
    paginationContainer.appendChild(pageInfo);
    paginationContainer.appendChild(nextBtn);
}
