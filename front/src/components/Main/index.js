import {h,Component} from "preact";
import {Router} from "preact-router";

import Home from "../Home";
import Detail from "../Detail";
import style from "./style.scss"
import { createHashHistory } from 'history';


class Main extends Component {

    render(props, state, context) {
        return (
            <div>
                <Router history={createHashHistory()}>
                    <Home path="/"/>
                    <Detail path="/book/:id"/>
                </Router>
            </div>
        );
    }
}


export default Main;