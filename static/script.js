// 開始測驗
function start() {
    document.getElementById('des').style.display = 'none';
    document.getElementById('q1').style.display = 'block';
}

// 建立上一題按鈕機制
function previous(count) {
    document.getElementById('q' + String(count - 1)).style.display = 'block';
    document.getElementById('q' + String(count)).style.display = 'none';
}

// 建立下一題按鈕機制，需確認使用者是否已選擇答案
function next(count) {
    const yesOption = document.getElementById(
        'q' + String(count) + 'yes'
    ).checked;
    const noOption = document.getElementById(
        'q' + String(count) + 'no'
    ).checked;

    if (!yesOption && !noOption) {
        alert('請選擇一個選項再繼續！');
        return;
    }

    setTimeout(() => {
        document.getElementById('q' + String(count)).style.display = 'none';

        const next = document.getElementById('q' + String(count + 1));
        next.style.display = 'block';

        // 特別處理最後一題，隱藏提交按鈕
        if (count == 24) {
            document.getElementById('submit').style.display = 'none';
        }
    }, 100);
}

// 確認回答最後一題後，顯示提交按鈕
function showSubmit() {
    document.getElementById('submit').style.display = 'block';
}
