import { BrowserRouter as Router, Route,Switch, Link} from "react-router-dom"//配置路由
import MapView from "./pages/MapView"
import DataList from "./pages/DataList";
import './App.css';

function App() {
  return (
      <Router>
          <div className="App">
              {/* 配置导航菜单*/}
              <ul>
                  <li><Link to="/datalist"></Link></li>
                  <li><Link to="/mapview"></Link></li>
              </ul>
              <Link to="/datalist">数据页</Link>
              <Link to="/mapview">地图</Link>
              {/*只匹配其中一个*/}
              <Switch>
                  {/*配置路由*/}
                  <Route path="/datalist" component={DataList}></Route>
                  <Route path="/mapview" component={MapView}></Route>
              </Switch>
          </div>

      </Router>
  )
}

export default App;
