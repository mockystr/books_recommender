import {h} from "preact";
import {Link} from "preact-router";
import style from "./style.scss";


const Book = (props) => (
    <div className={`card ${style.book}`}>
        <Link href={`/book/${props.item.book_isbn}`} style="text-decoration: none; color: black;">
            <img className="card-img-top text-center" src={props.item.image_url} alt=""/>
            <div className="card-body">
                <h5 className="card-title">{props.item.title}</h5>
                <p className="card-text">{props.item.book_author}</p>
            </div>
        </Link>
    </div>
);

export default Book;