import {h, Component} from "preact";
import { connect } from 'redux-zero/preact';

import actions from "../../store/actions.js";
import {getRandomBooks, getRecommendations} from "./reducers"
import {books} from "./data.json";
import style from "./style.scss";
import Book from "../Book";

class Home extends Component {
    componentDidMount() {
        getRandomBooks().then((r)=>{
            this.props.getRandomBooks(this.props.randomBooks.concat(r.data.books.length !== 0 ? r.data.books : books));
        }).catch((e)=>{
            this.props.getRandomBooks(books);
            console.log(e)
        });

        if (this.props.likedBooks) {
            this.props.likedBooks.map(item =>{
                setTimeout(
                    getRecommendations(item).then((r)=>{
                        this.props.getRecommendedBooks(this.props.recommendedBooks.concat(r.data.books));
                        this.props.getRandomBooks(this.props.randomBooks.concat(this.props.recommendedBooks.concat(r.data.books)));
                    })
                , 300)
            })
        }
    }

    render(props, state, context) {
        return (
            <div>
                <h1 className={style.title}>Рекомендации</h1>
                <div className={style.books}>
                    {props.recommendedBooks.length !== 0 ? props.recommendedBooks.map((item, key) => (
                        <Book item={item} key={key}/>
                    )) : 'Пусто'}
                </div>
                <h1 className={style.title}>Книги</h1>
                <div className={style.books}>
                    {props.randomBooks.length !== 0 ? props.randomBooks.map((item, key) => (
                        <Book item={item} key={key}/>
                    )) : 'Загрузка...'}
                </div>
            </div>

        )
    }
}

const mapToProps = (state) => ({
    randomBooks: state.randomBooks,
    likedBooks: state.likedBooks,
    recommendedBooks: state.recommendedBooks
});

export default connect(mapToProps, actions)(Home);