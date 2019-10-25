import {h, Component} from "preact";
import {connect} from "redux-zero/preact";
import actions from "../../store/actions";
import {route} from "preact-router";

import style from './style.scss';
import homeStyle from '../Home/style.scss';
import Book from "../Book";
import {getRecommendations} from '../Home/reducers';


class Detail extends Component {

    state = {
        isLiked: this.props.likedBooks.indexOf(this.props.id) !== -1,
        book: null,
        recommendations: []
    };

    componentDidMount() {
        if (this.props.randomBooks.length !== 0) {
            this.setState({book: this.props.randomBooks.filter((item) => (item.book_isbn === this.props.id))[0]})
            getRecommendations(this.props.id).then(r => {
                this.setState({recommendations: r.data.books})
            })
        } else {
            route('/', true)
        }
    }

    like = () => {
        if (!this.state.isLiked) {
            this.props.setLikeBook(this.props.id);
        } else {
            this.props.removeLikeBook(this.props.id)
        }
        this.setState({isLiked: !this.state.isLiked});
    };

    render(props, state, context) {
        return (
            state.book ?
                <div>
                    <div className={style.book}>
                        <div className={style.img}>
                            <img src={state.book.image_url} alt=""/>
                        </div>
                        <div className={style.about}>
                            <h3>{state.book.title}</h3>
                            <h5>{state.book.publication_year}</h5>
                            <h3>Author: {state.book.book_author}</h3>
                            <h3>Publisher: {state.book.publisher}</h3>
                            <hr/>
                            <span
                                className={state.isLiked ? "btn btn-outline-danger" : "btn btn-outline-success"}
                                onClick={this.like}>{state.isLiked ? "Не нравится" : "Нравится"}</span>
                        </div>
                    </div>
                    <h1 className={homeStyle.title}>Рекомендации</h1>
                    <div className={homeStyle.books}>
                        {state.recommendations.length !== 0 ? state.recommendations.map((item, key) => (
                            <Book item={item} key={key}/>
                        )) : 'Пусто'}
                    </div>
                </div> : "Загрузка..."
        )
    }
}

const mapToProps = (state) => ({
    randomBooks: state.randomBooks,
    likedBooks: state.likedBooks,
    recommendedBooks: state.recommendedBooks
});

export default connect(mapToProps, actions)(Detail);