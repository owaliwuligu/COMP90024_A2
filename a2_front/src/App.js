import {BrowserRouter as Router, Route, Switch, Redirect} from "react-router-dom"//configure router
import Home from "./pages/Home"
import MapView from "./pages/MapView";
import DataList from "./pages/DataList";
import './App.css';

function App() {
  return (
        <Router>
          <Switch>
              {/*Configure routing*/}
              <Route path="/home" component={Home}></Route>
              <Route path="/mapview" component={MapView}></Route>
              <Route path="/datalist" component={DataList}></Route>
              <Redirect to="/home"></Redirect>
          </Switch>
        </Router>
  )
}

export default App;
