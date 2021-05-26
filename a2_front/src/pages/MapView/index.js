import {Link} from "react-router-dom";
import React from 'react'
import Map from './Map';

export default class MapView extends React.Component {
    render() {
        return (
            <>
                <div className="list_style">
                    <div>
                        <Link to="/home">Home</Link><span>|</span><Link to="/datalist">Data</Link>
                    </div>
                </div>
                <div>
                    <Map />
                </div>
            </>
        );
    }
}
