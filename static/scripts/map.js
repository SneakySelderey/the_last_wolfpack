let center = [54.31364762674106,10.13353274609368];


var getData = function(url) {
    console.log('getData started')
    var request = new XMLHttpRequest();
    request.open('GET', url, false);
    request.onload = function() {
        console.log('getData onloaded')
        getCoords(JSON.parse(request.response));
    };

    request.send();
};


function getCoords(data) {
    console.log('getCoords started')
    for(let i = 0; i < data["uboats"].length; i++){
        let crds = data["uboats"][i]["coords"]
        if (crds){
            crds = [parseFloat(crds.split(', ')[1]),
                    parseFloat(crds.split(', ')[0])]
            if (!points.includes(crds)){
                 points.push(crds);
            }
            if (json_data[crds]){
                json_data[crds].push(data["uboats"][i]["tactical_number"]);
            }
            else{
                json_data[crds] = [data["uboats"][i]["tactical_number"]];
            }
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
    console.log(points.length)
    for(let i = 0; i < points.length; i++){
        var placemark = new ymaps.Placemark(points[i], {
            balloonContentHeader: points[i].join(', '),
            balloonContentBody: json_data[points[i]].join(', '),
        }, {
            preset: 'islands#redIcon'
        });
        map.geoObjects.add(placemark);
    }
}

var points = new Array();
var json_data = {};
getData('/api/uboats');
ymaps.ready(init);