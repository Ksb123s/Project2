function categoryChange(e) {
  var good_naver = ["어학사전", "블로그", "카페", "이미지", "지식iN", "인플루언서", "동영상", "쇼핑", "뉴스", "지도", "도서", "지식백과", "학술정보"];
  var good_google = ["동영상", "이미지", "도서", "쇼핑", "뉴스", "지도"];
  var good_daum = ["어학사전", "통합웹", "뉴스", "지도", "책", "이미지", "쇼핑"];
  var target = document.getElementById("detail");

  if (e.value == "naver") var d = good_naver;
  else if (e.value == "google") var d = good_google;
  else if (e.value == "daum") var d = good_daum;

  target.options.length = 0;

  for (x in d) {
    var opt = document.createElement("option");
    opt.value = d[x];
    opt.innerHTML = d[x];
    target.appendChild(opt);
  }
}
