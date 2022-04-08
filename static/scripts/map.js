let center = [50.97265436797006,9.793819812133787];


var getData = function(url) {
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'json';
    request.onload = function() {
        getCoords(request.response);
    };

    request.send();
};


function getCoords(data) {
    for(let i = 0; i < data["uboats"].length; i++){
        let crds = data["uboats"][i]["coords"]
        if (crds){
            crds = [parseFloat(crds.split(', ')[1]),
                    parseFloat(crds.split(', ')[0])]
            points.push(crds);
            json_data[crds] = data["uboats"][i]["tactical_number"]
        }
    }
}

function init() {
	let map = new ymaps.Map('map-test', {
		center: center,
		zoom: 6
	});

    map.controls.remove('geolocationControl'); // удаляем геолокацию
    map.controls.remove('searchControl'); // удаляем поиск
    map.controls.remove('trafficControl'); // удаляем контроль трафика
    map.controls.remove('typeSelector'); // удаляем тип
    map.controls.remove('fullscreenControl'); // удаляем кнопку перехода в полноэкранный режим
    map.controls.remove('zoomControl'); // удаляем контрол зуммирования
    map.controls.remove('rulerControl'); // удаляем контрол правил
    for(let i = 0; i < points.length; i++){
        var placemark = new ymaps.Placemark(points[i], {}, {
            preset: 'islands#redIcon'
        });
        map.geoObjects.add(placemark);
    }
}

getData('/api/uboats');
ymaps.ready(init);
var points = [];
var json_data = {};