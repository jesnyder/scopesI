var cities = L.layerGroup();
var fdaLocs = L.layerGroup();
var cdcStats = L.layerGroup();
var cdcWestNile = L.layerGroup();
var cdcDengue = L.layerGroup();
var climatePalmer = L.layerGroup();


var mbAttr = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';
var mbUrl = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
var streets = L.tileLayer(mbUrl, {id: 'mapbox/streets-v11', tileSize: 512, zoomOffset: -1, attribution: mbAttr});

var osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	});


//var map = L.map('map').setView([37.8, -96], 4);
var map = L.map("map", {
		center: [37.8, -96],
		zoom: 4,
		minZoom: 4,
		maxZoom: 18,
		zoomSnap: 0.1,
		zoomDelta: 0.1,
		layers: [osm]
		});

	var baseLayers = {
		'OpenStreetMap': osm,
		'Streets': streets
	};

	var overlays = {
		/* 'FDA Inspection Site': fdaLocs,
		'Arthritis-Crude Prevalence': cdcStats, */
		'West Nile': cdcWestNile,
		'Dengue': cdcDengue,
		'Palmer Z Index': climatePalmer,
	};

	var layerControl = L.control.layers(baseLayers, overlays).addTo(map);

	var satellite = L.tileLayer(mbUrl, {id: 'mapbox/satellite-v9', tileSize: 512, zoomOffset: -1, attribution: mbAttr});
	layerControl.addBaseLayer(satellite, 'Satellite');


	var tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
	}).addTo(map);

	// control that shows state info on hover
	var info = L.control();

	info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'info');
		this.update();
		return this._div;
	};

	info.update = function (props) {
		this._div.innerHTML = '<b>US Dengue </b>' +  (props ?
			'<br><b>' + props.NAME + '</b><br><b>' + props['Dengue']['value'] + '%</b> with Degnue' : '<br>Hover over a state');
	};

	info.addTo(map);


	function style(feature) {
		return {
			weight: 0,
			opacity: 1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.7,
			fillColor: feature.properties['Dengue2023']['color']
		};
	}

	function styleWestNile(feature) {
		return {
			weight: 0,
			opacity: 1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.7,
			fillColor: feature.properties['WestNile2023']['color']
		};
	}


	function stylePalmer(feature) {
		return {
			weight: 0,
			opacity: 1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.7,
			fillColor: feature.properties['Palmer2023']['color']
		};
	}

	function highlightFeature(e) {
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#666',
			dashArray: '',
			fillOpacity: 0.7
		});

		if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
			layer.bringToFront();
		}

		info.update(layer.feature.properties);
	}


	function resetHighlight(e) {
		geojson_counties.resetStyle(e.target);
		info.update();
	}


	function zoomToFeature(e) {
		map.fitBounds(e.target.getBounds());
	}


	function onEachFeature(feature, layer) {
		layer.on({
			mouseover: highlightFeature,
			mouseout: resetHighlight,
			click: zoomToFeature
		});
	}


	function onEachFacility(feature, layer) {
			var website = feature.properties.website;

			var popupContent = '<b>' +
					feature.properties.name + '</b><br>' + '<a href="' + feature.properties.website + '" target="_blank" rel="noopener">' + feature.properties.website + '</a>'  + '<br>' + feature.properties.city + ', ' + feature.properties.state + '</p>';
			if (feature.properties && feature.properties.popupContent) {
				popupContent += feature.properties.popupContent;
			}
			layer.bindPopup(popupContent);
		}


	/* global statesData */
	var geojson_counties = L.geoJson(cdc_stats, {
		style: style,
		/* onEachFeature: onEachFeature */
	}).addTo(map).addTo(cdcDengue);
	

	/* global statesData */
	var geojson_countiesWestNiles = L.geoJson(cdc_stats, {
		style: styleWestNile,
		/* onEachFeature: onEachFeature */
	}).addTo(map).addTo(cdcWestNile);

	/* global statesData */
	var geojson_countiesWestNiles = L.geoJson(cdc_stats, {
		style: stylePalmer,
		/* onEachFeature: onEachFeature */
	}).addTo(map).addTo(climatePalmer);

	

	/* global statesData 
	var geojson_facility = L.geoJson(facilityData, {
		style: style,
		onEachFeature: onEachFacility
	}).addTo(map).addTo(fdaLocs);
	*/

	/* cite source of information */
	map.attributionControl.addAttribution('| <a href="https://www.cdc.gov/arthritis/data_statistics/state-data-current.htm" target="_blank" rel="noopener">CDC Arthritis Statistics</a> | <a href="https://datadashboard.fda.gov/ora/cd/inspections.htm" target="_blank" rel="noopener"> FDA Inspection Record </a>' );
