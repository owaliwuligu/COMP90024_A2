import React, {useRef, useEffect, useState} from 'react';
import mapboxgl from 'mapbox-gl';
import $ from 'jquery';
import './Map.css';
import * as echarts from 'echarts';
import '../../api/ajax.js';

import redpng from "../../assets/img/red.png";
import darkpng from "../../assets/img/dark_pink.png";
import pinkpng from "../../assets/img/pick.png";
import bluepng from "../../assets/img/blue.png";



mapboxgl.accessToken = 'pk.eyJ1IjoiemphbmUiLCJhIjoiY2tjMWE1Z3ZyMDRzbDM2cXU3amhhM3M3cSJ9.hi0IVhPoWS2uPP47wEtC1Q';


const Map = () => {
        const mapContainerRef = useRef(null);

        const [lng, setLng] = useState(145);
        const [lat, setLat] = useState(-37);
        const [zoom, setZoom] = useState(8);


        const user = ajax('/infouser/users');

        const usergeo = {
            "type": "FeatureCollection",
            "features": []
        };

        for (var userid in user) {
            var id = userid;
            var coor = [];
            var mag = {};

            const userid_data = $.extend({}, user[userid]);
            coor = userid_data.coordinates.coordinates;
            mag = userid_data.food_preference.total;
            usergeo.features.push(
                {
                    "type": "Feature",
                    "properties": {"id": id, "mag": mag},
                    "geometry": {"type": "Point", "coordinates": coor}
                }
            )

        }

        const data = ajax('/infores/restaurants');
        //console.log('data load successful')
        var sourcelist = {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': []
            }
        };
        var count = 0;
        for (var title in data) {
            var data_title = $.extend({}, data[title]);
            delete data_title.coordinates;
            delete data_title.total;

            var feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': data[title].coordinates
                },
                'properties': {
                    'title': title,
                    'history_data': data_title
                }
            }
            sourcelist.data.features.push(feature)
        }
        //console.log("sourcelist load finished")
        //console.log(sourcelist)

        // Initialize map when component mounts
        useEffect(() => {
            const map = new mapboxgl.Map({
                container: mapContainerRef.current,
                style: 'mapbox://styles/mapbox/light-v10',
                //style: 'mapbox://styles/zjane/ckoeixq280iei17mkldrrs787',
                center: [lng, lat],
                zoom: zoom
            });

            // Add navigation control (the +/- zoom buttons)
            map.addControl(new mapboxgl.NavigationControl(), 'top-right');

            map.on('move', () => {
                setLng(map.getCenter().lng.toFixed(4));
                setLat(map.getCenter().lat.toFixed(4));
                setZoom(map.getZoom().toFixed(2));
            });

            map.on('load', () => {


                console.log(usergeo)
                map.addSource('user_heat', {
                    'type': 'geojson',
                    'data': usergeo
                });


                map.addLayer(
                    {
                        'id': 'user-heat',
                        'type': 'heatmap',
                        'source': 'user_heat',
                        'maxzoom': 16,
                        'paint': {
                            'heatmap-weight': [
                                'interpolate',
                                ['linear'],
                                ['get', 'mag'],
                                0,
                                0,
                                6,
                                1
                            ],
                            'heatmap-intensity': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                0,
                                1,
                                9,
                                3
                            ],
                            'heatmap-color': [
                                'interpolate',
                                ['linear'],
                                ['heatmap-density'],
                                0,
                                'rgba(33,102,172,0)',
                                0.2,
                                'rgb(103,169,207)',
                                0.4,
                                'rgb(209,229,240)',
                                0.6,
                                'rgb(253,219,199)',
                                0.8,
                                'rgb(239,138,98)',
                                1,
                                'rgb(178,24,43)'
                            ],
                            'heatmap-radius': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                0,
                                2,
                                9,
                                20
                            ],
                            'heatmap-opacity': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                7,
                                1,
                                9,
                                0
                            ]
                        }
                    },
                    'waterway-label'
                );
                map.addLayer(
                    {
                        'id': 'userpoint',
                        'type': 'circle',
                        'source': 'user_heat',
                        'minzoom': 10,
                        'paint': {
// Size circle radius by earthquake magnitude and zoom level
                            'circle-radius': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                10,
                                ['interpolate', ['linear'], ['get', 'mag'], 1, 1, 6, 4],
                                20,
                                ['interpolate', ['linear'], ['get', 'mag'], 1, 5, 6, 9]
                            ],
// Color circle by earthquake magnitude
                            'circle-color': [
                                'interpolate',
                                ['linear'],
                                ['get', 'mag'],
                                1,
                                'rgba(33,102,172,0)',
                                2,
                                'rgb(103,169,207)',
                                3,
                                'rgb(209,229,240)',
                                4,
                                'rgb(253,219,199)',
                                5,
                                'rgb(239,138,98)',
                                6,
                                'rgb(178,24,43)'
                            ],
                            'circle-stroke-color': 'white',
                            'circle-stroke-width': 1,
// Transition from heatmap to circle layer by zoom level
                            'circle-opacity': [
                                'interpolate',
                                ['linear'],
                                ['zoom'],
                                7,
                                0,
                                8,
                                1
                            ]
                        }
                    },
                    'waterway-label'
                );


                map.loadImage(
                    'https://api.mapbox.com/v4/marker/pin-m-restaurant+f76565@2x.png?access_token=pk.eyJ1IjoiemphbmUiLCJhIjoiY2tjMWE1Z3ZyMDRzbDM2cXU3amhhM3M3cSJ9.hi0IVhPoWS2uPP47wEtC1Q',
                    function (error, image) {
                        if (error) console.log("Customs error: " + error);
                        map.addImage('pin-m-restaurant', image);
                        map.addSource('points', sourcelist);
                        map.addLayer({
                                'id': 'points',
                                'type': 'symbol',
                                'source': 'points',
                                'layout': {
                                    'icon-image': 'pin-m-restaurant',
                                    'text-field': ['get', 'title'],
                                    'text-font': [
                                        'Open Sans Semibold',
                                        'Arial Unicode MS Bold'
                                    ],
                                    'text-offset': [0, 1.25],
                                    'text-anchor': 'top'
                                }
                            }
                        )
                        //console.log(title + " has " + data[title].total + " scores and located at " + data[title].coordinates)
                    }
                );
            })

            // Clean up on unmount


            map.on('click', 'points', function (e) {
                    var coordinates = e.features[0].geometry.coordinates;
                    var history = e.features[0].properties.history_data;
                    var title = e.features[0].properties.title;
                    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
                    }
                    history = JSON.parse(history)
                    var date = [];
                    var score = [];
                    $.each(history, function (key, value) {
                        date.push(key);
                        score.push(value)
                    });
                    new mapboxgl.Popup()
                        .setLngLat(coordinates)
                        .setHTML("<div id='echarts' style='height: 400px; width: 600px'/>")
                        .addTo(map);


                    //console.log(document.getElementById('echarts'))

                    var myChart = echarts.init(document.getElementById('echarts'));
                    var option = {
                        title: {
                            text: 'How popular is ' + title + ' on Twitter'
                        },
                        xAxis: {
                            type: 'category',
                            data: date
                        },
                        yAxis: {
                            type: 'value'
                        },
                        series: [{
                            data: score,
                            type: 'line'
                        }]
                    };

                    myChart.setOption(option);


                }
            )
            return () => map.remove();
        }, []); // eslint-disable-line react-hooks/exhaustive-deps

        return (
            <div>
                <div className='sidebarStyle'>
                    <div>
                        Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
                    </div>

                </div>
                <div className='map-container' ref={mapContainerRef}>
                    <div id="left" className="sidebar flex-center left collapsed">
                        <div className="sidebar-content rounded-rect flex-center">
                            <body>
                            <div className="link-top"></div>
                            <h2>Instances Introduction:</h2>
                            <ul>
                                <li>
                                    <img src={ redpng } alt="" className="logo_img"/>
                                </li>
                                <li>
                                    <img src={ darkpng } alt="" className="logo_img"/>
                                </li>
                                <li>
                                    <img src={ pinkpng } alt="" className="logo_img"/>
                                </li>
                                <li>
                                    <img src={ bluepng } alt="" className="logo_img"/>
                                </li>
                                <div className="link-top"></div>
                                <li>
                                    <pre>The top 10 of popular restaurant:</pre>
                                </li>
                                <div className="link-top"></div>
                                <li>
                                    <table>
                                        <tr>
                                            <th>Restaurant</th>
                                            <th>Score</th>
                                        </tr>
                                        <tr>
                                            <th>Nick & Nora's Melbourne</th>
                                            <th>580723</th>
                                        </tr>
                                        <tr>
                                            <th>Bon Good to Eat</th>
                                            <th>10344</th>
                                        </tr>
                                        <tr>
                                            <th>Rare Steakhouse Midtown</th>
                                            <th>8890</th>
                                        </tr>
                                        <tr>
                                            <th>kfc</th>
                                            <th>7668</th>
                                        </tr>
                                        <tr>
                                            <th>subway</th>
                                            <th>7047</th>
                                        </tr>
                                        <tr>
                                            <th>Parco Ramen X Shujinko</th>
                                            <th>3470</th>
                                        </tr>
                                        <tr>
                                            <th>Massi</th>
                                            <th>3031</th>
                                        </tr>
                                        <tr>
                                            <th>oter</th>
                                            <th>2104</th>
                                        </tr>
                                        <tr>
                                            <th>spire</th>
                                            <th>1759</th>
                                        </tr>
                                        <tr>
                                            <th>sud</th>
                                            <th>1507</th>
                                        </tr>
                                        <tr>
                                            <th>sud</th>
                                            <th>1507</th>
                                        </tr>
                                        <tr>
                                            <th>a25</th>
                                            <th>1264</th>
                                        </tr>
                                        <tr>
                                            <th>gazi</th>
                                            <th>1199</th>
                                        </tr>
                                        <tr>
                                            <th>nora</th>
                                            <th>1128</th>
                                        </tr>
                                        <tr>
                                            <th>traveller</th>
                                            <th>1098</th>
                                        </tr>
                                        <tr>
                                            <th>mcdonalds</th>
                                            <th>1008</th>
                                        </tr>
                                        <tr>
                                            <th>counter</th>
                                            <th>865</th>
                                        </tr>
                                        <tr>
                                            <th>nashi</th>
                                            <th>720</th>
                                        </tr>
                                        <tr>
                                            <th>the common</th>
                                            <th>696</th>
                                        </tr>
                                        <tr>
                                            <th>vacant</th>
                                            <th>595</th>
                                        </tr>
                                        <tr>
                                            <th>cookie</th>
                                            <th>519</th>
                                        </tr>

                                    </table>
                                </li>
                            </ul>
                            </body>


                            <div>

                            </div>
                            <div className="sidebar-toggle rounded-rect right">
                            </div>
                        </div>
                    </div>
                </div>

            </div>


        );
    }
;

export default Map;
