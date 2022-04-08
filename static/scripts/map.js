let center = [50.97265436797006,9.793819812133787];
let points = [];


function getData() {
   fetch('/api/uboats')
  .then((response) => {
      console.log('ok')
      return response.json();
  })
  .then((data) => {
      console.log(data);
  });

}

function getCoords(data) {
    for(let i = 0; i < data.length; i++){
        console.log(data[i]["coords"])
    }
}

function init() {
	let map = new ymaps.Map('map-test', {
		center: center,
		zoom: 17
	});

    map.controls.remove('geolocationControl'); // удаляем геолокацию
    map.controls.remove('searchControl'); // удаляем поиск
    map.controls.remove('trafficControl'); // удаляем контроль трафика
    map.controls.remove('typeSelector'); // удаляем тип
    map.controls.remove('fullscreenControl'); // удаляем кнопку перехода в полноэкранный режим
    map.controls.remove('zoomControl'); // удаляем контрол зуммирования
    map.controls.remove('rulerControl'); // удаляем контрол правил
}

ymaps.ready(init);
const boats = getData();
console.log(boats);