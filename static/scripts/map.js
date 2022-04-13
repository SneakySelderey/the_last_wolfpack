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
                 points.push({"coords": crds, "text": data["uboats"][i]["tactical_number"]});
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
        var placemark = new ymaps.Placemark(points[i]["coords"], {
            balloonContentHeader: points[i]["coords"],
            balloonContentBody: json_data[points[i]["coords"]].join(', '),
        }, {
            iconLayout: 'default#image',
            iconImageHref: 'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/placemark.png',
            iconImageSize: [30, 38],
            iconImageOffset: [0, 0]
        });
        map.geoObjects.add(placemark);
    }

    // Создаем экземпляр класса ymaps.control.SearchControl
    var mySearchControl = new ymaps.control.SearchControl({
        options: {
            // Заменяем стандартный провайдер данных (геокодер) нашим собственным.
            provider: new CustomSearchProvider(points),
            // Не будем показывать еще одну метку при выборе результата поиска,
            // т.к. метки коллекции myCollection уже добавлены на карту.
            noPlacemark: true,
            resultsPerPage: 5
        }});

    // Добавляем контрол в верхний правый угол,
    map.controls
        .add(mySearchControl, { float: 'right' });
    
    if (uboat != "all_boats") { 
        mySearchControl.search(uboat);
    }
}

function CustomSearchProvider(points) {
    this.points = points;
}

// Провайдер ищет по полю text стандартным методом String.ptototype.indexOf.
CustomSearchProvider.prototype.geocode = function (request, options) {
    var deferred = new ymaps.vow.defer(),
        geoObjects = new ymaps.GeoObjectCollection(),
    // Сколько результатов нужно пропустить.
        offset = options.skip || 0,
    // Количество возвращаемых результатов.
        limit = options.results || 20;
        
    var points = [];
    // Ищем в свойстве text каждого элемента массива.
    for (var i = 0, l = this.points.length; i < l; i++) {
        var point = this.points[i];
        if (point.text.toLowerCase().indexOf(request.toLowerCase()) != -1) {
            points.push(point);
        }
    }
    // При формировании ответа можно учитывать offset и limit.
    points = points.splice(offset, limit);
    // Добавляем точки в результирующую коллекцию.
    for (var i = 0, l = points.length; i < l; i++) {
        var point = points[i],
            coords = point.coords,
                    text = point.text;

        geoObjects.add(new ymaps.Placemark(coords, {
            name: text,
            description: coords,
            balloonContentBody: '<p>' + text + '</p>',
            boundedBy: [coords, coords]
        }));
    }

    deferred.resolve({
        // Геообъекты поисковой выдачи.
        geoObjects: geoObjects,
        // Метаинформация ответа.
        metaData: {
            geocoder: {
                // Строка обработанного запроса.
                request: request,
                // Количество найденных результатов.
                found: geoObjects.getLength(),
                // Количество возвращенных результатов.
                results: limit,
                // Количество пропущенных результатов.
                skip: offset
            }
        }
    });
    // Возвращаем объект-обещание.
    return deferred.promise();
};


var points = new Array();
var json_data = {};
getData('/api/uboats');
ymaps.ready(init);