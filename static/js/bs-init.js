document.addEventListener('DOMContentLoaded', function() {

	var charts = document.querySelectorAll('[data-bss-chart]');

	for (var chart of charts) {
		chart.chart = new Chart(chart, JSON.parse(chart.dataset.bssChart));
	}
}, false);

document.getElementById("clear").onclick = async function (){
	let response = await fetch("/api/clear_notifications");

	if (response.ok) { // if HTTP-status is 200-299
	// get the response body (the method explained below)
		let json = await response.json();
	} else {
		alert("HTTP-Error: " + response.status);
	}
	document.getElementById("clear-me").innerHTML = ""
	document.getElementById("notnum").innerHTML = ""
}