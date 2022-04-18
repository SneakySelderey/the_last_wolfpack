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
        json_fate.push([data["uboats"][i]["fate"]]);
    }
}

function placeMark(points, json_data, map, colour, i) {
    p_data = json_data[points[i]["coords"]]
    data_with_a = [];
    for(let i = 0; i < p_data.length; i ++){
        data_with_a.push('<a href="/uboats#' + p_data[i] + '">' + p_data[i] + '</a>')
    }
    var placemark = new ymaps.Placemark(points[i]["coords"], {
        balloonContentHeader: points[i]["coords"].join(', '),
        balloonContentBody: data_with_a.join(', '),
    }, {
        iconLayout: 'default#image',
        iconImageHref: 'https://the-last-wolfpack.herokuapp.com/static/img/misc.%20pictures/placemark_' + colour + '.png',
        iconImageSize: [15, 19],
        iconImageOffset: [-6.5, -6]
    });
    map.geoObjects.add(placemark);
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

    globalThis.count39 = 0
    globalThis.count40 = 0
    globalThis.count41 = 0
    globalThis.count42 = 0
    globalThis.count43 = 0
    globalThis.count44 = 0
    globalThis.count45 = 0

    console.log(points.length)
    for(let i = 0; i < points.length; i++){
        sentence = json_fate[i];
        if(sentence[0].includes('1939')) { 
            placeMark(points, json_data, map, 'red', i)
            globalThis.count39 += 1
        }
        if(sentence[0].includes('1940')) { 
            placeMark(points, json_data, map, 'yellow', i)
            globalThis.count40 += 1
        }
        if(sentence[0].includes('1941')) { 
            placeMark(points, json_data, map, 'green', i)
            globalThis.count41 += 1
        }
        if(sentence[0].includes('1942')) { 
            placeMark(points, json_data, map, 'orange', i)
            globalThis.count42 += 1
        }
        if(sentence[0].includes('1943')) { 
            placeMark(points, json_data, map, 'black', i)
            globalThis.count43 += 1
        }
        if(sentence[0].includes('1944')) { 
            placeMark(points, json_data, map, 'purple', i)
            globalThis.count44 += 1
        }
        if(sentence[0].includes('1945')) { 
            placeMark(points, json_data, map, 'blue', i)
            globalThis.count45 += 1
        }
    }
    console.log(count39, count40, count41, count42, count43, count44, count45)

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
        console.log('a')
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
var json_fate = new Array();
getData('/api/uboats');
ymaps.ready(init);