import axios from 'axios';

const server_port = process.env.SERVER_PORT || 8000;
const server_address = process.env.SERVER_ADDRESS || "localhost";
const server_scheme = process.env.SERVER_SCHEME || "http";

const url = `${server_scheme}://${server_address}:${server_port}`;

const getRandomBooks = async (books_number = 10) => {
    const { data } = await axios.get(`${url}/get_random_books`, {
        'params': {'books_number': books_number}
    });
    return data;
};

export {
    getRandomBooks
}
