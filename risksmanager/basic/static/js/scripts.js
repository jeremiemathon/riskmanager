function add_fields(text) {
    var search = document.getElementById('dtSearch')
    var double_quote = '"'

    search.value = double_quote.concat(text).concat(double_quote)
    search.dispatchEvent(new Event('search'));
}