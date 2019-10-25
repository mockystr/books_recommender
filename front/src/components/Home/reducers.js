import axios from 'axios';

console.log(process.env.USE_LOCALHOST, process.env.LOCALHOST_ADDRESS, process.env.REMOTE_ADDRESS);
console.log(process.env, process.env.NODE_ENV);
const USE_LOCALHOST = process.env.USE_LOCALHOST;
const LOCALHOST_ADDRESS = process.env.LOCALHOST_ADDRESS || "http://localhost:8000";
const REMOTE_ADDRESS = process.env.REMOTE_ADDRESS || "http://178.128.196.37:1234";

const DOMAIN = USE_LOCALHOST ? LOCALHOST_ADDRESS : REMOTE_ADDRESS;
const GET_RANDOM_BOOKS_URL = `${DOMAIN}/random_books`;
const GET_RECOMMENDATION_URL = `${DOMAIN}/recommendation?book_isbn=`;

export const getRandomBooks = async () => {
    return await axios.get(GET_RANDOM_BOOKS_URL)
};

export const getRecommendations = async (id) => {
    return await axios.get(GET_RECOMMENDATION_URL + id)
};