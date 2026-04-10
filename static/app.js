//app.js
//2026-04-10
//index page

fetch("/api/hello")
	.then(res => res.json())
    .then(data => {
        document.querySelector("div").innerText = data.message  // 화면에 표시
        console.log(data.message)
    })