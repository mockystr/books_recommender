import { h, render } from "preact";
import { Provider } from 'redux-zero/preact';


import Main from './components/Main';
import store from './store';

const App = () => (
   <Provider store={store}>
       <Main />
   </Provider>
);

render(<App />, document.getElementById('root'));