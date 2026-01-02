// 初期表示
window.onload = function () {
  const list = document.getElementById("list");
  list.innerHTML = dataList;
};

// 検索キーワードの分割
function divideKeywords(searchText) {
  const regex = /[\u0020\u3000\t]+/;
  return searchText.split(regex);
}

// 検索処理
function searchKeyword(searchText) {
  const keys = divideKeywords(searchText);
  const list = dataList.split(/\n/);
  let matchLines = "";
  list.forEach((row) => {
    let found = true;
    keys.forEach((key) => {
      if (key != "") {
        if (!row.includes(key)) {
          found = false;
        }
      }
    });
    // 検索された場合
    if (found) {
      matchLines += row + "\n";
    }
  });
  return matchLines;
}

// 検索ボタンクリック
function onSearchButtonClick() {
  const keyword = document.getElementById("keyword").value;
  if (keyword.trim() == "") {
    searchList = dataList;
  } else {
    searchList = searchKeyword(keyword);
  }
  const list = document.getElementById("list");
  list.innerHTML = searchList;
}

// 全て表示ボタンクリック
function onAllButtonClick() {
  const list = document.getElementById("list");
  list.innerHTML = dataList;
}
