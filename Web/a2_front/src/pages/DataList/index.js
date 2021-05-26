import React from 'react';
import "./DataList.css"
import * as echarts from 'echarts';
import { Link } from "react-router-dom";
import food_category from '../../data/food_category_score_modified.json'
import food_score from '../../data/food_sorted.json'

export default class DataList extends React.Component {
    componentDidMount() {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('tree'));
        var myChart2 = echarts.init(document.getElementById('line'));

        // 指定图表的配置项和数据
        var option = {
            title: {
                text: 'Food Category'
            },
            visualMap: [{
                type: 'continuous',
                min: 0,
                max: 1000,
                show: false
            }],
            backgroundColor: 'rgb(255, 255, 255)',
            series: [{
                type: 'tree',
                id: 'tree',
                initialTreeDepth: 1,
                symbolSize: 7,
                label: {
                    position: 'left',
                    verticalAlign: 'middle',
                    align: 'right',
                    fontSize: 15
                },
                leaves: {
                    label: {
                        position: 'right',
                        verticalAlign: 'middle',
                        align: 'left',
                        fontSize: 8,
                    }
                },
                labelLayout: {
                    hideOverlap: true,
                    draggable: true,
                },
                data: [food_category],
                emphasis: {
                    focus: 'descendant'
                }
            }]
        };

        var option2 = {
            visualMap: [{
                type: 'continuous',
                min: 0,
                max: 10,
                show: false
            }],
            grid: {
                top: '40%',
                bottom: '40%',
                show: true,
                containLabel: false,
            },
            tooltip: {
                trigger: 'axis',
                position: 'top'
            },
            xAxis: {
                id: 'line',
                name: 'Time',
                nameLocation: 'middle',
                axisLabel: {
                    show: false,
                },
                axisLine: {
                    show: false,
                },
                type: 'category',
                boundaryGap: false,
                data: []
            },
            yAxis: {
                id: 'line',
                name: 'Popularity',
                nameLocation: 'middle',
                axisLabel: {
                    show: false,
                },
                axisLine: {
                    show: false,
                },
                type: 'value'
            },
            backgroundColor: 'rgb(255, 255, 255)',
            series: [{
                data: [],
                type: 'line',
                id: 'line'
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
        myChart2.setOption(option2);

        myChart.on('mouseover', function (params) {
            var data = [];
            var date = [];
            for (var key in food_score[params.name])
            {
                if (key != "total")
                {
                    date.push(key)
                    data.push(food_score[params.name][key])
                }
            }

            option2 = {
                title: {
                    text: params.name,
                    top: '30%'
                },
                xAxis: {
                    id: 'line',
                    type: 'category',
                    boundaryGap: false,
                    data: date.reverse()
                },
                yAxis: {
                    id: 'line',
                    type: 'value'
                },
                backgroundColor: 'rgb(255, 255, 255)',
                series: [{
                    data: data.reverse(),
                    type: 'line',
                    id: 'line'
                }]
            }

            myChart2.setOption(option2);
        });
    }
    render() {
        return (
            <>
            <div className="data_header">
                <Link to="/home">Home</Link><span>|</span><Link to="/mapview">Map</Link>
            </div>
            <div id="main" className="data_box">
                <div className="row">
                    <div id="tree" style={{ width: 950, height: 800, display:"inline-block" }}></div>
                    <div id="line" style={{ width: 300, height: 800, display:"inline-block" }}></div>
                </div>
            </div>
            </>
        );
    }
};
