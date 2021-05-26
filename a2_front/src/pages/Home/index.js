import React, {Component} from 'react'
import { Link } from 'react-router-dom';
import "./Home.css"
import bgURL from "../../assets/img/2_new.jpg";

export default class Home extends Component {
    render () {
        return (
            <>
                <div className="app_header">
                    <Link to="home">Home</Link>
                </div>
                <div className="app_content">
                    <img className="bg_img" src={ bgURL } />
                    <div className="router_btn">
                    <Link to="/datalist">data</Link>
                        <span>|</span>
                    <Link to="/mapview" >map</Link>
                    </div>
                </div>
                <div className="footer">
                    Group61, Dongxu Xiang, Jiacheng Yu, Jing Li, Tianyu Zhou, Yujia Zhu,
                </div>
            </>
        )
    }
}