import React, {Component} from 'react';
import {getRandomBooks} from 'api';

export default class Books extends Component {
    state = {
        books: [],
    };

    async componentDidMount() {
        const {books} = await getRandomBooks();
        this.setState({books});
    }

    render_books = (books) => {
        return (
            <div className='container text-center'>
                <div className='row'>
                {books.map(el => {
                    return (
                        <div className="card" style={{"width": "18rem"}} key={el.ISBN}>
                            <img src={el.ImageURL} className="card-img-top" alt="..."/>
                            <div className="card-body">
                                <h5 className="card-title">{el.BookTitle}</h5>
                                <p className="card-text">{el.BookAuthor}</p>
                                <p className="card-text">{el.YearOfPublication}</p>
                                <p className="card-text">Rating: {el.BookRating}</p>
                                <a href="#" className="btn btn-primary">Получить рекомендацию</a>
                            </div>
                        </div>
                    )
                })}
                </div>
            </div>
        )
    };
    render() {
        const books = this.state.books;
        return this.render_books(books);
    }
}
