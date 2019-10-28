import createStore from 'redux-zero';

const initialState = {
    randomBooks: [],
    likedBooks: [],
    recommendedBooks: []
};
const store = createStore(initialState);

export default store;
