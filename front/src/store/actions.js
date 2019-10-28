

const actions = store => ({
    getRandomBooks: (state, payload) => ({ ...state, randomBooks: payload }),
    setLikeBook: (state, payload) => ({ ...state, likedBooks: state.likedBooks.concat(payload)}),
    removeLikeBook: (state, payload) => {
        state.likedBooks.splice(state.likedBooks.indexOf(payload),1);
        return state

    },
    getRecommendedBooks: (state, payload) => ({ ...state, recommendedBooks: payload})
});

export default actions;