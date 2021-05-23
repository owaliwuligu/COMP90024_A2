import React, { useRef, useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import $ from 'jquery';
import './Map.css';

mapboxgl.accessToken = 'pk.eyJ1IjoiemphbmUiLCJhIjoiY2tjMWE1Z3ZyMDRzbDM2cXU3amhhM3M3cSJ9.hi0IVhPoWS2uPP47wEtC1Q';

const Map = () => {
  const mapContainerRef = useRef(null);

  const [lng, setLng] = useState(145);
  const [lat, setLat] = useState(-37);
  const [zoom, setZoom] = useState(8);

  // Initialize map when component mounts
  useEffect(() => {
    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: 'mapbox://styles/zjane/ckoeixq280iei17mkldrrs787',
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

    map.on('load', function() {
      console.log("load success");
      $.get("../../data/shop_count.json", function (data, code, jqxhr) {
        console.log("load data success");
        const restr = data;
        console.log(restr);
      })
    })
    // Clean up on unmount
    return () => map.remove();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div>
      <div className='sidebarStyle'>
        <div>
          Longitude: {lng} | Latitude: {lat} | Zoom: {zoom}
        </div>
      </div>
      <div className='map-container' ref={mapContainerRef} />
    </div>
  );
};

export default Map;
